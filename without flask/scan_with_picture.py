from pyzbar import pyzbar
import argparse
import cv2 as cv
import time
import datetime
import winsound

frequency = 2500
duration = 1000

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes_image.csv",
                help="Path to output csv file")
args = vars(ap.parse_args())

image = cv.imread("2.jpg")  # reading through image

csv = open(args["output"], "w")
found = set()

barcodes = pyzbar.decode(image)

for barcode in barcodes:
    (x, y, w, h) = barcode.rect
    cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type

    text = "{} ({})".format(barcodeData, barcodeType)
    cv.putText(image, text, (x, y - 10),
                cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    if barcodeData not in found:
        csv.write("{},{}\n".format(datetime.datetime.now(), barcodeData))
        csv.flush()
        found.add(barcodeData)
        winsound.Beep(frequency, duration)
    print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

csv.close()
cv.imshow("Image", image)
cv.waitKey(0)
