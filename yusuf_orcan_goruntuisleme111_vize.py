# El Hareketlerine Dayalı Etkileşimli Sistem
#
# Bu Python programı, bir bilgisayarın kamerası aracılığıyla kullanıcının ellerini takip eder ve çeşitli el hareketlerine dayalı etkileşimler sağlar.
# Mediapipe kütüphanesi kullanılarak el izleme gerçekleştirilir ve farklı el hareketleriyle:
# - Spotify müzik kontrolü (başlat/durdur)
# - Ekran parlaklığını ayarlama
# - Ses seviyesini kontrol etme
# - Web tarayıcısını açma
#
# Kullanıcı sağ elini ve sol elini farklı hareketlerle kontrol edebilir:
# - Sağ el: Spotify kontrolü, ses seviyesi ayarlama, web tarayıcısı açma
# - Sol el: Ekran parlaklığı ayarlama, Spotify müziğini durdurma
#
# Program, her el hareketini tanımak için belirli bir mesafe veya pozisyonu analiz eder ve kullanıcı hareketlerine tepki verir.
# Programda platform bağımsızlık sağlanarak, Windows, Linux ve macOS işletim sistemlerinde çalışabilmesi için gerekli koşullar sağlanmıştır.
#
# Gereksinimler:
# - opencv-python: Görüntü işleme için
# - mediapipe: El hareketlerini algılamak için
# - pyautogui: Uygulama açma ve klavye simülasyonu için
# - pycaw: Ses seviyesini kontrol etmek için (sadece Windows)
# - screen-brightness-control: Ekran parlaklığını kontrol etmek için
# - numpy: Matematiksel işlemler için
# - platform: Çalışılan işletim sistemini belirlemek için
# - Kütüphaneleri yüklemek için pip install komutunu kullanabilirsiniz:
# "pip install opencv-python mediapipe pyautogui pycaw screen-brightness-control numpy platform" bu kütüphaler gereklidir.
#
#
# Kullanım:
# Program çalıştığında, kameradan gelen görüntüler üzerinden el hareketlerini takip eder ve belirli bir hareket tanımlandığında 
# ilgili işlevi gerçekleştirir (örneğin Spotify açma, ekran parlaklığını ayarlama). Program, sürekli olarak kameradan görüntü alır 
# ve yapılan hareketlere göre tepki verir.
# Kullanıcı, 'Esc' tuşuna basarak programdan çıkabilir.
#
#
# YUSUF ORÇAN - 2023688051



import cv2
import mediapipe as mp
import math
import time
import subprocess
import platform
import numpy as np
import pyautogui
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# Platform türünü öğreniyoruz (Windows, Linux, macOS)
PLATFORM = platform.system()

# Ses ayarlayıcı başlatılıyor
cihazlar = AudioUtilities.GetSpeakers()  # Ses cihazlarını al
arayuz = cihazlar.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)  # Ses ayarlarını aktive et
ses_seviyesi = cast(arayuz, POINTER(IAudioEndpointVolume))  # Ses seviyesini kontrol etmek için gerekli arayüz

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

# Uygulama açmak için fonksiyon
def uygulama_ac(uygulama):
    try:
        if PLATFORM == "Windows":
            subprocess.Popen(f"start {uygulama}", shell=True)  # Windows'ta uygulama aç
        elif PLATFORM == "Linux":
            subprocess.Popen([uygulama])  # Linux'ta uygulama aç
        elif PLATFORM == "Darwin":
            subprocess.Popen(["open", "-a", uygulama])  # macOS'ta uygulama aç
    except Exception as e:
        print("Uygulama açma hatası:", e)

spotify_durumu = False  # Spotify durumu

# Spotify'ı açma fonksiyonu
def spotify_ac():
    global spotify_durumu
    if not spotify_durumu:
        uygulama_ac("spotify")  # Spotify'ı aç
        spotify_durumu = True

# Spotify'ı kapama fonksiyonu
def spotify_kapat():
    global spotify_durumu
    if spotify_durumu:
        try:
            if PLATFORM == "Windows":
                pyautogui.hotkey("alt", "f4")  # Windows'ta Spotify'ı kapat
            elif PLATFORM == "Darwin":
                pyautogui.hotkey("command", "q")  # macOS'ta Spotify'ı kapat
            else:
                pyautogui.hotkey("alt", "f4")  # Linux'ta Spotify'ı kapat
        except Exception as e:
            print("Spotify kapatma hatası:", e)
        spotify_durumu = False

# Spotify müziğini başlat veya durdur
def spotify_muzik(baslat=True):
    pyautogui.press("playpause")  # Play/pause tuşuna bas

# Belirli bir fonksiyonu işlem yapılabilir olup olmadığını kontrol ederek çalıştırma
def islem_yap(func):
    if kontrol.hazir_mi():
        func()  # Fonksiyonu çalıştır
        kontrol.guncelle()  # Zamanı güncelle
        return True
    return False

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

            # Farklı el hareketlerini tanımla (yumruk, iki parmak, işaret parmağı ve serçe)
            yumruk = not (isaret_yukari or orta_yukari or yuzuk_yukari or serce_yukari or bas_yukari)
            iki_parmak = isaret_yukari and orta_yukari and not (yuzuk_yukari or serce_yukari or bas_yukari)
            kurt_isareti = isaret_yukari and serce_yukari and not (orta_yukari or yuzuk_yukari)

            # Sağ el için işlemler
            if etiket == "Right":
                if kurt_isareti and islem_yap(lambda: uygulama_ac("chrome")):  # Sağ işaret parmağı ve serçe ile Chrome aç
                    islem_yapildi = True
                elif iki_parmak and islem_yap(spotify_ac):  # İki parmakla Spotify aç
                    islem_yapildi = True
                elif yumruk and islem_yap(lambda: spotify_muzik(True)):  # Yumruk yapınca Spotify müziğini başlat
                    islem_yapildi = True
                elif not islem_yapildi:
                    vol = max(min(mesafe / 150, 1), 0)  # Ses seviyesi mesafeye göre ayarlanıyor
                    try:
                        ses_seviyesi.SetMasterVolumeLevelScalar(vol, None)  # Ses seviyesini ayarla
                    except:
                        pass
                    cv2.putText(frame, f"Ses: %{int(vol*100)}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)  # Ekrana yazdır

            # Sol el için işlemler
            elif etiket == "Left":
                if iki_parmak and islem_yap(spotify_kapat):  # Sol iki parmakla Spotify'ı kapat
                    islem_yapildi = True
                elif yumruk and islem_yap(lambda: spotify_muzik(False)):  # Sol yumrukla Spotify müziğini durdur
                    islem_yapildi = True
                elif not islem_yapildi:
                    parlaklik = int(max(min((mesafe / 150) * 100, 100), 0))  # Parlaklık mesafeye göre ayarlanıyor
                    try:
                        sbc.set_brightness(parlaklik)  # Ekran parlaklığını ayarla
                    except:
                        pass
                    cv2.putText(frame, f"Parlaklik: %{parlaklik}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)  # Ekrana yazdır

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