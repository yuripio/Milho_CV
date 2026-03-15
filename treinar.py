from ultralytics import YOLO

model = YOLO('yolo11n.pt')

caminho_yaml = 'dataset_espigas/data.yaml'

print("Iniciando o treinamento no processador...")

# Rodando direto na CPU
resultados = model.train(data=caminho_yaml, epochs=50, imgsz=640, device='cpu')

print("Treinamento concluido com sucesso,")