from pdf2image import convert_from_path
import os
import cv2
# Load image, convert to grayscale, Otsu's threshold
import numpy as np
from matplotlib import pyplot as plt
plt.rcParams["figure.figsize"] = (50,50)

sheet_Directory = "code/music_sheet"
files = os.listdir(sheet_Directory)
files = [f for f in files if os.path.isfile(sheet_Directory+'/'+f)]

image_Directory = 'code/images'
img_files = os.listdir(image_Directory)
img_files = [f for f in img_files if os.path.isfile(image_Directory+'/'+f)]


bar_Directory = 'code/temp/bar_img'
bar_files = os.listdir(bar_Directory)
bar_files = [f for f in bar_files if os.path.isfile(bar_Directory+'/'+f)]
bar_files.sort()

### PDF Conversion Functions ####

def task(pdf_path):
    print(pdf_path)
    images = convert_from_path(pdf_path)
    for index, image in enumerate(images):
        image.save(f'images/{pdf_path[12:]}-{index}.png')


def convert_pdf_to_images():
    for elem in files:
        if (elem[-4:] == ".pdf"):
            task(sheet_Directory + '/' + elem)

### Extract Bars ####
def process_counter_point(c):
    if (len(c) == 2):
        x1 = c[0][0][0]
        y1 = c[0][0][1]
        x2 = c[1][0][0]
        y2 = c[1][0][1]
        pty = (y1 + y2)//2
        return c, np.array([[x1, pty], [x2, pty]])
    else:
        pty = (c[0][0][1] + c[1][0][1] + c[2][0][1] + c[3][0][1]) // 4
        x1 = (c[0][0][0] + c[1][0][0]) // 2
        x2 = (c[2][0][0] + c[3][0][0]) // 2
        return c,  np.array([[x1, pty], [x2, pty]])


def extract_bars():
    for k, img in enumerate(img_files):
        ### Read sheet image and do Thresholding ####
        if (img[-4:] != ".png"):
            continue
        image = cv2.imread(image_Directory + "/" +img)
        result = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        cv2.imwrite("temp/del/threshold_sheet_"+ str(k) +".png", thresh)

        ### Detect horizantal Line ###
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (400, 1))
        detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        pts_list = list()
        for c in cnts:
            c, pts = process_counter_point(c)
            cv2.drawContours(result, [c], -1, (36, 255, 12), 1)
            result = cv2.circle(result, pts[0], 3, (0, 0, 255), -1)
            result = cv2.circle(result, pts[1], 3, (0, 0, 255), -1)
            pts_list.append(pts)

        cv2.imwrite("temp/del/Lines_on_sheet_" + str(k) + ".png", result)

        pts_list.reverse()
        total_bar = int(len(pts_list) / 10)

        ## cropping
        bar_imgs = list()
        for i in range(total_bar):
            y1 = pts_list[10 * i][0][0]
            y2 = pts_list[10 * i + 9][1][0]
            x1 = pts_list[10 * i][0][1]
            # x2 = pts_list[10*i][0][1] + (pts_list[10*i + 9][0][1] - pts_list[10*i][0][1])//2

            diff = (pts_list[10 * i + 4][0][1] - pts_list[10 * i][0][1]) // 4
            x2 = pts_list[10 * i + 4][0][1] + 2 * diff

            img_thresh = thresh[x1:x2, y1:y2]
            filename = "temp/bar_img/bar_" + str(k)+ "_" + str(i + 1) + ".png"
            bar_imgs.append(img_thresh)
            cv2.imwrite(filename, img_thresh)

