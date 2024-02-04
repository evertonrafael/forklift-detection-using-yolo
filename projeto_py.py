import torch
import os
import cv2
import requests

caminho_pesos = "best.pt"

model = torch.hub.load('WongKinYiu/yolov7', 'custom', caminho_pesos)
                        #force_reload=True, trust_repo=True)

# Declaração das Variaveis
TABLE_CONFIDENCE = 0.40
CELL_CONFIDENCE = 0.40
OUTPUT_DIR = "/content"

# Cores das caixas de detecção dos objetos
ALPHA = 0.2
TABLE_BORDER = (0, 0, 255)
CELL_FILL = (0, 0, 200)
CELL_BORDER = (0, 0, 255)

#Conexão com o ESP32 - Defina o endereço IP da rede
#esp32_ip = "192.168.0.11"

cap = cv2.VideoCapture(0)
while True:

    ret, frame = cap.read()
    
    image = frame.copy()

    #cv2.imshow('frame', image)

    if cv2.waitKey(1) == ord("q"):
        break

    results = model(frame)
    df = results.pandas().xyxy[0]
    table_bboxes = []
    cell_bboxes = []
    class_bboxes = []
    for _, row in df.iterrows():
        if row['class'] == 0 and row['confidence'] > TABLE_CONFIDENCE:
            table_bboxes.append([int(row['xmin']), int(row['ymin']),
                                int(row['xmax']), int(row['ymax'])])

        if row['class'] == 0 and row['confidence'] > CELL_CONFIDENCE:
            cell_bboxes.append([int(row['xmin']), int(row['ymin']),
                                int(row['xmax']), int(row['ymax']),
                                str(row['name']), row['confidence']])
            class_bboxes.append((row["confidence"], row['name']))
        if row['confidence'] > CELL_CONFIDENCE:
            print('empilhadeira detectada')
        #    ligar_url = f"http://{esp32_ip}/X"
        #    response = requests.get(ligar_url)
        #    print(response.text)
        else:
            print('sem empilhadeira')
        #    desligar_url = f"http://{esp32_ip}/Y"
        #    response = requests.get(desligar_url)
        #    print(response.text)




    #image = cv2.imread(frame)
    #image = frame.copy()

    #cv2.imshow('frame', image)

    #overlay = image.copy()
    #for table_bbox in table_bboxes:
        #cv2.rectangle(image, (table_bbox[0], table_bbox[1]),
                    #(table_bbox[2], table_bbox[3]), TABLE_BORDER, 1)

    for cell_bbox in cell_bboxes:
    #   cv2.rectangle(overlay, (cell_bbox[0], cell_bbox[1]),
                    #(cell_bbox[2], cell_bbox[3]), CELL_FILL, -1)
        cv2.rectangle(image, (cell_bbox[0], cell_bbox[1]),
                    (cell_bbox[2], cell_bbox[3]), CELL_BORDER, 1)

        text = str(round(cell_bbox[5], 2)) + " " + str(cell_bbox[4])

        cv2.putText(image, text , (cell_bbox[0] , cell_bbox[1] - 5),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)

    cv2.imshow('frame', image)

cap.release()
cv2.destroyAllWindows()