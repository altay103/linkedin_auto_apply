# LinkedIn Otomatik İş Başvuru Sistemi 🤖

Bu sistem LinkedIn'deki **Easy Apply** ilanlarına otomatik başvuru yapmak için geliştirilmiştir. GitHub Actions kullanarak **günde 1 kez otomatik çalışır** ve tamamen **ücretsizdir**.

## 🎯 Özellikler

- ✅ **Otomatik Easy Apply başvuruları**
- ✅ **Günlük maksimum başvuru limiti** (varsayılan: 20)
- ✅ **Akıllı filtreleme** (pozisyon, şirket, lokasyon)
- ✅ **İnsan benzeri davranış** (rastgele bekleme süreleri)
- ✅ **Detaylı raporlama** ve loglama
- ✅ **GitHub Actions ile ücretsiz çalışma**
- ✅ **Anti-detection** özellikler

## 🚀 Kurulum

### 1. GitHub Repository Kurulumu

1. Bu repository'yi kendi GitHub hesabınıza **fork** edin veya **clone** yapın
2. Repository ayarlarından **Actions** sekmesini aktif edin

### 2. LinkedIn Bilgilerini Ayarlama

GitHub repository'nizde **Secrets** ayarlayın:

1. Repository sayfasında **Settings** > **Secrets and variables** > **Actions**
2. **New repository secret** butonuna tıklayın
3. Aşağıdaki secret'ları ekleyin:

```
LINKEDIN_EMAIL=sizin@email.com
LINKEDIN_PASSWORD=şifreniz
```

⚠️ **ÖNEMLİ**: LinkedIn bilgileriniz GitHub Secrets'da güvenli şekilde saklanır ve kod içinde görünmez.

### 3. Bot Ayarlarını Özelleştirme

`config.py` dosyasını düzenleyerek botun davranışını özelleştirebilirsiniz:

```python
# Arama anahtar kelimeleri
SEARCH_KEYWORDS = [
    "Python Developer",
    "Software Developer", 
    "Backend Developer"
]

# Lokasyonlar
LOCATIONS = [
    "Turkey",
    "İstanbul, Turkey", 
    "Remote"
]

# Günlük maksimum başvuru sayısı
MAX_APPLICATIONS_PER_DAY = 20
```

## ⏰ Çalışma Zamanı

Bot varsayılan olarak **her gün saat 11:00** (Türkiye saati) çalışır.

Zamanı değiştirmek için `.github/workflows/daily_job.yml` dosyasındaki cron ayarını düzenleyin:

```yaml
schedule:
  - cron: '0 8 * * *'  # UTC 08:00 = TR 11:00
```

### Cron Zaman Örnekleri:
- `0 6 * * *` → Her gün 09:00 (Türkiye saati)
- `0 12 * * *` → Her gün 15:00 (Türkiye saati)
- `0 18 * * 1-5` → Hafta içi her gün 21:00 (Türkiye saati)

## 🔧 Manuel Çalıştırma

Botu manuel olarak çalıştırmak için:

1. GitHub repository'nize gidin
2. **Actions** sekmesine tıklayın
3. **LinkedIn Auto Apply Bot** workflow'unu seçin
4. **Run workflow** butonuna tıklayın

## 📊 Raporlar ve Loglar

Bot her çalıştığında detaylı raporlar oluşturur:

- **Başvuru istatistikleri**
- **Başvuru yapılan işler listesi**
- **Hata logları**
- **Zaman damgalı aktivite geçmişi**

Raporları görüntülemek için:
1. **Actions** sekmesine gidin
2. Son çalıştırılan workflow'u tıklayın
3. **Artifacts** bölümünden log dosyalarını indirin

## ⚙️ Gelişmiş Ayarlar

### Filtreleme Seçenekleri

```python
# Hariç tutulacak şirketler
EXCLUDED_COMPANIES = [
    "MLM Company",
    "Pyramid Scheme Corp"
]

# Hariç tutulacak pozisyon kelimeleri
EXCLUDED_KEYWORDS = [
    "senior",   # Senior pozisyonları hariç tut
    "lead",     # Lead pozisyonları hariç tut
    "manager"   # Yöneticilik pozisyonları hariç tut
]
```

### Güvenlik Ayarları

```python
# Başvuru aralıkları (anti-detection)
MIN_DELAY_BETWEEN_APPLICATIONS = 30   # 30 saniye
MAX_DELAY_BETWEEN_APPLICATIONS = 120  # 2 dakika

# Tarayıcı ayarları
BROWSER_CONFIG = {
    "headless": True,  # Görünmez mod
    "disable_images": True,  # Hız için resim yükleme kapalı
}
```

## 🛡️ Güvenlik ve Etik

### ⚠️ Riskler
- LinkedIn hesabınız kilitlenebilir
- IP adresiniz engellenebilir
- LinkedIn'in Kullanım Koşulları'nı ihlal edebilir

### 🛡️ Güvenlik Önlemleri
- **İnsan benzeri davranış**: Rastgele bekleme süreleri
- **Makul başvuru limiti**: Günde 20 başvuru (değiştirilebilir)
- **Akıllı filtreleme**: Sadece uygun pozisyonlara başvuru
- **Hata yönetimi**: Bot hata durumunda güvenli şekilde durur

### 💡 Öneri
Bu botu **sorumlu** bir şekilde kullanın:
- Günlük başvuru sayısını abartmayın
- Sadece gerçekten ilginizi çeken pozisyonlar için filtreleme yapın
- CV'nizi ve profilinizi güncel tutun

## 🆘 Sorun Giderme

### Bot çalışmıyor
1. **Secrets'ları kontrol edin**: LinkedIn email/şifre doğru mu?
2. **Actions'ın aktif olduğunu** kontrol edin
3. **Workflow log'larını** inceleyin

### LinkedIn girişi başarısız
1. **2FA (İki faktörlü doğrulama)** kapalı olmalı
2. **Şifrenizde özel karakter** varsa escape etmeniz gerekebilir
3. **Hesabınız kilitli** olabilir

### Başvuru yapılmıyor
1. **Easy Apply filtresi** çalışıyor mu kontrol edin
2. **Arama kriterleri** çok spesifik olabilir
3. **Hariç tutma filtreleri** çok kısıtlayıcı olabilir

## 📝 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Ticari olmayan kullanım için serbesttir.

## ⭐ Katkıda Bulunma

Bu projeyi geliştirmek için:
1. Repository'yi fork edin
2. Yeni özellik ekleyin
3. Pull request gönderin

---

**🎯 İyi başvurular! Umarım hayalinizdeki işi bulursunuz! 🚀**