### Detect Notes ####
def identify_note(x, h):
    #print(x,h)
    x = h - x
    buffer = 0.1
    delta = h/6
    var = x/delta

    if var <= 1:
        var = var
        if(var < buffer):
            return "A"
        elif(var<1-buffer):
            return "B"
        else:
            return "C"

    elif var <= 2:
        var = var -1
        if(var < buffer):
            return "C"
        elif(var<1-buffer):
            return "D"
        else:
            return "E"
    elif var <= 3:
        var = var - 2
        if (var < buffer):
            return "E"
        elif (var < 1 - buffer):
            return "F"
        else:
            return "G"

    elif var <= 4:
        var = var - 3
        if (var < buffer):
            return "G"
        elif (var < 1 - buffer):
            return "A"
        else:
            return "B"
    elif var <= 5:
        var = var - 4
        if (var < buffer):
            return "B"
        elif (var < 1 - buffer):
            return "C"
        else:
            return "D"
    elif var <= 6:
        var = var - 5
        if (var < buffer):
            return "D"
        elif (var < 1 - buffer):
            return "E"
        else:
            return "F"
    return "O"

def closest_point(elem, note_location1):
    min = 10000000
    point = [0,0]
    for pts in note_location1:
        temp = np.sqrt( (elem[1] - pts[1])**2 + (elem[0] - pts[0])**2)
        if (temp < min):
            min = temp
            point = pts
    if(min > 20):
        return [-1,-1]
    else:
        return point
def detect_notes():
    ttl = 0
    notes = list()
    for filename in bar_files:
        if (filename[-4:] != ".png"):
            continue
        ttl += 1
        image_orig = cv2.imread(bar_Directory+'/' + filename)
        image = cv2.cvtColor(image_orig, cv2.COLOR_BGR2GRAY)

        ### First set of filters
        kernel = np.ones((5, 5), np.float32) / 25
        dst = cv2.erode(image, kernel)

        kernel = np.ones((7, 7), np.float32) / 49
        dst1 = cv2.erode(dst, kernel)

        kernel = np.ones((2, 2), np.float32) / 25
        dst2 = cv2.dilate(dst1, kernel)

        x, y = dst2.shape
        note_location1 = list()
        prev_loc = 20
        for i in range(y):
            if (any(dst2[:, i])):
                if (i - prev_loc > 50):
                    note_location1.append([min(list(np.where(dst2[:, i] == 255))[0]), i])
                    prev_loc = i

        ### second set of filters
        kernel = np.ones((2, 2), np.float32) / 4
        dst = cv2.dilate(image, kernel, iterations=5)

        kernel = np.ones((3, 3), np.float32) / 9
        dst1 = cv2.erode(dst, kernel, iterations=4)

        kernel = np.ones((3, 3), np.float32) / 9
        dst2 = cv2.dilate(dst1, kernel, iterations=3)

        kernel = np.ones((2, 2), np.float32) / 4
        dst3 = cv2.erode(dst2, kernel, iterations=2)

        kernel = np.ones((3, 3), np.float32) / 9
        dst4 = cv2.erode(dst3, kernel)

        x, y = dst4.shape

        note_location2 = list()
        prev_loc = 50

        for i in range(y):
            if (any(dst4[5:, i])):
                if (len(list(np.where(dst4[:, i] == 255))) < 16):
                    if (i - prev_loc > 50):
                        note_location2.append([min(list(np.where(dst4[5:, i] == 255))[0]), i])
                        prev_loc = i


        for elem in note_location2: ## going through full note filter list
            # print((elem[0] , elem[1]))
            pt = closest_point(elem, note_location1)

            if(pt[0] == -1): ## full note
                h,w = image.shape
                note = identify_note( elem[0], h)
                cv2.circle(image_orig, (elem[1], elem[0]), 3, (255, 0, 125), -1)
                image_orig = cv2.putText(image_orig, note, (elem[1], elem[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                         (0, 0, 255), 1, cv2.LINE_AA)
                if (note == "E"):
                    note = "D"
                if(note == "D"):
                    note = "C"
                notes.append([note,"f"])
            else:
                elem = pt
                h, w = image.shape
                note = identify_note(elem[0], h)
                cv2.circle(image_orig, (elem[1], elem[0]), 3, (255, 0, 125), -1)
                image_orig = cv2.putText(image_orig, note, (elem[1], elem[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                         (0, 0, 255), 1, cv2.LINE_AA)
                notes.append([note,"h"])
        cv2.imwrite("temp/detected/" + str(ttl) +filename , image_orig)
    return notes
if __name__ == "__main__":
    pass