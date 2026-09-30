import socket
import threading
from datetime import datetime


# Configuracoes do servidor

HOST = '127.0.0.1'
PORT = 5000
ARQUIVO_LOG = 'servidor.log'

# Trava para que duas threads nao escrevam no log ao mesmo tempo
trava_log = threading.Lock()


def registrar(texto):
    linha = f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {texto}"
    print(linha)
    with trava_log:
        with open(ARQUIVO_LOG, 'a', encoding='utf-8') as f:
            f.write(linha + '\n')


def processar_comando(mensagem):

    # Separa o comando do restante do texto
    partes = mensagem.strip().split(' ', 1)
    comando = partes[0].upper()
    argumento = partes[1] if len(partes) > 1 else ''

    if comando == 'TIME':
        return f"Hora atual: {datetime.now().strftime('%H:%M:%S')}", False

    if comando == 'STATUS':
        return "Servidor ativo e aguardando conexões", False

    if comando == 'ECHO':
        if not argumento:
            return "ERRO: uso correto -> ECHO <mensagem>", False
        return argumento, False

    if comando == 'EXIT':
        return "Conexão encerrada", True

    # Validação de comando nao existente
    return f"ERRO: comando desconhecido '{comando}'. Use TIME, STATUS, ECHO <texto> ou EXIT", False


def atender_cliente(conexao, endereco):
    """Função  que permite a conecxao de mais de um cliente"""
    ip = endereco[0]
    registrar(f"Cliente conectado ({ip}:{endereco[1]})")

    try:
        with conexao:
            while True:
                dados = conexao.recv(1024)

                if not dados:
                    registrar(f"Cliente {ip} desconectou inesperadamente.")
                    break

                mensagem = dados.decode('utf-8').strip()
                if not mensagem:
                    continue

                registrar(f"Comando recebido de {ip}: {mensagem}")

                resposta, encerrar = processar_comando(mensagem)

                conexao.sendall(resposta.encode('utf-8'))
                registrar(f"Resposta enviada a {ip}: {resposta}")

                if encerrar:
                    registrar(f"Conexão com {ip} encerrada.")
                    break

    except ConnectionResetError:
        registrar(f"Conexão com {ip} foi interrompida pelo cliente.")
    except UnicodeDecodeError:
        registrar(f"Mensagem inválida (não é UTF-8) recebida de {ip}.")
    except Exception as erro:
        registrar(f"Erro inesperado com {ip}: {erro}")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))
        servidor.listen()

        registrar(f"Servidor iniciado na porta {PORT}")
        registrar("Pressione Ctrl+C para encerrar o servidor.")

        try:
            while True:
                conexao, endereco = servidor.accept()
                thread = threading.Thread(
                    target=atender_cliente,
                    args=(conexao, endereco),
                    daemon=True
                )
                thread.start()
        except KeyboardInterrupt:
            registrar("Servidor encerrado pelo administrador.")


if __name__ == '__main__':
    main()
