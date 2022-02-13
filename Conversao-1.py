import cv2
import io
from pytesseract import pytesseract
from pytesseract import Output
from spellchecker import SpellChecker

# muda a cor da imagem para escala de cinza
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.int8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.int8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return image


def procuraArquivo(palavra):
    file1 = io.open("arquivo.txt", "r", encoding="utf8")
    global achei
    global disciplina

    for line in file1:

        if palavra.lower().strip() == line.lower().strip():
            achei = 1
            break

    if achei == 1:
        disciplina = '' + line
    file1.close()


achei = 0
disciplina = ''

portuguese = SpellChecker(language='pt')

pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# psm: afeta como o Tesseract divide a imagem em linhas de texto e palavras.
# 6: Suponha um único bloco uniforme de texto
custom_config = r'-l por --psm 6'

img = cv2.imread("img/aula_sociologia.png")

gray_image = grayscale(img)

# binarização
thresh, im_bw = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

# image_data: inclui palavras com suas correspondentes largura, altura e coordenadas x, y
# output_type=Output.DIC: output_type especifica o tipo de saída, nesse caso pares chave-valor.
image_data = pytesseract.image_to_data(im_bw, config=custom_config, output_type=Output.DICT)

# método responsável por identificar as palavras no documento de texto
# é realizado uma iteração por cada palavra obedecendo as condições abaixo
# word != '' and flag == 0

# left é a distância do canto superior esquerdo da caixa delimitadora até a borda esquerda da imagem (todas as coodernadas X)
# top é a distância do canto superior esquerdo da caixa delimitadora até a borda superior da imagem
# width e height são a largura e a altura da caixa delimitadora

for i, palavra in enumerate(image_data['text']):
    if palavra != '' and achei == 0:
        x, y, w, h = image_data['left'][i], image_data['top'][i], image_data['width'][i], image_data['height'][i]
        cv2.rectangle(im_bw, (x, y), (x + w, y + h), (0, 255, 0), 3) # x e y são as coordenadas
        cv2.putText(im_bw, portuguese.correction(palavra), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        print('Posição:',i, ',Palavra:', portuguese.correction(palavra))
        procuraArquivo(portuguese.correction(palavra))

cv2.imshow("window", im_bw)
print('Disciplina:', disciplina)
cv2.waitKey(0)
