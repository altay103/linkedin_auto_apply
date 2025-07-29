#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Otomatik İş Başvuru Botu
Selenium kullanarak LinkedIn'de Easy Apply ilanlarına otomatik başvuru yapar.
"""

import time
import random
import logging
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    ElementClickInterceptedException,
    StaleElementReferenceException
)

logger = logging.getLogger(__name__)

class LinkedInBot:
    """LinkedIn otomatik iş başvuru botu"""
    
    def __init__(self, email: str, password: str, config):
        self.email = email
        self.password = password
        self.config = config
        self.driver = None
        self.applications_count = 0
        self.applied_jobs = []
        self.failed_jobs = []
        
    def setup_driver(self) -> webdriver.Chrome:
        """Chrome driver'ını ayarlar ve döndürür"""
        try:
            chrome_options = Options()
            
            if self.config.BROWSER_CONFIG["headless"]:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images") if self.config.BROWSER_CONFIG["disable_images"] else None
            chrome_options.add_argument(f"--window-size={self.config.BROWSER_CONFIG['window_size']}")
            chrome_options.add_argument(f"--user-agent={self.config.BROWSER_CONFIG['user_agent']}")
            
            # Docker/Linux ortamları için ek ayarlar
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(self.config.PAGE_LOAD_TIMEOUT)
            
            logger.info("✅ Chrome driver başarıyla kuruldu")
            return driver
            
        except Exception as e:
            logger.error(f"❌ Driver kurulumunda hata: {str(e)}")
            raise
    
    def login_to_linkedin(self) -> bool:
        """LinkedIn'e giriş yapar"""
        try:
            logger.info("🔑 LinkedIn'e giriş yapılıyor...")
            
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(random.uniform(2, 4))
            
            # Email alanını doldur
            email_field = WebDriverWait(self.driver, self.config.ELEMENT_WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.clear()
            self.human_like_typing(email_field, self.email)
            
            # Şifre alanını doldur
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            self.human_like_typing(password_field, self.password)
            
            # Giriş butonuna tıkla
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Giriş kontrolü
            time.sleep(5)
            if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                logger.info("✅ LinkedIn'e başarıyla giriş yapıldı")
                return True
            else:
                logger.error("❌ LinkedIn girişi başarısız - URL kontrol et")
                return False
                
        except Exception as e:
            logger.error(f"❌ LinkedIn giriş hatası: {str(e)}")
            return False
    
    def human_like_typing(self, element, text: str):
        """İnsan benzeri yazma simülasyonu"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def search_jobs(self, keyword: str, location: str) -> bool:
        """İş ilanlarını arar"""
        try:
            logger.info(f"🔍 İş aranıyor: {keyword} - {location}")
            
            # Jobs sayfasına git
            self.driver.get("https://www.linkedin.com/jobs/")
            time.sleep(random.uniform(3, 5))
            
            # Arama kutusunu bul ve temizle
            search_box = WebDriverWait(self.driver, self.config.ELEMENT_WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'jobs-search-box-keyword-id')]"))
            )
            search_box.clear()
            self.human_like_typing(search_box, keyword)
            
            # Lokasyon kutusunu bul ve temizle
            location_box = self.driver.find_element(By.XPATH, "//input[contains(@id, 'jobs-search-box-location-id')]")
            location_box.clear()
            location_box.send_keys(Keys.CONTROL + "a")
            self.human_like_typing(location_box, location)
            
            # Arama butonuna tıkla
            search_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'jobs-search-box__submit-button')]")
            search_button.click()
            
            time.sleep(random.uniform(3, 5))
            
            # Easy Apply filtresini uygula
            self.apply_easy_apply_filter()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ İş arama hatası: {str(e)}")
            return False
    
    def apply_easy_apply_filter(self):
        """Easy Apply filtresini uygular"""
        try:
            logger.info("⚡ Easy Apply filtresi uygulanıyor...")
            
            # Filtreler butonunu tıkla
            filters_button = WebDriverWait(self.driver, self.config.ELEMENT_WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'filters') or contains(text(), 'filters')]"))
            )
            filters_button.click()
            time.sleep(2)
            
            # Easy Apply checkbox'ını bul ve işaretle
            easy_apply_checkbox = WebDriverWait(self.driver, self.config.ELEMENT_WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Easy Apply')]//input[@type='checkbox']"))
            )
            
            if not easy_apply_checkbox.is_selected():
                easy_apply_checkbox.click()
                time.sleep(1)
            
            # Filtreleri uygula
            apply_button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Apply') and contains(@data-test-id, 'filter')]")
            apply_button.click()
            
            time.sleep(random.uniform(3, 5))
            logger.info("✅ Easy Apply filtresi uygulandı")
            
        except Exception as e:
            logger.warning(f"⚠️ Easy Apply filtresi uygulanamadı: {str(e)}")
    
    def get_job_listings(self) -> List[Dict]:
        """Sayfa üzerindeki iş ilanlarını toplar"""
        try:
            # Sayfayı scroll et (daha fazla ilan yüklemek için)
            self.scroll_page()
            
            job_cards = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'job-search-card')]")
            jobs = []
            
            for card in job_cards[:self.config.MAX_APPLICATIONS_PER_DAY]:
                try:
                    title_element = card.find_element(By.XPATH, ".//h3[contains(@class, 'base-search-card__title')]//a")
                    company_element = card.find_element(By.XPATH, ".//h4[contains(@class, 'base-search-card__subtitle')]")
                    location_element = card.find_element(By.XPATH, ".//span[contains(@class, 'job-search-card__location')]")
                    
                    job_data = {
                        'title': title_element.text.strip(),
                        'company': company_element.text.strip(),
                        'location': location_element.text.strip(),
                        'url': title_element.get_attribute('href'),
                        'element': card
                    }
                    
                    # Filtreleme kontrolü
                    if self.should_apply_to_job(job_data):
                        jobs.append(job_data)
                    
                except Exception as e:
                    logger.warning(f"⚠️ İş kartı okunamadı: {str(e)}")
                    continue
            
            logger.info(f"📋 {len(jobs)} uygun iş ilanı bulundu")
            return jobs
            
        except Exception as e:
            logger.error(f"❌ İş listesi alınırken hata: {str(e)}")
            return []
    
    def should_apply_to_job(self, job_data: Dict) -> bool:
        """İşe başvuru yapılıp yapılmayacağını kontrol eder"""
        title = job_data['title'].lower()
        company = job_data['company'].lower()
        
        # Hariç tutulan şirketler
        for excluded_company in self.config.EXCLUDED_COMPANIES:
            if excluded_company.lower() in company:
                logger.info(f"⏭️ Hariç tutulan şirket: {job_data['company']}")
                return False
        
        # Hariç tutulan kelimeler
        for excluded_keyword in self.config.EXCLUDED_KEYWORDS:
            if excluded_keyword.lower() in title:
                logger.info(f"⏭️ Hariç tutulan pozisyon: {job_data['title']}")
                return False
        
        return True
    
    def scroll_page(self):
        """Sayfayı yavaşça scroll eder"""
        scroll_pause_time = self.config.ADVANCED_SETTINGS['scroll_pause_time']
        
        # Sayfanın sonuna kadar scroll et
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def apply_to_job(self, job_data: Dict) -> bool:
        """Tek bir işe başvuru yapar"""
        try:
            logger.info(f"📝 Başvuru yapılıyor: {job_data['title']} - {job_data['company']}")
            
            # İş ilanı sayfasına git
            self.driver.get(job_data['url'])
            time.sleep(random.uniform(3, 5))
            
            # Easy Apply butonunu bul
            try:
                easy_apply_button = WebDriverWait(self.driver, self.config.ELEMENT_WAIT_TIMEOUT).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Easy Apply') or contains(text(), 'Easy Apply')]"))
                )
                easy_apply_button.click()
                time.sleep(2)
                
                # Başvuru formunu doldur
                success = self.fill_application_form()
                
                if success:
                    self.applications_count += 1
                    self.applied_jobs.append(job_data)
                    logger.info(f"✅ Başvuru başarılı: {job_data['title']}")
                    return True
                else:
                    self.failed_jobs.append(job_data)
                    return False
                    
            except TimeoutException:
                logger.warning(f"⚠️ Easy Apply butonu bulunamadı: {job_data['title']}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Başvuru hatası: {str(e)}")
            self.failed_jobs.append(job_data)
            return False
    
    def fill_application_form(self) -> bool:
        """Başvuru formunu doldurur"""
        try:
            max_attempts = 3
            current_attempt = 0
            
            while current_attempt < max_attempts:
                try:
                    # İleri butonunu bul ve tıkla
                    next_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Continue') or contains(@aria-label, 'Next') or contains(text(), 'Next') or contains(text(), 'Continue')]"))
                    )
                    next_button.click()
                    time.sleep(2)
                    current_attempt += 1
                    
                except TimeoutException:
                    # Submit/Send butonunu ara
                    try:
                        submit_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Submit') or contains(text(), 'Submit') or contains(text(), 'Send')]"))
                        )
                        submit_button.click()
                        time.sleep(2)
                        logger.info("📤 Başvuru gönderildi")
                        return True
                        
                    except TimeoutException:
                        logger.warning("⚠️ Submit butonu bulunamadı")
                        break
                
                # Ek bilgi alanları varsa doldur
                self.fill_additional_fields()
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Form doldurma hatası: {str(e)}")
            return False
    
    def fill_additional_fields(self):
        """Ek alanları doldurur"""
        try:
            # Telefon numarası alanı
            phone_inputs = self.driver.find_elements(By.XPATH, "//input[contains(@id, 'phone') or contains(@name, 'phone')]")
            for phone_input in phone_inputs:
                if not phone_input.get_attribute('value'):
                    phone_input.send_keys("+90 555 123 4567")  # Örnek telefon
            
            # Cover letter alanı
            cover_letter_areas = self.driver.find_elements(By.XPATH, "//textarea[contains(@id, 'cover') or contains(@name, 'cover')]")
            for textarea in cover_letter_areas:
                if not textarea.get_attribute('value'):
                    textarea.send_keys(self.config.COVER_LETTER_TEMPLATE.strip())
                    
        except Exception as e:
            logger.warning(f"⚠️ Ek alan doldurma hatası: {str(e)}")
    
    def random_delay(self):
        """Rastgele bekleme süresi"""
        delay = random.uniform(
            self.config.MIN_DELAY_BETWEEN_APPLICATIONS, 
            self.config.MAX_DELAY_BETWEEN_APPLICATIONS
        )
        logger.info(f"⏰ {delay:.1f} saniye bekleniyor...")
        time.sleep(delay)
    
    def save_session_data(self):
        """Oturum verilerini kaydet"""
        try:
            session_data = {
                'timestamp': datetime.now().isoformat(),
                'applications_count': self.applications_count,
                'applied_jobs': self.applied_jobs,
                'failed_jobs': self.failed_jobs
            }
            
            with open('linkedin_session.json', 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"💾 Oturum verileri kaydedildi: {self.applications_count} başvuru")
            
        except Exception as e:
            logger.error(f"❌ Veri kaydetme hatası: {str(e)}")
    
    def run_job_application_process(self) -> bool:
        """Ana iş başvuru sürecini çalıştırır"""
        try:
            # Driver'ı başlat
            self.driver = self.setup_driver()
            
            # LinkedIn'e giriş yap
            if not self.login_to_linkedin():
                return False
            
            # Her anahtar kelime ve lokasyon kombinasyonu için arama yap
            for keyword in self.config.SEARCH_KEYWORDS:
                for location in self.config.LOCATIONS:
                    if self.applications_count >= self.config.MAX_APPLICATIONS_PER_DAY:
                        logger.info(f"🎯 Günlük maksimum başvuru sayısına ulaşıldı: {self.applications_count}")
                        break
                    
                    # İş ara
                    if self.search_jobs(keyword, location):
                        # İlanları al
                        jobs = self.get_job_listings()
                        
                        # Her ilana başvur
                        for job in jobs:
                            if self.applications_count >= self.config.MAX_APPLICATIONS_PER_DAY:
                                break
                                
                            self.apply_to_job(job)
                            self.random_delay()
                    
                    if self.applications_count >= self.config.MAX_APPLICATIONS_PER_DAY:
                        break
            
            # Sonuçları rapor et
            self.print_final_report()
            self.save_session_data()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Ana süreç hatası: {str(e)}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("🔚 Tarayıcı kapatıldı")
    
    def print_final_report(self):
        """Final raporunu yazdırır"""
        logger.info("=" * 50)
        logger.info("📊 GÜNLÜK BAŞVURU RAPORU")
        logger.info("=" * 50)
        logger.info(f"✅ Toplam Başvuru: {self.applications_count}")
        logger.info(f"❌ Başarısız Başvuru: {len(self.failed_jobs)}")
        logger.info(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.applied_jobs:
            logger.info("\n📝 Başvuru Yapılan İşler:")
            for job in self.applied_jobs:
                logger.info(f"  • {job['title']} - {job['company']}")
        
        logger.info("=" * 50)
