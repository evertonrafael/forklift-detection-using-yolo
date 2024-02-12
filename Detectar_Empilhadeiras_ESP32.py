import torch
import os
import cv2
import requests
import re

# Informe o caminho do melhor modelo do treinamento realizado
# Exemplo: yolov7/runs/train/weights/best.pt
caminho_pesos = "best.pt" # No projeto atual neste repositório o melhor modelo é este informado

modelo = torch.hub.load('WongKinYiu/yolov7', 'custom', caminho_pesos)

# Declaração das Variaveis
CELL_CONFIDENCE = 0.40 # Nível de confiança na detecção do Objeto para a marcação do objeto em tempo real

# Cores das caixas de detecção dos objetos
CELL_BORDER = (0, 0, 255) # Cor da borda para a caixa de detecção do objeto

# Código para solicitar a conexão do ESP32 e validar o IP
def validar_ip(ip):
    """Valida se o endereço IP está em um formato válido."""
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return pattern.match(ip) is not None

def validar_esp32():
    while True:
        se_esp32_conectado = input("Você possui um ESP32 conectado? (SIM/NÃO): ").strip().upper()
        if se_esp32_conectado == "SIM":
            while True:
                esp32_ip = input("Digite o IP do ESP32: ").strip()
                if validar_ip(esp32_ip):
                    print(f"IP válido: {esp32_ip}")
                    
                    # Função usando a biblioteça OpenCV para usar a Webcam na detecção de objetos
                    captura = cv2.VideoCapture(0) 

                    # Loop para detecção de cada frame da Webcam
                    while True:
                        
                        # Capturando o frame
                        ret, frame = captura.read()
                        image = frame.copy()
                        
                        # O while só será interrompido quando a tecla "Q" do teclado for pressionada
                        if cv2.waitKey(1) == ord("q"):
                            break

                        resultado_do_frame = modelo(frame)
                        df = resultado_do_frame.pandas().xyxy[0]
                        
                        table_bboxes = []
                        cell_bboxes = []
                        class_bboxes = []
                        
                        # Salvando as informações da detecção em variáveis
                        for _, row in df.iterrows():
                            
                            if row['class'] == 0 and row['confidence'] > CELL_CONFIDENCE:
                                cell_bboxes.append([int(row['xmin']), int(row['ymin']),
                                                    int(row['xmax']), int(row['ymax']),
                                                    str(row['name']), row['confidence']])
                                class_bboxes.append((row["confidence"], row['name']))
                            
                            # Mostrando uma mensagem se foi detectado o obejto ou não
                            if row['confidence'] > CELL_CONFIDENCE:
                                print('Empilhadeira Detectada')
                                if se_esp32_conectado == "SIM":
                                    ligar_url = f"http://{esp32_ip}/X"
                                    response = requests.get(ligar_url)
                                    print(response.text)
                                else:
                                    print('ESP32 Não conectado')
                            else:
                                print('Nenhuma Empilhadeira Detectada')
                                if se_esp32_conectado == "NÃO":
                                    desligar_url = f"http://{esp32_ip}/Y"
                                    response = requests.get(desligar_url)
                                    print(response.text)
                                else:
                                    print('ESP32 Não conectado')

                        # Criando os Retangulos e Porcentagem de Confiança, quando o objeto é detectado
                        for cell_bbox in cell_bboxes:
                                        
                            # Desenhando o Retangulo
                            cv2.rectangle(image, (cell_bbox[0], cell_bbox[1]),
                                        (cell_bbox[2], cell_bbox[3]), CELL_BORDER, 1)

                            # Informando o nível de Confiança
                            text = str(round(cell_bbox[5], 2)) + " " + str(cell_bbox[4])
                            cv2.putText(image, text , (cell_bbox[0] , cell_bbox[1] - 5),
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)

                        cv2.imshow('frame', image)

                    captura.release()
                    cv2.destroyAllWindows()
                    break
                else:
                    print("IP inválido. Por favor, digite um IP válido.")
            break
        elif se_esp32_conectado == "NÃO":
            print("Por favor, conecte um ESP32 antes de continuar.")
            break
        else:
            print("Resposta inválida. Digite 'SIM' ou 'NÃO'.")

# Descomentar para executar
validar_esp32()

