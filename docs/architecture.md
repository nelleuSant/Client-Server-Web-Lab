# Arquitetura do ambiente

## 1. Visão geral

O projeto utiliza duas máquinas virtuais no Proxmox VE. Uma máquina
representa o cliente que acessa a aplicação por navegador; a outra
hospeda os serviços necessários à aplicação web.

A separação entre cliente e servidor permite observar o fluxo de
requisições HTTP e a comunicação entre a aplicação e o banco de dados.

## 2. Componentes

|  Componente       |Responsabilidade                                      |
|  ---------------- |------------------------------------------------------|
|  Proxmox VE       |Hipervisor que hospeda as máquinas virtuais           |
|  `vmbr3`          |Bridge privada para comunicação entre as VMs          |
|  `client01`       |Estação cliente com navegador e ferramentas de teste  |
|  `server01`       |Sistema Debian que hospeda os serviços                |
| Nginx             |Recebe requisições HTTP e as encaminha ao backend     |
|  Flask            |Executa a lógica da aplicação                         |
|  PostgreSQL       |Armazena os dados da aplicação                        |
|  Docker Compose   |Define e inicia os serviços em containers             |
|  Terraform        |Provisiona os recursos virtuais no Proxmox            | 

## 3. Fluxo de comunicação

1.  O usuário acessa a aplicação pelo navegador na VM cliente.
2.  O navegador envia uma requisição HTTP ao endereço do servidor.
3.  O Nginx recebe a requisição na porta publicada pelo serviço.
4.  O Nginx encaminha a requisição ao backend Flask pela rede interna
    dos containers.
5.  Quando necessário, o Flask consulta ou modifica os dados no
    PostgreSQL.
6.  O backend devolve a resposta ao Nginx, que a encaminha ao navegador.

O PostgreSQL será acessível pelo backend dentro da rede Docker. Sua
porta não será publicada para a rede das máquinas virtuais na
configuração inicial.

## 4. Separação de responsabilidades

Terraform será utilizado para criar e gerenciar as máquinas virtuais e
suas interfaces de rede. Docker Compose será utilizado para definir e
executar os serviços da aplicação no servidor.

Essa separação evita usar Terraform para gerenciar o ciclo de vida dos
containers e mantém cada ferramenta concentrada em sua finalidade.

## 5. Limites da primeira versão

-   Duas VMs em um único host Proxmox.
-   Uma rede privada sem roteador virtual.
-   Sem alta disponibilidade.
-   Sem acesso externo à aplicação.
-   Sem firewall virtual dedicado.
-   Serviços web e banco de dados hospedados na VM servidor.

## 6. Diagrama

O diagrama visual será adicionado em `docs/images/` após a validação da
configuração de rede e dos serviços. Até lá, a topologia está descrita
em [`network.md`](network.md).
