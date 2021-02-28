from PIL import Image, ImageDraw, ImageFont

# Textdatei holen
with open('./traindata/training_bs.txt') as f:
    txt = f.read()

# Textzeile werden in List-datei gesplittet
    lines = txt.splitlines()
# Hier werden nur 100 Zeilen berücksichtigt
    for l in range(100):


        # Canvas erstellen
        bg = Image.new('RGB', (100, 2500), (255,255,255))

        # Font holen
        fnt = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc', 50)
        # Zeile auf dem Canvas schreiben
        d = ImageDraw.Draw(bg)
        d.text((25,30), lines[l], fill=(0,0,0), font=fnt, features=['kern', 'palt'], direction='ttb', language='ja')

        
        path1 = './traindata/txt/'
        path2 = './traindata/img/'

        # Textzeile speichern
        txName = str(l+1) + '.gt.txt'

        with open(path1+txName, 'w') as f:
            print(lines[l], file=f)

        # Image speichern
        imName = str(l+1) + '.tif'
        bg.save(path2+imName)
