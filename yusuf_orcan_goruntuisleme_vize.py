# El hareketleriyle ses seviyesi ve ekran parlaklığını kontrol etme sistemi
# Bu program, bir web kamerası aracılığıyla sağ ve sol eldeki parmak hareketlerini algılar.
# Sağ elde baş ve işaret parmağı arasındaki mesafe ses seviyesini ayarlarken, 
# sol elde aynı hareket ekran parlaklığını kontrol eder.
# Mediapipe kütüphanesi ile el işaretlerini algılar, pycaw ile ses seviyesi, 
# screen_brightness_control ile ise ekran parlaklığını değiştirir.
#
# Gereksinimler:
# - OpenCV
# - Mediapipe
# - Pycaw (ses kontrolü)
# - screen_brightness_control (parlaklık kontrolü)
# - Kütüphaneleri yüklemek için pip install komutunu kullanabilirsiniz: 
# "pip install opencv-python mediapipe screen-brightness-control pycaw comtypes" bu kütüphaler gereklidir.
#
#
# Kullanım:
# - Sağ elde baş ve işaret parmağı arasındaki mesafe ses seviyesini kontrol eder.
# - Sol elde baş ve işaret parmağı arasındaki mesafe ekran parlaklığını kontrol eder.
# - Program, her iki elin hareketlerini algılar ve doğru işlemleri gerçekleştirir.
# - 'Esc' tuşuna basarak programdan çıkabilirsiniz.
#
# YUSUF ORÇAN - 2023688051

import cv2
import mediapipe as mp
import math
import time
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# Ses ayarlayıcı başlatılıyor
cihazlar = AudioUtilities.GetSpeakers()  # Ses cihazlarını al
arayüz = cihazlar.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)  # Ses ayarlarını aktive et
ses_seviyesi = cast(arayüz, POINTER(IAudioEndpointVolume))  # Ses seviyesini kontrol etmek için gerekli arayüz

# Mediapipe ile el algılamayı başlatıyoruz
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)  # Maksimum 2 el, %70 güvenle algıla
drawing = mp.solutions.drawing_utils  # Çizim için yardımcı fonksiyonlar

# Zaman kontrol sınıfı: Hareketler arasında belirli bir süre beklemeyi sağlar
class ZamanKontrol:
    def __init__(self, bekleme=2):
        self.son_zaman = 0
        self.bekleme = bekleme

    def hazir_mi(self):
        # Belirli bir süre geçti mi diye kontrol eder
        return time.time() - self.son_zaman > self.bekleme

    def guncelle(self):
        # Son zamanı günceller
        self.son_zaman = time.time()

kontrol = ZamanKontrol()  # Zaman kontrolünü başlat

# Kamera başlatma
kamera = cv2.VideoCapture(0)

# Sonsuz döngü, her kareyi alarak işlemi sürekli olarak devam ettiriyor
while True:
    ret, frame = kamera.read()  # Kameradan bir kare al
    if not ret:
        break  # Eğer kare alınamazsa döngüden çık

    frame = cv2.flip(frame, 1)  # Görüntüyü yatayda ters çevir
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR'den RGB'ye dönüşüm
    sonuc = hands.process(rgb)  # El algılama işlemi
    islem_yapildi = False  # İşlem yapılıp yapılmadığını kontrol et

    if sonuc.multi_hand_landmarks:  # Eğer eller algılanmışsa
        for el, sinif in zip(sonuc.multi_hand_landmarks, sonuc.multi_handedness):  # Her el için
            if islem_yapildi:
                continue  # Eğer işlem yapıldıysa devam etme

            etiket = sinif.classification[0].label  # Elin sağ mı sol mu olduğunu al
            lm = el.landmark  # Elin işaret noktalarını al

            # İşaret noktalarını ekran koordinatlarına dönüştür
            def al(i): return int(lm[i].x * frame.shape[1]), int(lm[i].y * frame.shape[0])

            bas, isaret, orta, yuzuk, serce = al(4), al(8), al(12), al(16), al(20)
            bas_eklem, isaret_eklem = al(3), al(6)

            # Parmakların konumlarını kontrol et
            isaret_yukari = isaret[1] < isaret_eklem[1]
            orta_yukari = orta[1] < al(10)[1]
            yuzuk_yukari = yuzuk[1] < al(14)[1]
            serce_yukari = serce[1] < al(18)[1]
            bas_yukari = bas[0] > bas_eklem[0] if etiket == "Right" else bas[0] < bas_eklem[0]

            # Elin işaret noktaları arasındaki mesafeyi hesapla
            mesafe = math.hypot(isaret[0] - bas[0], isaret[1] - bas[1])

            # Sağ elin hareketleriyle ses seviyesini ayarla
            if etiket == "Right":
                ses_seviyesi = max(min(mesafe / 150, 1), 0)  # Ses seviyesi mesafeye göre ayarlanıyor
                try:
                    ses_seviyesi.SetMasterVolumeLevelScalar(ses_seviyesi, None)  # Ses seviyesini ayarla
                except:
                    pass
                cv2.putText(frame, f"ses_seviyesi: %{int(ses_seviyesi*100)}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)  # Ekrana yazdır

            # Sol elin hareketleriyle parlaklık ayarla
            elif etiket == "Left":
                parlaklik = int(max(min((mesafe / 150) * 100, 100), 0))  # Parlaklık mesafeye göre ayarlanıyor
                try:
                    sbc.set_brightness(parlaklik)  # Ekran parlaklığını ayarla
                except:
                    pass
                cv2.putText(frame, f"Parlaklik: %{parlaklik}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)  # Ekrana yazdır

            # Elin işaretlerini çiz
            drawing.draw_landmarks(frame, el, mp_hands.HAND_CONNECTIONS)

    # Sonuçları ekranda göster
    cv2.imshow("El Kontrol Sistemi", frame)

    # Esc tuşu ile çıkma
    if cv2.waitKey(1) & 0xFF == 27:  # 'Esc' tuşuna basılınca çık
        break

# Kamera işlemini sonlandır
kamera.release()
cv2.destroyAllWindows()
