
BL242 Görüntü İşleme Vize Projesi - Yusuf Orçan

Proje Açıklaması
- Bu proje, Mediapipe kütüphanesi kullanarak el hareketlerine dayalı etkileşimli bir görüntü işleme uygulaması geliştirmeyi amaçlamaktadır. 
- Proje, kullanıcıların sağ ve sol ellerindeki parmak hareketleriyle farklı etkileşimler gerçekleştirmelerine olanak tanır. Ses seviyesi, 
ekran parlaklığı gibi özellikler, el parmakları arasındaki mesafeye göre kontrol edilir. Ayrıca, belirli el hareketleri ile Spotify uygulaması 
kontrol edilip, varsayılan web tarayıcısı açılabilir.

Proje Özellikleri
Sağ El:
- Baş ve işaret parmağı arasındaki mesafe ile ses seviyesi kontrolü.

Sol El:
- Baş ve işaret parmağı arasındaki mesafe ile ekran parlaklığı ayarı.
- İşaret ve orta parmak ile web tarayıcısı açma işlemi.

Global Özellikler:
- Mediapipe kullanılarak el hareketlerinin algılanması.
- PyCaw kütüphanesiyle ses seviyesi kontrolü.
- Screen-brightness-control ile ekran parlaklığı ayarı.

Teknolojiler ve Kütüphaneler
- Python 3.x
- OpenCV
- Mediapipe
- PyCaw (Ses kontrolü)
- Screen-brightness-control (Ekran parlaklığı kontrolü)
- PyAutoGUI (UI kontrolü ve otomasyon)
- NumPy

Proje Dosyaları
yusuf_orcan_goruntuisleme_vize.py:
- Sağ ve sol eldeki parmak hareketlerine dayalı olarak ses seviyesi ve ekran parlaklık kontrolünü sağlar.

yusuf_orcan_goruntuisleme111_vize.py:
- Ek olarak, sağ eldeki hareketler ile Spotify kontrolünü ve sol eldeki hareketler ile tarayıcı açılmasını içerir.

Kurulum ve Çalıştırma
Gerekli kütüphaneleri yükleyin:
Proje için gerekli olan tüm Python kütüphanelerini yüklemek için aşağıdaki komutu kullanabilirsiniz:

"pip install opencv-python mediapipe pycaw screen-brightness-control pyautogui numpy"

hand_landmarker.task 

Kodları Çalıştırın:
İlgili dosyayı çalıştırarak uygulamanın çalışmasını sağlayabilirsiniz:

"python yusuf_orcan_goruntuisleme_vize.py"
veya
"python yusuf_orcan_goruntuisleme111_vize.py"

Bu dosyalar, el hareketlerinizi algılayarak belirtilen etkileşimleri gerçekleştirecektir.

Kullanım
- Ses Seviyesi: Sağ elde baş ve işaret parmağı arasındaki mesafeye göre ses seviyesi azalacak veya artacaktır.
- Ekran Parlaklığı: Sol elde baş ve işaret parmağı arasındaki mesafe ile ekranın parlaklığı ayarlanabilir.
- Spotify ve Tarayıcı Kontrolü: Sağ elde işaret ve orta parmak açıkken Spotify başlatılır, sol elde aynı hareket ile varsayılan web tarayıcısı açılır.

Proje İleri Seviye Özellikleri
- Proje, gerçek zamanlı görüntü işleme ve etkileşimli kullanıcı arayüzü sunarak, kullanıcı deneyimini iyileştirir.
- Mediapipe'in güçlü el tespiti özellikleri ile anlık parmak hareketleri algılanır ve hızlı tepki verilir.
- PyCaw ve screen-brightness-control ile ses seviyesi ve ekran parlaklığı gibi sistem özelliklerine dair detaylı kontrol sağlanır.

Katkıda Bulunma
Eğer projeye katkıda bulunmak isterseniz:
1. Fork yapın.
2. Değişikliklerinizi yapın.
3. Pull request oluşturun.

- Yusuf Orçan: Çukurova Üniversitesi KOZAN MYO Öğrencisi - Görüntü işleme Projesi
