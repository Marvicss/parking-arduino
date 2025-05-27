import serial
import time

def conectar_arduino(porta='COM6', baudrate=9600):
    try:
        with serial.Serial(porta, baudrate, timeout=2) as arduino:
            time.sleep(2)  # Aguarda o Arduino inicializar
            print("Conectado com sucesso!")

            # Aqui você pode escrever ou ler da serial
            arduino.write(b'ping\n')  # Exemplo de comando
            print("Comando enviado.")

            # Leitura (opcional)
            if arduino.in_waiting:
                resposta = arduino.readline().decode().strip()
                print("Resposta:", resposta)

    except serial.SerialException as e:
        print(f"Erro de serial: {e}")
    except Exception as e:
        print(f"Erro geral: {e}")

if __name__ == '__main__':
    conectar_arduino()
