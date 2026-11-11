# Topologia e plano de endereçamento

**Status:** proposta; endereços e bridge devem ser verificados no host
antes da configuração.

## 1. Objetivo

Criar uma rede virtual dedicada ao projeto cliente-servidor, sem
reutilizar as bridges do laboratório de cibersegurança e sem utilizar
pfSense ou outro roteador virtual.

## 2. Bridge privada

  |Parâmetro         |Valor proposto|
  |----------------- |-------------------------------------|
  |Nome              |`vmbr3`|
  |Tipo             |Linux Bridge do Proxmox|
  |Porta física      |Nenhuma (`bridge-ports none`)|
  |Rede              |`10.10.30.0/24`|
  |Gateway da rede   |Não haverá|
  |Finalidade        |Comunicação entre as VMs do projeto|

A bridge deverá ser criada somente após confirmar que o nome está livre
e que a faixa IP não conflita com redes existentes.

## 3. Endereçamento

  |Máquina      |VMID   | Hostname       | Endereço
  |-------------|------ |-------------|------------------
  |Cliente       |201 |`client01`   |`10.10.30.20/24`
  |Servidor      |202 |`server01`   |`10.10.30.10/24`

Os endereços serão configurados estaticamente. Não haverá DHCP ou DNS
dedicado na primeira versão. O acesso poderá ser realizado pelo IP do
servidor.

## 4. Acesso temporário à internet

Durante a instalação e preparação, cada VM poderá utilizar
temporariamente uma segunda interface conectada à bridge existente
`vmbr0`.

-   `net0`: conectada à `vmbr3`, para comunicação privada do projeto.
-   `net1`: conectada temporariamente à `vmbr0`, para atualizações e
    downloads.

A configuração de rotas deverá ser verificada para evitar gateways
padrão concorrentes. Após concluir a preparação, a interface temporária
será removida da configuração Terraform e das VMs.

A conectividade será então validada novamente. A arquitetura final não
terá rota para a internet.

## 5. Fluxos previstos na rede final

  -----------------------------------------------------------------------
  Origem            Destino           Tráfego           Política proposta
  ----------------- ----------------- ----------------- -----------------
  `client01`        `server01`        TCP 80            Permitir

  `client01`        `server01`        ICMP              Permitir para
                                                        diagnóstico

  `client01`        `server01`        TCP 443           Reservado para
                                                        HTTPS futuro

  Rede das VMs      PostgreSQL        TCP 5432          Não publicar na
                                                        rede das VMs

  Outras origens    VMs               Demais tráfegos   Restringir
                                                        conforme política
                                                        do Proxmox
  -----------------------------------------------------------------------

As regras definitivas do Proxmox Firewall serão configuradas e testadas
durante a implantação. Não presumir que a simples criação da bridge
habilita uma política de bloqueio.

## 6. Isolamento e limitações

Uma bridge sem porta física permite comunicação entre as VMs conectadas
a ela, mas não fornece internet por si só. Como não haverá gateway, as
VMs não terão rota para outras redes na configuração final.

O acesso à interface de gerenciamento do Proxmox continuará ocorrendo
pela rede de gerenciamento já existente, fora do escopo da rede privada
do projeto.

## 7. Verificações antes da implantação

No host Proxmox, inspecionar:

``` bash
ip -br addr
cat /etc/network/interfaces
ip route
```

Confirmar:

-   `vmbr3` ainda não está em uso.
-   `10.10.30.0/24` não conflita com redes existentes.
-   A configuração atual de `vmbr0`, `vmbr1` e `vmbr2` será preservada.
-   A criação da bridge não altera a conectividade de gerenciamento do
    host.

Não aplicar alterações de rede remotamente sem garantir acesso ao
console do host e um procedimento de recuperação.
