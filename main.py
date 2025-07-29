#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Otomatik İş Başvuru Sistemi
Bu sistem günde 1 kez çalışarak Easy Apply ilanlarına otomatik başvuru yapar.
"""

import os
import sys
import logging
from datetime import datetime
from linkedin_bot import LinkedInBot
from config import Config

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('linkedin_bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Ana fonksiyon - LinkedIn botunu çalıştırır"""
    try:
        logger.info("🚀 LinkedIn Otomatik Başvuru Sistemi Başlatılıyor...")
        logger.info(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Çevre değişkenlerini kontrol et
        required_vars = ['LINKEDIN_EMAIL', 'LINKEDIN_PASSWORD']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.error(f"❌ Eksik çevre değişkenleri: {', '.join(missing_vars)}")
            logger.error("GitHub Secrets'da LINKEDIN_EMAIL ve LINKEDIN_PASSWORD tanımlanmalı")
            return False
        
        # Bot'u başlat
        bot = LinkedInBot(
            email=os.getenv('LINKEDIN_EMAIL'),
            password=os.getenv('LINKEDIN_PASSWORD'),
            config=Config()
        )
        
        # İş başvuru sürecini çalıştır
        success = bot.run_job_application_process()
        
        if success:
            logger.info("✅ İş başvuru süreci başarıyla tamamlandı!")
            return True
        else:
            logger.error("❌ İş başvuru sürecinde hata oluştu!")
            return False
            
    except Exception as e:
        logger.error(f"❌ Ana fonksiyonda hata: {str(e)}")
        return False
    finally:
        logger.info("🏁 LinkedIn Bot Kapatılıyor...")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
