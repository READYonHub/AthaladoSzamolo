# OpenCV és imutils csomagok importálása
import cv2  # package name
import imutils

# Videó beolvasása vagy webkamera kapcsolódás
cap = cv2.VideoCapture('test_video.mp4')
#cap = cv2.VideoCapture(1)  # A webkamera használata, az 1-es index az eszköz sorszáma

# Fő ciklus, amely folyamatosan megjeleníti a képet egy ablakban
while True:
    # Videó keret beolvasása
    ret, frame = cap.read()

    # Keret méretének módosítása 800 pixel szélességre az imutils csomag segítségével
    frame = imutils.resize(frame, width=800)

    # Szöveg hozzáadása a képhez
    text = "a cs2 egy retek nyakcsavaridegelrazodast okozo hulladek"
    cv2.putText(frame, text, (5, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 1)

    # Téglalap rajzolása a képre
    cv2.rectangle(frame, (50, 50), (500, 500), (0, 0, 255), 2)

    # Kép megjelenítése az 'Application' címke alatt
    cv2.imshow('Application', frame)

    # Kép mentése
    cv2.imwrite('output_frame.jpg', frame)

    # Várakozás a felhasználói bemenetre, 1 miliszekundumig
    key = cv2.waitKey(1)

    # Ellenőrzés, hogy a lenyomott billentyű 'q'-e
    if key == ord('q'):
        # Ha igen, akkor kilép a ciklusból
        break

# Az ablakok bezárása
cv2.destroyAllWindows()
