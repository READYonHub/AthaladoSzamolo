import numpy as np
import cv2 as cv
import Person
import time

# Naplófájl megnyitása írásra
log = open('log.txt', "w")

# Be- és kilépési számlálók
cnt_up = 0
cnt_down = 0

# Videó forrás (előre definiált videó)
# cap = cv.VideoCapture(0)  # Kamera használata
cap = cv.VideoCapture('testVideo.mp4')

h = int(cap.get(4))
w = int(cap.get(3))
felvetelArea = h * w
areaTH = felvetelArea / 250
print('Szurt területe', areaTH)

# Up/Down vonalak
line_up = int(2 * (h / 5))
line_down = int(3 * (h / 5))

up_limit = int(1 * (h / 5))
down_limit = int(4 * (h / 5))

print("Piros vonal y:", str(line_down))
print("Kék vonal y:", str(line_up))
line_down_color = (255, 0, 0)
line_up_color = (0, 0, 255)
pt1 = [0, line_down]
pt2 = [w, line_down]
pts_L1 = np.array([pt1, pt2], np.int32)
pts_L1 = pts_L1.reshape((-1, 1, 2))
pt3 = [0, line_up]
pt4 = [w, line_up]
pts_L2 = np.array([pt3, pt4], np.int32)
pts_L2 = pts_L2.reshape((-1, 1, 2))

pt5 = [0, up_limit]
pt6 = [w, up_limit]
pts_L3 = np.array([pt5, pt6], np.int32)
pts_L3 = pts_L3.reshape((-1, 1, 2))
pt7 = [0, down_limit]
pt8 = [w, down_limit]
pts_L4 = np.array([pt7, pt8], np.int32)
pts_L4 = pts_L4.reshape((-1, 1, 2))

# Háttér szűrés árnyékok szerint
fgbg = cv.createBackgroundSubtractorMOG2(detectShadows=True)

# MOG árnyék szűrés
kernelOp = np.ones((3, 3), np.uint8)
kernelOp2 = np.ones((5, 5), np.uint8)
kernelCl = np.ones((11, 11), np.uint8)

font = cv.FONT_HERSHEY_SIMPLEX
persons = []
max_p_age = 5
pid = 1

while(cap.isOpened()):
    ret, felvetel = cap.read()

    for i in persons:
        i.age_one()

    # Háttér leválasztás az emberektől
    fgmaszk = fgbg.apply(felvetel)
    fgmaszk2 = fgbg.apply(felvetel)

    # Árnyékok eltüntetése
    try:
        ret, imBin = cv.threshold(fgmaszk, 200, 255, cv.THRESH_BINARY)
        ret, imBin2 = cv.threshold(fgmaszk2, 200, 255, cv.THRESH_BINARY)
        # Nyitás (erode->dilate) a zaj eltávolításához.
        maszk = cv.morphologyEx(imBin, cv.MORPH_OPEN, kernelOp)
        maszk2 = cv.morphologyEx(imBin2, cv.MORPH_OPEN, kernelOp)
        # Zárás (dilate -> erode) a fehér területek összekapcsolásához.
        maszk = cv.morphologyEx(maszk, cv.MORPH_CLOSE, kernelCl)
        maszk2 = cv.morphologyEx(maszk2, cv.MORPH_CLOSE, kernelCl)
    except:
        print("\nVege\nosszesen:\nfel: \t"+str(cnt_up)+"\nle: \t"+str(cnt_down))
        
        break

    contours0, hierarchy = cv.findContours(maszk2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours0:
        area = cv.contourArea(cnt)
        if area > areaTH:
            # Követés

            M = cv.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            x, y, w, h = cv.boundingRect(cnt)

            new = True
            
            if cy in range(up_limit, down_limit):
                for i in persons:
                    if abs(x - i.getX()) <= w and abs(y - i.getY()) <= h:
                        new = False
                        i.updateCoords(cx, cy)
                        if i.going_UP(line_down, line_up) == True:
                            cnt_up += 1
                            print("ID:", i.getId(), '\t fel megy \t', time.strftime("%c"))
                            log.write("ID: " + str(i.getId()) + '\t fel megy \t' + time.strftime("%c") + '\n')
                        elif i.going_DOWN(line_down, line_up) == True:
                            cnt_down += 1
                            print("ID:", i.getId(), '\t le megy \t', time.strftime("%c"))
                            log.write("ID: " + str(i.getId()) + '\t le megy \t' + time.strftime("%c") + '\n')
                        break
                    if i.getState() == '1':
                        if i.getDir() == 'le' and i.getY() > down_limit:
                            i.setDone()
                        elif i.getDir() == 'fel' and i.getY() < up_limit:
                            i.setDone()
                    if i.timedOut():
                        index = persons.index(i)
                        persons.pop(index)
                        del i
                if new == True:
                    p = Person.MyPerson(pid, cx, cy, max_p_age)
                    persons.append(p)
                    pid += 1
            cv.circle(felvetel, (cx, cy), 5, (0, 0, 255), -1)
            img = cv.rectangle(felvetel, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #ID kiiratas objektumra
    for i in persons:
        cv.putText(felvetel, str(i.getId()), (i.getX(), i.getY()), font, 0.3, i.getRGB(), 1, cv.LINE_AA)

    #kiiras felvetelre
    str_up = 'Fel: ' + str(cnt_up)
    str_down = 'Le: ' + str(cnt_down)
    
    # le vonal
    felvetel = cv.polylines(felvetel, [pts_L1], False, line_down_color, thickness=2)
    # fel vonal 
    felvetel = cv.polylines(felvetel, [pts_L2], False, line_up_color, thickness=2)
    
    #feher vonal
    felvetel = cv.polylines(felvetel, [pts_L3], False, (255, 255, 255), thickness=1)
    felvetel = cv.polylines(felvetel, [pts_L4], False, (255, 255, 255), thickness=1)
    
    # vonal 
    cv.putText(felvetel, str_up, (10, 40), font, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(felvetel, str_up, (10, 40), font, 0.5, (0, 0, 255), 1, cv.LINE_AA)
    cv.putText(felvetel, str_down, (10, 90), font, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(felvetel, str_down, (10, 90), font, 0.5, (255, 0, 0), 1, cv.LINE_AA)



    cv.imshow('felvetel', felvetel)
    cv.imshow('maszk', maszk)
    
    k = cv.waitKey(1) & 0xff
    if k == 27:
        log.write("\nVege\nosszesen:\nfel: \t"+str(cnt_up)+"\nle: \t"+str(cnt_down))
        break

log.flush()
log.close()
cap.release()
cv.destroyAllWindows()
