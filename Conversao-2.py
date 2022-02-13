import cv2
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

img = cv2.imread("img/matematica.png")

image_data = pytesseract.image_to_data(img, config=custom_config, output_type=Output.DICT)

for i, palavra in enumerate(image_data['text']):
    if palavra != '' and achei == 0:
        x, y, w, h = image_data['left'][i], image_data['top'][i], image_data['width'][i], image_data['height'][i]
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(img, portuguese.correction(palavra), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        print('Posição:',i, ',Palavra:', portuguese.correction(palavra))
        procuraArquivo(portuguese.correction(palavra))

cv2.imshow("window", img)
print('Disciplina:', disciplina)
cv2.waitKey(0)
