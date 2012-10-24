# -*- coding: utf-8 -*
from selenium import webdriver
from old.api.models import Target, Phone
import time
from old.api.utils import custom_phone

i = 45 # Число страниц

browser = webdriver.Firefox() # Запускаем локальную сессию firefox
while i >= 0:
    print i
    url = "http://maps.2gis.ru/#/?history=project/moscow/center/37.598752%2C55.739112/zoom/13/state/firms/what/%D0%B0%D0%B2%D1%82%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%BA%D0%B0/action/search/page/" + str(i) + "/sort/relevance/ppage/1"
    browser.get(url) # Загружаем страницу
    time.sleep(5) # Пусть страница загрузится. Вдруг у нас медленный интернет...
    # Здесь будет код
    place_blocks = []
    place_blocks.append(browser.find_elements_by_xpath('//*[@id="cat-results-list-first"]/div'))
    place_blocks.append(browser.find_elements_by_xpath('//*[@id="cat-results-list-other"]/div'))
    for place_block in place_blocks:
        for div_peace in place_block:
            target = Target()
            repeate = False
            phones = []
            target.category_id = 4
            target.address = div_peace.find_element_by_class_name('dg-firm-address').text
            div_peace.find_element_by_xpath('./div/h2/a').click()
            target.name = div_peace.find_element_by_class_name('link-text').text
            try:
                target.email = div_peace.find_element_by_class_name('dg-row-email').text
            except :
                pass
            try:
                target.site = div_peace.find_element_by_class_name('dg-row-website').text
            except :
                pass
            try:
                phones_src = div_peace.find_elements_by_class_name('dg-row-phone')
                if phones_src:
                    for phone_src in phones_src:
                        phone = custom_phone(phone_src.text)
                        phones.append(phone)
                        if Phone.objects.filter(phone=phone):
                            print "Повторяется"
                            repeate = True
                else:
                    repeate = True
            except :
                repeate = True
            if not repeate:
                target.save()
                for phone in phones:
                    Phone(phone=phone, target = target).save()
    i -= 1
