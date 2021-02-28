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
 
# Getting text from image
res = tool.image_to_string(Image.open("./images/bsp2_2.tif"),lang="jpn_vert", builder=pyocr.builders.LineBoxBuilder(tesseract_layout=5))

# Show the recognized text
print(res)
 
# Checking the recognized areas
out = cv2.imread("./images/bsp2_2.tif")
orgHeight, orgWidth = out.shape[0], out.shape[1]
size = (orgWidth//2, orgHeight//2)
 
for d in res:
    print(d.content) # which character is recognized?
    print(d.position) # which area are targeted?
    cv2.rectangle(out, d.position[0], d.position[1], (0, 0, 255), 2) # create red boxes for the recognized areas
 
# Show the image with boxes
img_resize = cv2.resize(out, size) 
cv2.imwrite("./images/test/testres_bsp2_2.jpg", img_resize)