import cv2
import serial
import time
from pyzbar.pyzbar import decode

# IDs permitidos
ids_permitidos = [1001, 1002, 1003]

# Conexão com o Arduino
arduino = serial.Serial('COM6', 9600)  # Ajuste para a porta correta
time.sleep(2)  # Aguarda conexão

def ler_qrcode(frame):
    dados = decode(frame)
    for codigo in dados:
        data = codigo.data.decode('utf-8')
        try:
            import json
            obj = json.loads(data)
            return obj.get("id")
        except:
            pass
    return None

def escutar_arduino():
    while True:
        if arduino.in_waiting:
            linha = arduino.readline().decode('utf-8').strip()
            print(f"[ARDUINO] {linha}")

            if linha == "VEICULO_DETECTADO":
                print("Veículo detectado. Lendo QRCode...")
                camera = cv2.VideoCapture(0)

                tentativa = 0
                id_lido = None

                while tentativa < 20:
                    _, frame = camera.read()
                    id_lido = ler_qrcode(frame)

                    if id_lido:
                        print(f"ID lido: {id_lido}")
                        break

                    tentativa += 1
                    time.sleep(0.2)

                camera.release()
                cv2.destroyAllWindows()

                if id_lido in ids_permitidos:
                    print("ID autorizado. Enviando comando para abrir a cancela.")
                    arduino.write(b'ABRIR_CANCELA\n')
                else:
                    print("ID não autorizado.")
                    arduino.write(b'NAO_AUTORIZADO\n')

if __name__ == "__main__":
    try:
        escutar_arduino()
    except KeyboardInterrupt:
        print("Encerrando aplicação...")
        arduino.close()
