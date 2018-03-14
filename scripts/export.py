import numpy as np
import cv2
from fpdf import FPDF
import os, sys

fh = open("C:/Users/DM/Documents/Vook/img.txt", "r")
img = fh.readlines()
fh.close()
fh = open("C:/Users/DM/Documents/Vook/caption.txt", "r")
txt = fh.readlines()
fh.close()

counter = 0
for i in range(len(img)):
    img[i] = img[i].replace("\n", "")
    txt[i] = txt[i].replace("\n", "")
    frame = cv2.imread("C:/Users/DM/Documents/Vook/frames/"+img[i]+".jpg")

    shape_frame = list(frame.shape)
    shape_frame[0] -= 250
    shape_frame = tuple(shape_frame)

    # Create a black image
    image = np.zeros(shape_frame, np.uint8)

    # Write some Text
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, txt[i] ,(40,50), font, 0.5,(255,255,255),1)


    h1, w1 = frame.shape[:2]
    h2, w2 = image.shape[:2]

    vis = np.zeros((h1+h2, max(w1,w2) ,3), np.uint8)

    vis[:h1, :w1,:3] = frame
    vis[h1:h1+h2, :w2,:3] = image

    #Save image
    cv2.imwrite("C:/Users/DM/Documents/Vook/result/" + str(counter) + ".jpg", vis)
    counter += 1
        
path = 'C:/Users/DM/Documents/Vook/result/'
dirs = os.listdir(path)
pdf = FPDF()

# imagelist is the list with all image filenames
for image in dirs:
    pdf.add_page(orientation='L')
    pdf.image(path + image)
pdf.output("C:/Users/DM/Desktop/Vook.pdf", "F")
