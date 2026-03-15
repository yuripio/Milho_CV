import json
import os
import glob

pasta_alvo = "dataset_espigas"
caminho_busca = f"{pasta_alvo}/*.json"
arquivos_json = glob.glob(caminho_busca)

if not arquivos_json:
    print(f"Erro: Nao achei o JSON na pasta {pasta_alvo},")
else:
    arquivo_json = arquivos_json[0]
    print(f"Achei o arquivo: {arquivo_json}")
    
    with open(arquivo_json, 'r') as f:
        dados = json.load(f)
        
    quantidade_imagens = len(dados.get('images', []))
    quantidade_anotacoes = len(dados.get('annotations', []))
    
    print(f"O JSON tem {quantidade_imagens} imagens e {quantidade_anotacoes} anotacoes,")
    
    if quantidade_anotacoes == 0:
        print("Problema: O Roboflow baixou o JSON vazio sem as coordenadas das espigas,")
    else:
        mapa_imagens = {img['id']: img for img in dados['images']}
        arquivos_gerados = 0

        for ann in dados['annotations']:
            img_id = ann['image_id']
            img_info = mapa_imagens[img_id]

            # Converte as dimensoes da imagem para numero real (float)
            w_img = float(img_info['width'])
            h_img = float(img_info['height'])
            
            nome_arquivo = os.path.basename(img_info['file_name'])

            # Converte todas as coordenadas do bounding box para numero real (float)
            x_min, y_min, w_box, h_box = map(float, ann['bbox'])

            x_centro = (x_min + w_box / 2) / w_img
            y_centro = (y_min + h_box / 2) / h_img
            w_norm = w_box / w_img
            h_norm = h_box / h_img

            nome_txt = os.path.splitext(nome_arquivo)[0] + '.txt'
            caminho_salvar = os.path.join(pasta_alvo, nome_txt)

            with open(caminho_salvar, 'a') as f_txt:
                f_txt.write(f"0 {x_centro} {y_centro} {w_norm} {h_norm}\n")
            
            arquivos_gerados += 1

        print(f"Sucesso real! {arquivos_gerados} linhas de coordenadas foram salvas nos txt,")