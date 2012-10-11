# -*- coding: utf-8 -*
from selenium import webdriver
from api.models2 import Company_DB, Phone_Company_DB
import time
from api.utils import custom_phone

i = 100 # Число страниц

browser = webdriver.Firefox() # Запускаем локальную сессию firefox
while i >= 0:
    print i
    url = "http://maps.2gis.ru/#/?history=project/moscow/center/37.649964%2C55.726781/zoom/11/state/firms/what/%D1%81%D1%82%D1%80%D0%BE%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D1%82%D0%B2%D0%BE/action/search/page/" + str(i) + "/sort/relevance/ppage/1"
    browser.get(url) # Загружаем страницу
    time.sleep(5) # Пусть страница загрузится. Вдруг у нас медленный интернет...
    # Здесь будет код
    place_blocks = []
    place_blocks.append(browser.find_elements_by_xpath('//*[@id="cat-results-list-first"]/div'))
    place_blocks.append(browser.find_elements_by_xpath('//*[@id="cat-results-list-other"]/div'))
    for place_block in place_blocks:
        for div_peace in place_block:
            company_db = Company_DB()
            repeate = False
            phones = []
            company_db.packet_id = 4
            company_db.address = div_peace.find_element_by_class_name('dg-firm-address').text
            div_peace.find_element_by_xpath('./div/h2/a').click()
            company_db.name = div_peace.find_element_by_class_name('link-text').text
            try:
                company_db.email = div_peace.find_element_by_class_name('dg-row-email').text
            except :
                pass
            try:
                company_db.site = div_peace.find_element_by_class_name('dg-row-website').text
            except :
                pass
            try:
                phones_src = div_peace.find_elements_by_class_name('dg-row-phone')
                if phones_src:
                    for phone_src in phones_src:
                        phone = custom_phone(phone_src.text)
                        phones.append(phone)
                        if Phone_Company_DB.objects.filter(phone=phone):
                            print "Повторяется"
                            print phone
                            print Phone_Company_DB.objects.filter(phone=phone)
                            print Phone_Company_DB.objects.filter(phone=phone)[0].company_db
                            repeate = True
                else:
                    repeate = True
            except :
                repeate = True
            if not repeate:
                company_db.save()
                for phone in phones:
                    Phone_Company_DB(phone=phone, company_db = company_db).save()
    i -= 1
