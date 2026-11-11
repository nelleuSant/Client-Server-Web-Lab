# Plano de implantação

**Status:** procedimento planejado. Registrar os comandos e resultados
efetivamente utilizados durante a execução.

## 1. Preparação

Antes de alterar o Proxmox:

1.  Confirmar acesso administrativo ao host.
2.  Registrar a configuração atual de rede.
3.  Verificar disponibilidade de armazenamento e memória.
4.  Confirmar que `vmbr3` e `10.10.30.0/24` estão livres.
5.  Identificar o template Debian ou a ISO que será utilizada.

Comandos de inspeção:

``` bash
ip -br addr
ip route
cat /etc/network/interfaces
```

## 2. Criar a bridge

Criar a bridge `vmbr3` pela interface de rede do Proxmox ou por
configuração persistente equivalente, sem associar uma interface física.

Configuração conceitual:

``` text
auto vmbr3
iface vmbr3 inet manual
    bridge-ports none
    bridge-stp off
    bridge-fd 0
```

Validar a configuração antes de aplicá-la. A sintaxe final deverá
respeitar a configuração de rede já existente no host.

## 3. Provisionar as VMs

Terraform será utilizado para criar as VMs:

-   VMID 201: `client01`.
-   VMID 202: `server01`.

A configuração de CPU, memória, disco, template e provider será definida
após verificar os recursos disponíveis no host e os templates
existentes.

Não armazenar credenciais ou arquivos de estado Terraform no Git.

## 4. Instalar e configurar os sistemas

Instalar Debian nas duas VMs. Configurar:

-   Hostnames;
-   IPs estáticos da rede `10.10.30.0/24`;
-   Interface principal conectada à `vmbr3`;
-   Ausência de gateway na rede final.

Durante a preparação, uma segunda interface conectada à `vmbr0` poderá
ser utilizada temporariamente para atualizações e downloads. Evitar
gateways padrão concorrentes.

## 5. Preparar o servidor

No `server01`:

1.  Instalar Docker Engine e Docker Compose.
2.  Criar os arquivos de configuração da aplicação.
3.  Definir os serviços Nginx, Flask e PostgreSQL em Docker Compose.
4.  Configurar variáveis de ambiente e credenciais fora do
    versionamento.
5.  Persistir os dados do PostgreSQL em volume.
6.  Publicar para a rede da VM somente a porta necessária do Nginx.

O PostgreSQL deverá permanecer na rede interna dos containers, sem
publicação direta da porta 5432.

## 6. Finalizar o isolamento

Após concluir os downloads e a instalação:

1.  Desligar as VMs.
2.  Remover a interface temporária conectada à `vmbr0` da configuração
    Terraform e das VMs.
3.  Aplicar a alteração com Terraform e conferir o resultado.
4.  Iniciar as VMs.
5.  Verificar endereços e rotas.
6.  Confirmar que cliente e servidor se comunicam pela `vmbr3`.
7.  Confirmar que não existe conectividade externa na configuração
    final.

## 7. Registrar evidências

Adicionar em `docs/images/` capturas sem credenciais ou informações
sensíveis:

-   Bridge `vmbr3` no Proxmox;
-   Hardware e interfaces das VMs;
-   Serviços em execução;
-   Aplicação aberta no navegador cliente;
-   Testes de conectividade e HTTP.

Atualizar este documento com versões, comandos e eventuais diferenças
entre o plano e a implantação real.
