import cv2
import numpy as np
import io
from pytesseract import pytesseract
from pytesseract import Output
from spellchecker import SpellChecker

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

custom_config = r'-l por --psm 6'

img = cv2.imread("img/biologia.png")

# converte a imagem para escala de cinza
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# limiar imagem
thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

# aplicar morfologia para limpar pequenas regiões brancas ou pretas
kernel = np.ones((5,5), np.uint8)
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

# região fina para remover o excesso de borda preta
kernel = np.ones((3,3), np.uint8)
morph = cv2.morphologyEx(morph, cv2.MORPH_ERODE, kernel)

image_data = pytesseract.image_to_data(morph, config=custom_config, output_type=Output.DICT)

for i, palavra in enumerate(image_data['text']):
    if palavra != '' and achei == 0:
        x, y, w, h = image_data['left'][i], image_data['top'][i], image_data['width'][i], image_data['height'][i]
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(img, portuguese.correction(palavra), (x, y+140), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        print('Posição:',i, ',Palavra', portuguese.correction(palavra))
        procuraArquivo(portuguese.correction(palavra))

cv2.imshow("window", img)
print('Disciplina:', disciplina)
cv2.waitKey(0)
