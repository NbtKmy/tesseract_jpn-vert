import pyocr
import pyocr.builders
import cv2
from PIL import Image
import sys

# Getting ocr tool
tools = pyocr.get_available_tools()
 
if len(tools) == 0:
    print("No OCR software found")
    sys.exit(1)
 
# Ocr[0] = tesseract
tool = tools[0]

# Zeile für Zeile lesen und daraus einen Text erstellen
res_tex = ""
for image_num in range(19):
    # Getting text from image
	# jpn_vert2 muss noch einmal trainiert werden - wegen der Fehlermeldung 'Failed to load any lstm-specific dictionaries for lang jpn_vert2!!'
	# siehe https://github.com/tesseract-ocr/tesstrain/issues/28 - dennoch funtioniert über command line
    res = tool.image_to_string(Image.open('./Vorarbeiten/line_output/line_{}.tif'.format(image_num)), lang='jpn_vert2', builder=pyocr.builders.TextBuilder(tesseract_layout=5))
    res_tex = '\n'.join(res)

print(res_tex)
# Output
# with open('./results/last_result/res_bsp1_2.txt', mode='w') as f:
#    f.write(res_tex)


