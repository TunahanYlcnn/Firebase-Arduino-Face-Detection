# 🛡️ Akıllı Kapı Kilidi Sistemi (Yüz Tanıma & Firebase)

Bu proje, gerçek zamanlı yüz tanıma teknolojisi kullanarak yetkili kişileri tespit eden ve bir kilit sistemini (Arduino) Firebase üzerinden senkronize bir şekilde kontrol eden akıllı bir güvenlik çözümüdür.

## 🚀 Özellikler
* **Gerçek Zamanlı Yüz Tanıma:** OpenCV ve LBPH algoritması ile hızlı ve güvenilir yüz tanımlama.
* **Firebase Entegrasyonu:** Tanınan kişilerin loglanması ve sistem durumunun (islem) bulut üzerinden takibi.
* **Donanım Kontrolü:** Seri port (RS232) üzerinden Arduino ile fiziksel kilit yönetimi.
* **Dinamik Eşik (Threshold):** Ortam ışığına ve tanıma kalitesine göre kendini güncelleyen güven aralığı.

## 📁 Dosya Yapısı
* `Program.py`: Sistemin ana dosyası. Tanıma ve veri iletişimini yönetir.
* `Yuz Kayıt.py`: Yeni kullanıcıları sisteme kaydetmek ve AI modelini eğitmek için kullanılır.
* `veri/`: Kaydedilen yüz fotoğraflarının tutulduğu klasör.
* `denemee/`: Eğitilmiş modelin (`.yml`) saklandığı klasör.

## 🛠️ Kurulum
1.  **Gerekli Kütüphaneler:**
    ```bash
    pip install opencv-contrib-python numpy firebase-admin pyserial Pillow
    ```
2.  **Firebase Ayarları:**
    * Firebase konsolundan bir proje oluşturun.
    * Firestore ve Realtime Database'i aktif edin.
    * Hizmet hesabı (Service Account) anahtarını `.json` olarak indirin ve kod içindeki dosya yolunu güncelleyin.
3.  **Arduino:**
    * Arduino'yu bilgisayarınıza bağlayın ve `COM` portunu `Program.py` içerisinden düzeltin.

## 💻 Kullanım
1.  Önce `Yuz Kayıt.py` dosyasını çalıştırarak yüzünüzü tanıtın.
2.  Eğitim tamamlandıktan sonra `Program.py` dosyasını çalıştırarak sistemi başlatın.
    * `d`: Taramayı tekrar aktif eder.
    * `k`: Manuel olarak sisteme sinyal gönderir.
    * `q`: Programdan güvenli çıkış yapar.

