import cv2
import os

pasta_destino = "dataset_espigas"
os.makedirs(pasta_destino, exist_ok=True)

video = cv2.VideoCapture("video_milho.mp4")

# Define o inicio e o fim do corte em segundos
# Exemplo: do minuto 5:00 (300s) ao minuto 7:00 (420s)
tempo_inicio_segundos = 240
tempo_fim_segundos = 360
intervalo_frames = 15

# Calcula em qual frame o video deve comecar e terminar
fps = video.get(cv2.CAP_PROP_FPS)
frame_inicial = int(tempo_inicio_segundos * fps)
frame_final = int(tempo_fim_segundos * fps)

# Pula direto para o frame inicial
video.set(cv2.CAP_PROP_POS_FRAMES, frame_inicial)

frame_atual = frame_inicial
fotos_salvas = 0

while video.isOpened() and frame_atual <= frame_final:
    retorno, frame = video.read()
    
    if not retorno:
        break
        
    if frame_atual % intervalo_frames == 0:
        nome_imagem = f"{pasta_destino}/espiga_{fotos_salvas}.jpg"
        cv2.imwrite(nome_imagem, frame)
        fotos_salvas += 1
        
    frame_atual += 1

video.release()
print(f"Sucesso! {fotos_salvas} fotos extraídas do trecho escolhido,")