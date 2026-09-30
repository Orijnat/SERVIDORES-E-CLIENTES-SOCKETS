# Comunicação Cliente-Servidor com Sockets TCP

Sistema simples de comunicação entre um **cliente** e um **servidor** usando sockets TCP em Python. O servidor interpreta comandos de texto enviados pelo cliente e responde de acordo com um protocolo próprio.

## Arquivos

| Arquivo | Descrição |
|---|---|
| `socket_servidor.py` | Servidor TCP multithreaded |
| `socket_cliente.py` | Cliente TCP interativo |
| `servidor.log` | Gerado automaticamente ao executar o servidor |

## Requisitos

- Python 3.6 ou superior

## Como executar

1. Abra um terminal e inicie o servidor:

2. Abra **outro** terminal e inicie o cliente:

3. Digite os comandos no cliente. Para testar vários clientes ao mesmo tempo, abra mais terminais e rode o cliente em cada um.

4. Para encerrar o servidor, pressione `Ctrl+C` no terminal dele.


## Protocolo

Protocolo textual do tipo pedido-resposta: o cliente envia uma linha de texto com um comando e o servidor responde com uma única mensagem.

| Comando | Ação do servidor | Exemplo de resposta |
|---|---|---|
| `TIME` | Retorna o horário atual do servidor 
| `STATUS` | Retorna o estado do servidor 
| `ECHO <texto>` | Devolve exatamente o texto enviado
| `EXIT` | Encerra a conexão com o cliente 
| *(outro)* | Retorna mensagem de erro

Um `ECHO` sem texto também retorna erro: `ERRO: uso correto -> ECHO <mensagem>`.
