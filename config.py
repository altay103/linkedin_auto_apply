"""
LinkedIn Bot Konfigürasyon Ayarları
Bu dosyada botun çalışma parametrelerini ayarlayabilirsiniz.
"""

class Config:
    """LinkedIn Bot için yapılandırma sınıfı"""
    
    # Arama parametreleri
    SEARCH_KEYWORDS = [
        "Python Developer",
        "Software Developer", 
        "Backend Developer",
        "Full Stack Developer",
        "Data Scientist",
        "Machine Learning Engineer"
    ]
    
    # Lokasyon filtreleri
    LOCATIONS = [
        "Turkey",
        "İstanbul, Turkey", 
        "Ankara, Turkey",
        "Remote"
    ]
    
    # İş deneyimi seviyesi
    EXPERIENCE_LEVEL = [
        "Entry level",  # Giriş seviyesi
        "Associate",    # Orta seviye
        "Mid-Senior level"  # Üst seviye
    ]
    
    # İş türü
    JOB_TYPE = [
        "Full-time",
        "Part-time", 
        "Contract",
        "Internship"
    ]
    
    # Maksimum başvuru sayısı (günlük)
    MAX_APPLICATIONS_PER_DAY = 20
    
    # Başvuru aralıkları (saniye)
    MIN_DELAY_BETWEEN_APPLICATIONS = 30  # Minimum 30 saniye
    MAX_DELAY_BETWEEN_APPLICATIONS = 120  # Maksimum 2 dakika
    
    # Sayfa yükleme bekleme süresi
    PAGE_LOAD_TIMEOUT = 20
    
    # Element bulma bekleme süresi
    ELEMENT_WAIT_TIMEOUT = 10
    
    # Başvuru mesajı şablonu
    COVER_LETTER_TEMPLATE = """
    Merhaba,
    
    Bu pozisyon için başvuruda bulunmak istiyorum. Yazılım geliştirme konusundaki deneyimim 
    ve teknik becerilerimle ekibinize değer katabileceğime inanıyorum.
    
    Profilimdeki detaylı bilgileri incelemenizi rica ederim.
    
    Saygılarımla,
    """
    
    # Hariç tutulacak şirketler
    EXCLUDED_COMPANIES = [
        "MLM Company",
        "Pyramid Scheme Corp"
    ]
    
    # Hariç tutulacak kelimeler (iş başlığında)
    EXCLUDED_KEYWORDS = [
        "senior",  # Senior pozisyonlar
        "lead",    # Liderlik pozisyonları  
        "manager", # Yöneticilik
        "director" # Direktörlük
    ]
    
    # Tarayıcı ayarları
    BROWSER_CONFIG = {
        "headless": True,  # Tarayıcıyı görünmez modda çalıştır
        "disable_images": True,  # Resim yüklemeyi devre dışı bırak (hız için)
        "window_size": "1920,1080",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Google Auth ayarları
    GOOGLE_AUTH_CONFIG = {
        "enable_auto_detection": True,  # Google giriş butonunu otomatik algıla
        "manual_wait_time": 30,  # Manuel giriş için bekleme süresi (saniye)
        "max_login_attempts": 3,  # Maksimum giriş deneme sayısı
    }
    
    # Gelişmiş ayarlar
    ADVANCED_SETTINGS = {
        "scroll_pause_time": 2,  # Sayfa kaydırma arası bekleme
        "retry_attempts": 3,     # Hata durumunda tekrar deneme sayısı
        "screenshot_on_error": True,  # Hata durumunda ekran görüntüsü al
        "save_applications_log": True,  # Başvuru loglarını kaydet
    }
