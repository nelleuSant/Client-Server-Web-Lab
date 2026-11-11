# Plano de testes e validação

**Status:** testes planejados; preencher resultados após a implantação.

## 1. Objetivo

Verificar a comunicação entre cliente e servidor, o funcionamento da
aplicação web, a persistência no PostgreSQL e o isolamento esperado da
rede.

## 2. Testes de rede

Na VM cliente, verificar a configuração:

``` bash
ip addr
ip route
```

Testar a comunicação com o servidor:

``` bash
ping -c 4 10.10.30.10
```

Resultado esperado: respostas ICMP, caso a regra correspondente esteja
habilitada no Proxmox Firewall.

## 3. Testes HTTP

Com a aplicação em execução, testar:

``` bash
curl -I http://10.10.30.10
```

Resultado esperado: resposta HTTP do serviço Nginx/aplicação. Registrar
o código HTTP observado e investigar respostas diferentes do esperado.

## 4. Testes funcionais da aplicação

Validar as operações previstas no CRUD:

-   Criar uma tarefa;
-   Listar tarefas;
-   Atualizar uma tarefa;
-   Alterar o status;
-   Excluir uma tarefa.

Registrar entradas utilizadas e resultados observados, sem incluir
credenciais.

## 5. Teste de persistência

1.  Criar um registro pela aplicação.
2.  Reiniciar os containers.
3.  Consultar novamente o registro pela aplicação.
4.  Confirmar que os dados continuam disponíveis.

O teste verifica a persistência configurada para o PostgreSQL.

## 6. Testes de isolamento

Após remover a interface temporária conectada à `vmbr0`:

-   Verificar a tabela de rotas das duas VMs.
-   Confirmar a comunicação entre cliente e servidor.
-   Verificar que as VMs não possuem rota padrão para a internet.
-   Confirmar que a porta PostgreSQL não está publicada na interface de
    rede da VM.
-   Verificar as regras efetivas do Proxmox Firewall.

A ausência de rota padrão é um resultado de configuração; testes
adicionais devem confirmar o comportamento real da rede.

## 7. Registro de resultados

  -------------------------------------------------------------------------
  Teste              Resultado esperado Resultado obtido  Status
  ------------------ ------------------ ----------------- -----------------
  IP do cliente      `10.10.30.20/24`   A preencher       Pendente

  IP do servidor     `10.10.30.10/24`   A preencher       Pendente

  Ping               Comunicação        A preencher       Pendente
  cliente-servidor   permitida                            

  Requisição HTTP    Resposta do        A preencher       Pendente
                     serviço web                          

  CRUD               Operações          A preencher       Pendente
                     concluídas                           

  Persistência       Dados preservados  A preencher       Pendente
                     após reinício                        

  Isolamento externo Sem rota externa   A preencher       Pendente
                     na configuração                      
                     final                                
  -------------------------------------------------------------------------

## 8. Evidências

Armazenar capturas e saídas sanitizadas em `docs/images/`. Não incluir
tokens, senhas, endereços públicos sensíveis ou arquivos de configuração
que contenham segredos.
