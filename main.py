# =====================================================================
#  AKABE YAPI MARKET - STOK / ENVANTER TAKİP SİSTEMİ
#  KUZEM Python Eğitimi - Final Projesi
#
#  Kullanılan konular:
#    - OOP (2 sınıf: Urun ve StokYonetici)
#    - Konsol menü arayüzü (while True)
#    - Dosyaya kalıcı kayıt (JSON)
#    - Hata yönetimi (try / except)
#    - Arama / filtreleme
#    - Liste ve sözlük veri yapıları
#    - Fonksiyonlarla kod tekrarının önlenmesi
#    - Özet / rapor ekranı
# =====================================================================

import json
import os

# Verilerin saklanacağı dosya. Program klasörüne göreli olduğu için
# projeyi başka bir bilgisayarda da sorunsuz çalışır.
DOSYA_ADI = "stok.json"


# ---------------------------------------------------------------------
# 1. VARLIK SINIFI: Tek bir ürünü temsil eder.
# ---------------------------------------------------------------------
class Urun:
    def __init__(self, ad, kategori, adet, fiyat, kritik_stok):
        self.ad = ad
        self.kategori = kategori
        self.adet = adet
        self.fiyat = fiyat
        self.kritik_stok = kritik_stok

    def sozluge_cevir(self):
        """Ürünü JSON dosyasına yazmak için sözlüğe dönüştürür."""
        return {
            "ad": self.ad,
            "kategori": self.kategori,
            "adet": self.adet,
            "fiyat": self.fiyat,
            "kritik_stok": self.kritik_stok,
        }

    def kritik_mi(self):
        """Stok kritik seviyenin altına düştü mü kontrol eder."""
        return self.adet <= self.kritik_stok

    def toplam_deger(self):
        """Bu üründen elde stokta kalan toplam parasal değer."""
        return self.adet * self.fiyat


