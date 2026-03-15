import cv2
from ultralytics import YOLO

# 1. Carrega o seu modelo treinado
model = YOLO('runs/detect/train/weights/best.pt')

# 2. Carrega o video original
nome_do_video = 'video_milho.mp4'
cap = cv2.VideoCapture(nome_do_video)

# 3. Define o tempo de corte em segundos
inicio_segundos = (4 * 60) + 30
fim_segundos = (5 * 60) + 30

# Pega as informacoes do video original
fps = cap.get(cv2.CAP_PROP_FPS)
largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Calcula os frames e pula direto para o inicio do trecho
frame_inicial = int(inicio_segundos * fps)
frame_final = int(fim_segundos * fps)
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_inicial)

# 4. Prepara o arquivo para salvar o video final
# O formato mp4v costuma ser o mais compativel com o Windows
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
saida_video = cv2.VideoWriter('resultado_apresentacao.mp4', fourcc, fps, (largura, altura))

print("Iniciando a deteccao e gravando o video da apresentacao...")

frame_atual = frame_inicial

while cap.isOpened() and frame_atual <= frame_final:
    success, frame = cap.read()
    
    if success:
        # Roda o modelo
        resultados = model(frame, conf=0.2)
        
        # Desenha os quadradinhos
        frame_anotado = resultados[0].plot(line_width= 2, font_size = 1, labels=False)

        # Mostra na tela para voce ir acompanhando o progresso
        cv2.imshow("Processando Esteira", frame_anotado)
        
        # Salva o frame processado no novo arquivo de video
        saida_video.write(frame_anotado)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
        
    frame_atual += 1

# Limpa a memoria e finaliza as gravacoes
cap.release()
saida_video.release()
cv2.destroyAllWindows()

print("Show! Video salvo com sucesso como resultado_apresentacao.mp4 na sua pasta,")