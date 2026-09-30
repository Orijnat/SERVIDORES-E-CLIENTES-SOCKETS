import socket

# Endereço e porta do servidor devem ser iguais aos do servidor
HOST = '127.0.0.1'
PORT = 5000


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        print("Conectando ao servidor...")

        try:
            cliente.connect((HOST, PORT))
        except ConnectionRefusedError:
            print(f"[ERRO] Não foi possível conectar em {HOST}:{PORT}. "
                  "O servidor está em execução?")
            return

        print(f"Conectado a {HOST}:{PORT}")
        print("Comandos: TIME | STATUS | ECHO <texto> | EXIT\n")

        try:
            while True:
                comando = input("Digite um comando: ").strip()

                if not comando:
                    continue

                cliente.sendall(comando.encode('utf-8'))

                resposta = cliente.recv(1024)

                if not resposta:
                    print("[!] O servidor encerrou a conexão.")
                    break

                print(f"Resposta do servidor: {resposta.decode('utf-8')}\n")

                if comando.upper() == 'EXIT':
                    break

        except (ConnectionResetError, BrokenPipeError):
            print("[ERRO] A conexão com o servidor foi perdida.")
        except KeyboardInterrupt:
            print("\n[!] Interrompido pelo usuário.")

    print("Conexão encerrada.")


if __name__ == '__main__':
    main()
