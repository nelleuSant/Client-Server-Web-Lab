# Client-Server Web Environment

> Projeto acadêmico da pós-graduação em Desenvolvimento Web: implantação
> de um ambiente virtual cliente-servidor para desenvolvimento e
> execução de uma aplicação web.

**Status:** planejamento e documentação inicial. A infraestrutura ainda
não foi implantada.

## Objetivo

Construir um ambiente cliente-servidor virtualizado no Proxmox VE,
utilizando software livre e ferramentas reproduzíveis. O projeto busca
demonstrar a comunicação entre um cliente web, um servidor de aplicação
e um banco de dados, além de documentar o provisionamento e a validação
do ambiente.

## Arquitetura planejada

O ambiente será composto por duas máquinas virtuais conectadas a uma
bridge privada no Proxmox:

| Componente   | Identificação           | Configuração planejada           |
|--------------|-------------------------|----------------------------------|
| Hipervisor   | Proxmox VE              | Host físico existente            |
| Rede privada | `vmbr3`                 | `10.10.30.0/24`, sem porta física|
| Cliente      | `client01` / VMID `201` | Debian com ambiente gráfico      |
| Servidor     | `server01` / VMID `202` | Debian Server                    |
| Aplicação    | Flask                   | Backend web                      |
| Proxy web    | Nginx                   | Entrada HTTP para a aplicação    |
|Banco de dados| PostgreSQL              |Persistência dos dados            |
|Provisionamento| Terraform              |Criação das VMs no Proxmox        |
|Implantação de serviços| Docker Compose |Execução dos serviços no servidor |
            

O cliente utilizará o navegador para acessar a aplicação hospedada no
servidor. O Flask será responsável pela lógica da aplicação e se
comunicará com o PostgreSQL pela rede interna do Docker.

Consulte [`docs/architecture.md`](docs/architecture.md) e
[`docs/network.md`](docs/network.md) para os detalhes.

## Escopo

### Incluído na primeira versão

-   Provisionamento das VMs com Terraform.
-   Rede privada dedicada por meio da bridge `vmbr3`.
-   Acesso temporário à internet durante instalação e preparação.
-   Aplicação web simples com operações CRUD.
-   Nginx, Flask e PostgreSQL implantados com Docker Compose.
-   Testes de conectividade, acesso HTTP e persistência.
-   Documentação técnica e evidências da implantação.

### Fora do escopo inicial

-   pfSense ou outro firewall virtual.
-   Kubernetes, Ansible ou Packer.
-   Pipeline de CI/CD.
-   Exposição da aplicação à internet pública.
-   Monitoramento avançado e centralização de logs.
-   Alta disponibilidade ou clusterização.

O controle de tráfego será feito com os recursos nativos do Proxmox VE.
A rede privada não terá roteador ou gateway próprio.

## Organização do repositório

``` text
client-server-web-environment/
├── README.md
├── infra/
│   └── terraform/
├── app/
├── deploy/
│   └── nginx/
├── database/
└── docs/
    ├── architecture.md
    ├── network.md
    ├── installation.md
    ├── testing.md
    └── images/
```

Os diretórios de infraestrutura, aplicação e implantação serão
preenchidos nas próximas etapas.

## Pré-requisitos previstos

-   Servidor Proxmox VE operacional.
-   Bridge `vmbr3` disponível no Proxmox.
-   Template ou mídia de instalação Debian.
-   Terraform compatível com a versão do provider Proxmox selecionada (`bpg/proxmox`).
-   Token de API do Proxmox com permissões mínimas necessárias.
-   Acesso SSH com chave pública autorizada no host Proxmox (`root@pve`) para envio de *snippets* Cloud-Init.
-   Docker Engine e Docker Compose no servidor Debian.

As versões exatas das ferramentas serão registradas após a validação do
ambiente.

### Configuração de acessos e permissões no Proxmox (Terraform)

Para que o provider `bpg/proxmox` consiga autenticar via API e SSH, baixar a imagem Cloud-Init, enviar os *snippets* e provisionar as VMs sem erros de permissão (`HTTP 403`) ou falha de handshake SSH, é necessário configurar no Proxmox VE:

1. **Acesso SSH ao nó Proxmox (para upload de *snippets* Cloud-Init):**
   O recurso `proxmox_virtual_environment_file` utiliza SFTP/SSH direto com o nó Proxmox (pois a API HTTP não suporta envio de *snippets*).
   - Autorize a chave pública SSH da estação de trabalho no usuário `root` do Proxmox:
     ```bash
     ssh-copy-id -i ~/.ssh/id_ed25519.pub root@<IP_DO_PROXMOX>
     ```
   - No `provider.tf`, referencie a chave privada (`private_key = file(pathexpand("~/.ssh/id_ed25519"))`) no bloco `ssh` (ou carregue a chave no `ssh-agent` via `ssh-add`).
   - Certifique-se de que o storage de destino dos arquivos YAML (ex.: `HD-500GB` ou `local`) esteja com o tipo de conteúdo **Snippets** habilitado em *Datacenter -> Storage*.