# ---------------------------------------------------------------------
# 2. YÖNETİCİ SINIFI: Tüm ürünleri ve dosya işlemlerini yönetir.
# ---------------------------------------------------------------------
class StokYonetici:
    def __init__(self, dosya_adi):
        self.dosya_adi = dosya_adi
        self.urunler = []  # Urun nesnelerinden oluşan LİSTE
        self.verileri_yukle()

    # ---- Dosya İşlemleri --------------------------------------------
    def verileri_yukle(self):
        """Program açılışında dosyadan ürünleri okur."""
        try:
            with open(self.dosya_adi, "r", encoding="utf-8") as dosya:
                kayitlar = json.load(dosya)
                for kayit in kayitlar:
                    urun = Urun(
                        kayit["ad"],
                        kayit["kategori"],
                        kayit["adet"],
                        kayit["fiyat"],
                        kayit["kritik_stok"],
                    )
                    self.urunler.append(urun)
            print(f"Kayıtlı {len(self.urunler)} ürün dosyadan yüklendi.")
        except FileNotFoundError:
            # SENARYO 1: Dosya ilk kez açılıyor, henüz yok.
            print("Kayıt dosyası bulunamadı, yeni bir stok listesi başlatıldı.")
        except (json.JSONDecodeError, KeyError):
            # SENARYO 2: Dosya bozuk veya beklenen alanlar eksik.
            print("Kayıt dosyası okunamadı, boş listeyle devam ediliyor.")

    def verileri_kaydet(self):
        """Ürün listesini dosyaya yazar (her değişiklikten sonra çağrılır)."""
        kayitlar = []
        for urun in self.urunler:
            kayitlar.append(urun.sozluge_cevir())
        with open(self.dosya_adi, "w", encoding="utf-8") as dosya:
            json.dump(kayitlar, dosya, ensure_ascii=False, indent=4)

    # ---- İşlevler ----------------------------------------------------
    def urun_ekle(self, urun):
        self.urunler.append(urun)
        self.verileri_kaydet()
        print(f"'{urun.ad}' başarıyla eklendi.")

    def urunleri_listele(self):
        if len(self.urunler) == 0:
            print("Kayıtlı ürün bulunmuyor.")
            return

        print("\n{:<4} {:<22} {:<14} {:>6} {:>10} {:>10}".format(
            "No", "Ürün Adı", "Kategori", "Adet", "Fiyat", "Durum"))
        print("-" * 70)
        for sira, urun in enumerate(self.urunler, start=1):
            durum = "KRİTİK!" if urun.kritik_mi() else "Yeterli"
            print("{:<4} {:<22} {:<14} {:>6} {:>10.2f} {:>10}".format(
                sira, urun.ad, urun.kategori, urun.adet, urun.fiyat, durum))
        print("-" * 70)

    def urun_ara(self, anahtar):
        """Ürün adında veya kategoride geçen kayıtları döndürür."""
        anahtar = anahtar.lower()
        bulunanlar = []
        for urun in self.urunler:
            if anahtar in urun.ad.lower() or anahtar in urun.kategori.lower():
                bulunanlar.append(urun)
        return bulunanlar

    def urun_sil(self, sira):
        """Listedeki sıra numarasına göre ürün siler."""
        if sira < 1 or sira > len(self.urunler):
            print("Geçersiz sıra numarası.")
            return
        silinen = self.urunler.pop(sira - 1)
        self.verileri_kaydet()
        print(f"'{silinen.ad}' silindi.")

    def stok_guncelle(self, sira, degisim):
        """Bir ürünün stok adedini artırır (+) veya azaltır (-)."""
        if sira < 1 or sira > len(self.urunler):
            print("Geçersiz sıra numarası.")
            return
        urun = self.urunler[sira - 1]
        yeni_adet = urun.adet + degisim
        if yeni_adet < 0:
            print("Stok sıfırın altına düşemez, işlem iptal edildi.")
            return
        urun.adet = yeni_adet
        self.verileri_kaydet()
        print(f"'{urun.ad}' güncellendi. Yeni stok: {urun.adet}")

    def ozet_rapor(self):
        """Toplam ürün, toplam değer ve kategori bazlı özet gösterir."""
        if len(self.urunler) == 0:
            print("Rapor için kayıtlı ürün bulunmuyor.")
            return

        toplam_urun = len(self.urunler)
        toplam_deger = 0
        kritik_sayisi = 0

        # Kategori bazlı özet için SÖZLÜK kullanıyoruz.
        kategori_ozeti = {}

        for urun in self.urunler:
            toplam_deger += urun.toplam_deger()
            if urun.kritik_mi():
                kritik_sayisi += 1

            if urun.kategori in kategori_ozeti:
                kategori_ozeti[urun.kategori] += urun.adet
            else:
                kategori_ozeti[urun.kategori] = urun.adet

        print("\n" + "=" * 40)
        print("            ÖZET RAPOR")
        print("=" * 40)
        print(f"Toplam ürün çeşidi   : {toplam_urun}")
        print(f"Toplam stok değeri   : {toplam_deger:.2f} TL")
        print(f"Kritik stoktaki ürün : {kritik_sayisi} adet")
        print("-" * 40)
        print("Kategori bazlı toplam adet:")
        for kategori, adet in kategori_ozeti.items():
            print(f"  - {kategori}: {adet}")
        print("=" * 40)


# ---------------------------------------------------------------------
# YARDIMCI FONKSİYONLAR (kod tekrarını önlemek için)
# ---------------------------------------------------------------------
def metin_al(mesaj):
    """Boş olmayan bir metin girişi alır."""
    while True:
        deger = input(mesaj).strip()
        if deger == "":
            print("Bu alan boş bırakılamaz, lütfen tekrar girin.")
        else:
            return deger


def tam_sayi_al(mesaj):
    """Geçerli, negatif olmayan bir tam sayı alır."""
    while True:
        try:
            deger = int(input(mesaj))
            if deger < 0:
                print("Değer negatif olamaz.")
            else:
                return deger
        except ValueError:
            # SENARYO 3: Sayıya çevrilemeyen giriş.
            print("Lütfen geçerli bir tam sayı girin.")


