# -*- coding: utf-8 -*
from selenium import webdriver
from selenium import selenium
from api.utils import get_mail
from api.models import Target, Phone
import time

fp = webdriver.FirefoxProfile()
fp.add_extension(extension='/Users/vladimir/PycharmProjects/basecollector/firebug-1.8.0.xpi')
fp.set_preference("extensions.firebug.currentVersion", "1.8.4") #Avoid startup screen
browser = webdriver.Firefox(firefox_profile=fp)
url = "http://maps.yandex.ru/?text=%D0%B1%D0%B0%D1%80%D1%8B%20%D0%BA%D0%B0%D1%84%D0%B5%20%D1%80%D0%B5%D1%81%D1%82%D0%BE%D1%80%D0%B0%D0%BD%D1%8B%20%D0%A6%D0%90%D0%9E&sll=37.626572999999986%2C55.87024899999358&sspn=0.588455%2C0.212726&z=12&results=400&ll=37.613988%2C55.753706&spn=0.294228%2C0.106683&l=map"
#url = "http://maps.yandex.ru/?text=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%20%D0%B0%D0%B2%D1%82%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%BA%D0%B0&sll=37.61767099999998%2C55.75577168714407&sspn=3.010254%2C0.983540&z=9&results=20&ll=37.573851%2C55.751572&spn=3.010254%2C0.983647&l=map"
browser.get(url) # Загружаем страницу
time.sleep(10)
parking_list = browser.find_elements_by_class_name('b-serp-item')
count = 0
for parking in parking_list:
    parking.click()
    name = parking.find_element_by_class_name('b-link').text
    try:
        address = ''.join(browser.find_element_by_class_name('b-serp-contacts__line').text.split(',')[2:])
        print u"Адрес: Москва, %s" % ''.join(browser.find_element_by_class_name('b-serp-contacts__line').text.split(',')[2:])
    except :
        print "Адреса нету"
    #pos = p = re.compile('pos=.*\'').search(parking.get_attribute('onclick')).group()[5:-1]
    try:
        phone = browser.find_element_by_class_name('b-serp-contacts__item').text.strip().replace(' ','')
        print phone
    except :
        phone = False
        print "Телефона нету"
    try:
        baloon = browser.find_element_by_class_name('b-balloon')
        site = baloon.find_element_by_class_name('b-serp-url__link').text
        print site
        #print u"Сайт: %s" % browser.find_element_by_class_name('b-serp-url__link').text
    except :
        site = False
        print "Сайта нету"
    if phone:
        if not Phone.objects.filter(phone=phone):
            if site:
                target = Target(name=name, address=address, city=u'Москва', category_id=2)
                target.site = site
                mail = get_mail(site)
                if mail:
                    target.email = mail
                target.save()
                Phone(phone=phone, target = target).save()
                count +=1
                print "Сохранил в базу! - %s" % count
            else:
                target = Target(name=name, address=address, city=u'Москва', category_id=2)
                target.save()
                print "Сохранил в базу! - %s" % count
                Phone(phone=phone, target = target).save()
                count +=1
    time.sleep(1)
    print "--------------"
#browser.find_elements_by_class_name('b-form-button')[2].click()
