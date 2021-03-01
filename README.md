# tesseract_jpn-vert

## Für dieses Repository braucht man folgende Libraries und Software...

### Python Libraries
* Pillow
* Pyocr
* OpenCV
* Urllib (Nur für die Erstellung der Schriftzeichentabelle)

### Software
* Tesseract (>=4)
* tessdata - jpn_vert


## Anwendung von ocr_tess.py
`$ python ocr_tess.py [input file name] [output file name] [-l jpn_vert2 (Default-Wert jpn_vert)]`

## Ordner
* Der Ordner "images" enthält original Bilder
* Der Ordner "results" enthält Ergebnisse des OCR-Verfahrens (Bilder und Texte)
* Der Ordner "traindata" enthält die Daten, mit denen man tesseract trainiert hat
* Der Ordner "trained_jpn-vert" enthält das trainierte Modell 
* Der Ordner "Vorarbeiten" enthält Python-Codes, mit denen man die Vor-Prozess der OCR ausführt

## Training mit Tesstrain
Für das Training wurde [tesstrain](https://github.com/tesseract-ocr/tesstrain) verwendet. 
So wie in README von tesstrain steht, wurde zuerst "tesseract built with the training tools and matching leptonica bindings" installiert.
Tesstrain braucht noch folgende Python Libraries:

* Pillow>=6.2.1
* python-bidi>=0.4
* matplotlib
* pandas

Das Repo tesstrain clonen:

`$ git clone https://github.com/tesseract-ocr/tesstrain.git`

...und nach der Erläuterung von tesstrain packt man die div. Daten unter dem tesstrain-Ordner:

* Start-Modell, das fine getunt werden soll, unter ./usr/share/tessdata/
* Ground-Truth-Daten (Texte und Image) unter ./data/[Name des Modells]-ground-truth

Dann unter dem Ordner tesstrain den Befehl eingeben:

`$ nohup time -f "Run time = %E\n" make training MODEL_NAME=jpn_vert START_MODEL=jpn_vert PSM=5 >> train.log 2>&1 &`

PSM=5 ist für jpn_vert notwendig...

Um die log-Daten zu checken

`$ tail -f train.log`
