import cv2, os
import numpy as np
from PIL import Image

vid_cam = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml.txt')

face_id = 1
count = 0 

print("Yüz kaydı başlıyor. Lütfen kameraya bakın...")

while (True):
    _, image_frame = vid_cam.read()
    gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(image_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        count += 1
        cv2.imwrite("veri/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])
        cv2.imshow('Kayit Ekrani', image_frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
    elif count >= 100: 
        break

vid_cam.release()
cv2.destroyAllWindows()

recognizer = cv2.face.LBPHFaceRecognizer_create()

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])      
        faces = detector.detectMultiScale(img_numpy)
        
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y + h, x:x + w])
            ids.append(id)
    return faceSamples, ids

faces, ids = getImagesAndLabels('veri')
recognizer.train(faces, np.array(ids))

if not os.path.exists('denemee'):
    os.makedirs('denemee')

recognizer.save('denemee/denemee.yml')
print("[BİLGİ] Eğitim tamamlandı ve denemee.yml dosyası güncellendi.")