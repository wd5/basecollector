# -*- coding: utf-8 -*
import os
import logging
from grab import Grab
import time
import old.api.utils
from old.api.models import Target, Phone

logging.basicConfig(level=logging.DEBUG)

# Config variables
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
SITE_URL = 'http://www.rabota.ru/v3_searchVacancyByCompanyResults.html?wt=f&c=1&branch%5B0%5D=193&fa=f&pp=20&ov=1&start='
LOG_DIR = os.path.join(PROJECT_PATH, 'log')

g = Grab()
g2 = Grab()
for page in xrange(0,1050,20):
    print page
    g.go(SITE_URL + str(page))
    for item in g.xpath_list('//*[@class="name_vc"]/a'):
        g2.go(item.get('href'))
        target = Target()
        target.category_id = 15
        print g2.xpath('//*[@class="mb_20 pl22"]/p').text
        target.name = g2.xpath('//*[@class="mb_20 pl22"]/p').text
        target.comment = g2.xpath('//*[@class="mt_10 text_14"]').text
        repeat = False

        for count, contact in enumerate(g2.xpath_list('//*[@class="pers pl15"]/p'), 1):
            try:
                if u'Телефон' in contact.find('./span').text:
                    phones = g2.xpath('//*[@class="pers pl15"]/p[' + str(count) + ']/text()').split(',')
                    for phone in phones:
                        if phone:
                            if Phone.objects.filter(phone=old.api.utils.custom_phone(phone)):
                                repeat = True
                elif u'Адрес' in contact.find('./span').text:
                    target.address = g2.xpath('//*[@class="pers pl15"]/p[' + str(count) + ']/text()').encode('utf-8')
                elif u'Сайт' in contact.find('./span').text:
                    target.site = g2.xpath('//*[@class="pers pl15"]/p[' + str(count) + ']/noindex/a').get('href')
            except Exception, e:
                print e
        if not repeat:
            if phones:
                target.save()
                for phone in phones:
                    if phone:
                        print phone
                        print old.api.utils.custom_phone(phone)
                        try:
                            Phone(phone=old.api.utils.custom_phone(phone), target = target).save()
                        except Exception, e:
                            print "__________________@@@@@@@@@"
                            print e
                            print "@@@@@@@@@@@@@______________"
        phones = False
        time.sleep(2)
    time.sleep(5)