def ondalik_al(mesaj):
    """Geçerli, negatif olmayan bir ondalık sayı (fiyat) alır."""
    while True:
        try:
            deger = float(input(mesaj))
            if deger < 0:
                print("Değer negatif olamaz.")
            else:
                return deger
        except ValueError:
            print("Lütfen geçerli bir sayı girin (örnek: 25.50).")


# ---------------------------------------------------------------------
# MENÜ VE ANA PROGRAM
# ---------------------------------------------------------------------
def menu_goster():
    print("\n" + "=" * 40)
    print("     AKABE YAPI MARKET - STOK TAKİP")
    print("=" * 40)
    print("1 - Ürün Ekle")
    print("2 - Ürünleri Listele")
    print("3 - Ürün Ara")
    print("4 - Stok Güncelle (Giriş/Çıkış)")
    print("5 - Ürün Sil")
    print("6 - Özet Rapor")
    print("0 - Çıkış")
    print("=" * 40)


def ekleme_islemi(yonetici):
    print("\n--- Yeni Ürün Ekle ---")
    ad = metin_al("Ürün adı: ")
    kategori = metin_al("Kategori: ")
    adet = tam_sayi_al("Adet: ")
    fiyat = ondalik_al("Birim fiyat (TL): ")
    kritik = tam_sayi_al("Kritik stok seviyesi: ")
    yeni_urun = Urun(ad, kategori, adet, fiyat, kritik)
    yonetici.urun_ekle(yeni_urun)


def arama_islemi(yonetici):
    print("\n--- Ürün Ara ---")
    anahtar = metin_al("Aranacak kelime (ad veya kategori): ")
    sonuclar = yonetici.urun_ara(anahtar)
    if len(sonuclar) == 0:
        print("Eşleşen ürün bulunamadı.")
    else:
        print(f"{len(sonuclar)} sonuç bulundu:")
        for urun in sonuclar:
            print(f"  - {urun.ad} ({urun.kategori}) | "
                  f"Adet: {urun.adet} | Fiyat: {urun.fiyat:.2f} TL")


def guncelleme_islemi(yonetici):
    print("\n--- Stok Güncelle ---")
    yonetici.urunleri_listele()
    if len(yonetici.urunler) == 0:
        return
    sira = tam_sayi_al("Güncellenecek ürünün sıra no: ")
    degisim = int_al_isaretli("Stok değişimi (giriş için +, çıkış için -): ")
    yonetici.stok_guncelle(sira, degisim)


def int_al_isaretli(mesaj):
    """Pozitif veya negatif olabilen bir tam sayı alır."""
    while True:
        try:
            return int(input(mesaj))
        except ValueError:
            print("Lütfen geçerli bir tam sayı girin (örn. 10 veya -5).")


def silme_islemi(yonetici):
    print("\n--- Ürün Sil ---")
    yonetici.urunleri_listele()
    if len(yonetici.urunler) == 0:
        return
    sira = tam_sayi_al("Silinecek ürünün sıra no: ")
    yonetici.urun_sil(sira)


def main():
    yonetici = StokYonetici(DOSYA_ADI)

    while True:
        menu_goster()
        secim = input("Seçiminiz: ").strip()

        if secim == "1":
            ekleme_islemi(yonetici)
        elif secim == "2":
            yonetici.urunleri_listele()
        elif secim == "3":
            arama_islemi(yonetici)
        elif secim == "4":
            guncelleme_islemi(yonetici)
        elif secim == "5":
            silme_islemi(yonetici)
        elif secim == "6":
            yonetici.ozet_rapor()
        elif secim == "0":
            print("Program kapatılıyor. İyi çalışmalar!")
            break
        else:
            print("Geçersiz seçim, lütfen menüdeki bir numarayı girin.")


if __name__ == "__main__":
    main()
