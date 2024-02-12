# Forklift Detection Using YOLO

Este trabalho teve como propósito a criação de um modelo de detecção de empilhadeiras com um sistema de iluminação integrado usando ESP32.

## Clonando o Repositório

```javascript
git clone --depth=1 https://github.com/evertonrafael/forklift-detection-using-yolo
```

### Características

- Projeto de conclusão de curso: Ciencia de Dados - FACENS - Sorocaba/SP
- Detecção de Objetos
- Identificar Empilhadeiras em Tempo Real
- Previvir possíveis acidentes com empilhadeiras em uso

### Pré-requisitos

- Python: https://www.python.org/downloads/
- Consultar arquivo "requirements.txt"


### Instalação das bibliotecas
Python: Faça o download do Python na sua maquina e instale normalmente.

Execute o comando para baixar todas as bibliotecas necessárias:
```javascript
pip install -r requirements.txt
```

## Desenvolvimento

Faça a instalação de todas as bibliotecas necessárias. Assim será possível rodar o projeto.

## Rodando o projeto

### best.pt

Este é o modelo treinado pela equipe deste projeto, com a melhor performance para detecção das empilhadeiras.

### Detectar_Empilhadeiras.py

Script para rodar o algoritmo de detecção das empilhadeiras, já com o modelo treinado deste projeto.

### Sistema_Iluminacao_ESP32.ino

Este é o arquivo que deve ser compilado no ESP32. Script responsável para fazer a comunicação entre a detecção das empilhadeiras com o sistema luminoso.

- 1 - Conecte o ESP32 no USB
- 2 - Abra o programa [Arduino IDE](https://www.arduino.cc/en/software)
- 3 - Abra o arquivo "Sistema_Iluminacao_ESP32.ino", na linha 19, digite o nome da rede que será usada, e a senha da mesma rede, na linha 20.
- 4 - No Arduino IDE, clique em verificar o código e depois, clique em upload.
- 5 - No momento que estiver realizado o upload, clique no botão boot do arduino.
- 6 - Após finalizar o upload e o boot, no Arduino IDE, abra a ferramenta Serial Monitor.
- 7 - No ESP32, aperte o botão Reset
- 8 - No Serial Monitor, aparecerá o IP do ESP32 (Veja o exemplo abaixo) que será usado no arquivo "Detectar_Empilhadeiras_ESP32.py".


WiFi connected.
IP address: 
000.000.0.00


### Detectar_Empilhadeiras_ESP32.py

Script para rodar o algoritmo de detecção das empilhadeiras usando o ESP32 para acionar o sistema luminoso, já com o modelo treinado deste projeto.

### Executar_Treinamento.py

Script para criar o próprio modelo, utilizando YOLOv7, Roboflow e os hiperparâmetros de treinamento.

## Construído com

- [Python](https://www.python.org/) - Linguagem de Programação
- [YOLOv7](https://github.com/WongKinYiu/yolov7) - Official YOLOv7
- [Roboflow](https://roboflow.com/) - Criação de Dataset para imagens e Data Augmentation

## Autores

- **Everton Rafael** - [evertonrafael](https://github.com/evertonrafael)
- **Felipe Soflasio** - [FilipeData](https://github.com/FilipeData)
- **Lais Lins** - [laislins](https://github.com/laislins)