2. **Extensão da imagem Cloud-Init (`.img` em vez de `.qcow2`):**
   Quando a imagem é baixada via `proxmox_virtual_environment_download_file` com `content_type = "iso"`, o Proxmox exige que o `file_name` salvo termine com a extensão **`.img`** (ex.: `debian-13-generic-amd64.img`) para permitir a importação posterior do disco nas VMs.

3. **Usuário, Token de API e Role de Permissões (ACLs):**
   No Proxmox VE 8+, quando o Token da API possui *Privilege Separation* (`privsep = 1`) ativado, os privilégios efetivos são a **interseção** entre as permissões do usuário e as do token. Além disso, atribuir duas roles diferentes separadamente no mesmo caminho (`/`) para o mesmo usuário sobrescreve a anterior. Por isso, todos os privilégios necessários de VM, Storage e Rede devem estar unificados na mesma Role e vinculados tanto ao usuário quanto ao token:
   ```bash
   # 1. Criar usuário e token (caso ainda não existam)
   pveum user add terraform@pam
   pveum user token add terraform@pam terraform --privsep 1

   # 2. Criar/atualizar a Role unificada com permissões de VM, Datastore e Rede (query-url-metadata exige Sys.AccessNetwork, Sys.Audit e Sys.Modify)
   pveum role add TerraformProvisionamento -privs "Datastore.Allocate,Datastore.AllocateSpace,Datastore.AllocateTemplate,Datastore.Audit,Pool.Allocate,SDN.Use,Sys.AccessNetwork,Sys.Audit,Sys.Console,Sys.Modify,Sys.PowerMgmt,VM.Allocate,VM.Audit,VM.Clone,VM.Config.CDROM,VM.Config.CPU,VM.Config.Cloudinit,VM.Config.Disk,VM.Config.HWType,VM.Config.Memory,VM.Config.Network,VM.Config.Options,VM.Migrate,VM.PowerMgmt"

   # 3. Caso a role já exista, apenas atualize os privilégios:
   pveum role modify TerraformProvisionamento -privs "Datastore.Allocate,Datastore.AllocateSpace,Datastore.AllocateTemplate,Datastore.Audit,Pool.Allocate,SDN.Use,Sys.AccessNetwork,Sys.Audit,Sys.Console,Sys.Modify,Sys.PowerMgmt,VM.Allocate,VM.Audit,VM.Clone,VM.Config.CDROM,VM.Config.CPU,VM.Config.Cloudinit,VM.Config.Disk,VM.Config.HWType,VM.Config.Memory,VM.Config.Network,VM.Config.Options,VM.Migrate,VM.PowerMgmt"

   # 4. Aplicar a Role na raiz (/) tanto para o usuário quanto para o token
   pveum acl modify / -user terraform@pam -role TerraformProvisionamento
   pveum acl modify / -token 'terraform@pam!terraform' -role TerraformProvisionamento
   ```

## Implantação --- visão geral

1.  Verificar a configuração de rede atual do Proxmox e confirmar que a
    faixa `10.10.30.0/24` não está em uso.
2.  Criar a bridge privada `vmbr3`.
3.  Provisionar as VMs `client01` e `server01` com Terraform.
4.  Instalar e configurar Debian nas duas VMs.
5.  Usar temporariamente uma interface ligada à `vmbr0` para
    atualizações e downloads necessários.
6.  Remover a interface temporária e validar o isolamento da rede.
7.  Implantar Nginx, Flask e PostgreSQL com Docker Compose.
8.  Executar os testes e registrar evidências.

O procedimento detalhado será mantido em
[`docs/installation.md`](docs/installation.md).

## Segurança e informações sensíveis

Não versionar tokens, senhas, chaves privadas, arquivos `.tfstate`,
arquivos `.tfvars` reais ou arquivos de ambiente com credenciais. O
repositório deverá conter apenas exemplos sem segredos, como arquivos
`.example`.

A aplicação será acessível somente pela rede privada do laboratório. O
PostgreSQL não deverá publicar sua porta para a rede das VMs: o backend
Flask acessará o banco pela rede interna dos containers.

## Status do projeto

-   [x] Definição inicial do escopo.
-   [x] Proposta inicial de topologia.
-   [x] Estrutura inicial de documentação.
-   [ ] Inspecionar bridges e endereçamento existentes no Proxmox.
-   [ ] Criar `vmbr3`.
-   [ ] Definir recursos e templates das VMs.
-   [ ] Implementar Terraform.
-   [ ] Implantar aplicação e banco de dados.
-   [ ] Validar e documentar os testes.
-   [ ] Elaborar relatório acadêmico final.

## Observação acadêmica

Este repositório documenta o planejamento e, posteriormente, a execução
da atividade de implantação de um ambiente virtual cliente-servidor. As
seções serão atualizadas com configurações, resultados e capturas reais
à medida que as etapas forem concluídas. Não considerar como executada
nenhuma etapa marcada como pendente.

## Licença

A licença será definida quando o conteúdo inicial do projeto estiver
estabilizado.
