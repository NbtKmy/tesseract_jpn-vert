import pyocr
import pyocr.builders
import cv2
from PIL import Image
import sys
import argparse


parser = argparse.ArgumentParser(description='tesseract-ocr for jpn_vert')
parser.add_argument('input', help='Name of original image')
parser.add_argument('output', help='Name of output image')
parser.add_argument('-l', '--lang', default='jpn_vert')
args = parser.parse_args() 



# Getting ocr tool
tools = pyocr.get_available_tools()
 
if len(tools) == 0:
    print("No OCR software found")
    sys.exit(1)
 
# Ocr[0] = tesseract
tool = tools[0]
 
# Getting text from image
res = tool.image_to_string(Image.open(args.input),lang=args.lang, builder=pyocr.builders.LineBoxBuilder(tesseract_layout=5))

# Show the recognized text
print(res)
 
# Checking the recognized areas
out = cv2.imread(args.input)
orgHeight, orgWidth = out.shape[0], out.shape[1]
size = (orgWidth//2, orgHeight//2)
 
for d in res:
    print(d.content) # which character is recognized?
    print(d.position) # which area are targeted?
    cv2.rectangle(out, d.position[0], d.position[1], (0, 0, 255), 2) # create red boxes for the recognized areas
 
# Show the image with boxes
img_resize = cv2.resize(out, size) 
cv2.imwrite(args.output, img_resize)