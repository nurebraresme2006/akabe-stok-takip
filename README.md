# Akabe Yapı Market - Stok / Envanter Takip Sistemi

KUZEM Python Eğitimi **Final Projesi** olarak geliştirilmiş, konsol tabanlı
bir stok takip uygulamasıdır. Bir yapı market için ürünlerin eklenmesini,
listelenmesini, aranmasını, stok giriş/çıkışının işlenmesini ve özet rapor
alınmasını sağlar. Veriler `stok.json` dosyasında kalıcı olarak saklanır.

## Ne Yapar?

- **Ürün ekleme:** ad, kategori, adet, birim fiyat ve kritik stok seviyesi.
- **Listeleme:** tüm ürünleri tablo halinde gösterir; stok kritik seviyenin
  altındaysa **KRİTİK!** uyarısı verir.
- **Arama:** ürün adına veya kategoriye göre filtreleme.
- **Stok güncelleme:** giriş (+) / çıkış (-) ile adet değiştirme.
- **Silme:** listedeki sıra numarasına göre ürün silme.
- **Özet rapor:** toplam ürün çeşidi, toplam stok değeri (TL), kritik
  stoktaki ürün sayısı ve kategori bazlı toplam adet.

## Nasıl Çalıştırılır?

Projeyi çalıştırmak için Python 3 yeterlidir; **ek kütüphane gerekmez**
(yalnızca standart kütüphaneler `json` ve `os` kullanılır).

```bash
python main.py
```

Program ilk açıldığında `stok.json` yoksa boş bir listeyle başlar ve ilk
ürün eklendiğinde dosyayı otomatik oluşturur.

## Kullanılan Konular

- **OOP (Sınıf ve Nesne):** `Urun` (varlık) ve `StokYonetici` (yönetici)
  olmak üzere 2 sınıf.
- **Konsol menü arayüzü:** `while True` döngüsü ile numaralı menü.
- **Dosya işlemleri:** JSON formatında kalıcı kayıt.
- **Hata yönetimi:** `try/except` ile dosya bulunamadı, bozuk dosya ve
  sayıya çevrilemeyen giriş senaryoları.
- **Veri yapıları:** ürün listesi (list) ve kategori özeti (dict).
- **Fonksiyonlar:** ekleme/arama/güncelleme/silme ile ortak giriş
  fonksiyonları ayrı ayrı tanımlanarak kod tekrarı önlendi.
- **Karar yapıları ve döngüler:** menü yönlendirmesi ve tablo çıktısı.

## Ekran Görüntüsü

```
========================================
     AKABE YAPI MARKET - STOK TAKİP
========================================
1 - Ürün Ekle
2 - Ürünleri Listele
3 - Ürün Ara
4 - Stok Güncelle (Giriş/Çıkış)
5 - Ürün Sil
6 - Özet Rapor
0 - Çıkış
========================================
```

## Dosya Yapısı

```
.
├── main.py      # Uygulamanın tüm kodu
├── stok.json    # Ürün verilerinin saklandığı dosya (program oluşturur)
└── README.md    # Bu dosya
```
