import cv2
import serial
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials, firestore


cred = credentials.Certificate('Firebase anahtar dosyanın ismini')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://FİREBASE_ADRESİN.firebaseio.com/'
})


try:
    arduino = serial.Serial('COM5', 9600)
except:
    print("Arduino bağlantısı kurulamadı! Lütfen portu kontrol edin.")

tani = cv2.face.LBPHFaceRecognizer_create()
tani.read('denemee/denemee.yml')

cas = "haarcascade_frontalface_default.xml.txt"
yuzcas = cv2.CascadeClassifier(cas)
font = cv2.FONT_HERSHEY_SIMPLEX

cam = cv2.VideoCapture(0)

recognized_confidences = []
threshold = 50.0
db = firestore.client()
collection_ref = db.collection('user')

def api():
    query = collection_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
    docs = query.get()

    for doc in docs:
        print(f'Belge ID: {doc.id}')
        print(f'İsim: {doc.get("isim")}')
        print(f'İslem: {doc.get("islem")}')
        
        islem_tipi = doc.get("islem")
        if islem_tipi == 0:
            arduino.write(b'0')
        elif islem_tipi == 1:
            arduino.write(b'1')
        elif islem_tipi == 2:
            arduino.write(b'2')
        elif islem_tipi == 3:
            arduino.write(b'3')

def post(isim, islem):
    veri = str(islem)
    arduino.write(veri.encode())

    doc_ref = db.collection('user').document()
    doc_ref.set({
        'isim': isim,
        'islem': islem,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

taramaYap = True
while True:
    ret, res = cam.read()
    if not ret:
        break

    if not taramaYap:
        api()

    if taramaYap:
        gri = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        yuzler = yuzcas.detectMultiScale(gri, 1.2, 5)

        _isim = ""
        for (x, y, w, h) in yuzler:
            cv2.rectangle(res, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 255, 0), 4)
            no, uyum = tani.predict(gri[y:y + h, x:x + w])

            if uyum < threshold:
                if no == 1:
                    _isim = "tunahan"
                    post(_isim, 0)
                    taramaYap = False
                elif no == 2:
                    _isim = "mert"
                    post(_isim, 0)
                    taramaYap = False
                elif no == 3:
                    _isim = "yunus"
                    post(_isim, 0)
                    taramaYap = False
                else:
                    _isim = "bilinmiyor"

                recognized_confidences.append(uyum)
            else:
                _isim = "bilinmiyor"

            if len(recognized_confidences) > 0:
                threshold = sum(recognized_confidences) / len(recognized_confidences) + 10

            cv2.rectangle(res, (x - 22, y - 90), (x + w + 22, y - 22), (0, 255, 0), -1)
            cv2.putText(res, _isim, (x, y - 40), font, 2, (255, 255, 255), 3)
        
        cv2.imshow('im', res)

    key = cv2.waitKey(10)
    if key == ord('d'): 
        taramaYap = True
    elif key == ord('q'): 
        break
    elif key == ord('k'):
        post("PC", 1)

cam.release()
cv2.destroyAllWindows()
arduino.close()