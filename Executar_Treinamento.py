import torch
import os
import cv2
import requests
import subprocess
import roboflow

# Clonar o repositório do YOLOv7
subprocess.run(['git', 'clone', 'https://github.com/augmentedstartups/yolov7.git'], check=True)
# Mudar o diretório de trabalho para o repositório clonado do YOLOv7
os.chdir('yolov7')
# Instalar as dependências necessárias a partir de requirements.txt
subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)

from roboflow import Roboflow
# Substitua "your_api_key" pela sua chave de API real do Roboflow
chave_api = "exemplo-chave-api"
nome_espaco_trabalho = "exemplo-nome-espaco-trabalho"  # Substitua pelo nome do seu workspace no Roboflow
nome_projeto = "exemplo-nome-projeto"  # Substitua pelo nome do seu projeto no Roboflow
numero_versao = 1  # Substitua pelo número da versão do seu dataset que deseja baixar

rf = Roboflow(api_key=chave_api)
project = rf.workspace(nome_espaco_trabalho).project(nome_projeto)
dataset = project.version(numero_versao).download("yolov7")

caminho_diretorio_atual = os.getcwd()
os.chdir(caminho_diretorio_atual)

url_arquivo_yolov7 = "https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt"
diretorio_salvar = caminho_diretorio_atual
file_path = os.path.join(diretorio_salvar, "yolov7.pt")

resposta = requests.get(url_arquivo_yolov7)
with open(file_path, 'wb') as file:
    file.write(resposta.content)

# Definir os hiperparâmetros do treinamento
batch = 16
epochs = 55
comando_treino = f'python train.py --batch {batch} --cfg cfg/training/yolov7.yaml --epochs {epochs} --data {nome_projeto}/data.yaml --weights yolov7.pt'

# Executar o comando de treinamento
try:
    subprocess.run(comando_treino, check=True)
    print("Treinamento concluído com sucesso.")
except subprocess.CalledProcessError as e:
    print(f"Erro durante o treinamento: {e}")

#Executar o comando de detecção na pasta de test

# Nível de confiança para a detecção
confianca = "0.1"
# Fonte das imagens para detecção
caminho_fonte_imagens = f"yolov7/{nome_projeto}/test/images"
caminho_pesos = "yolov7/runs/train/weights/best.pt"
comando_deteccao = f'detect.py --weights {caminho_pesos} --conf {confianca} --source {caminho_fonte_imagens}'

# Executar o comando de detecção
try:
    subprocess.run(comando_deteccao, check=True)
    print("Detecção concluída com sucesso.")
except subprocess.CalledProcessError as e:
    print(f"Erro durante a detecção: {e}")