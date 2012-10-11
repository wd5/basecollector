# -*- coding: utf-8 -*-
from grab import Grab, base
from lxml import etree
import logging
import os
import re
import time
from api.utils import custom_phone
from api.models import Target, Phone

#logging.basicConfig(level=logging.DEBUG)

# Config variables
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
SITE_URL = 'http://www.restoran.ru/msk/catalog/restaurants/all'
LOG_DIR = os.path.join(PROJECT_PATH, 'log')
count = 0

for page in range(1,83):
    print "Страница %s" % page
    g = Grab()
#    g.setup(debug_post=True, log_dir=LOG_DIR, connect_timeout=60, timeout=60)
    g.go(SITE_URL + '?page=%s' % page)
    for tr_element in g.xpath_list('//table[@class="obj_list_table"]/tr'):
        try:
            name = tr_element.find('./td/table/tr/td/a').text
            internal_url = tr_element.find('./td/table/tr/td/a').get('href')
            phones = []
            target = Target()
            target.category_id = 2
            target.name = name
            repeate = False
        except :
            pass
        try:
            tdelement = etree.tostring(tr_element.find('./td'), encoding=unicode)
            if u'Адрес' in tdelement:
                target.address = tr_element.find('./td[2]').text[9:]
                #print tr_element.find('./td[2]').text
            elif u'Телефон' in tdelement:
                for part in tr_element.find('./td[2]').text.split(','):
                    phone = custom_phone(part)
                    phones.append(phone)
                    if Phone.objects.filter(phone=phone):
                        repeate = True
                if not repeate:
                    g2 = Grab()
                    g2.go('http://www.restoran.ru' + internal_url)
                    g2.setup(debug_post=True, log_dir=LOG_DIR, connect_timeout=60, timeout=60)
                    site = g2.xpath(u'//td[contains(text(), "Сайт")]/following::a').text
                    if not 'restoran.ru' in site:
                        try:
                            g2.go('http://' + site)
                            target.site = site
                            try:
                                email = g2.rex(re.compile("[-a-z0-9!#$%&'*+/=?^_`{|}~]+(\.[-a-z0-9!#$%&'*+/=?^_`{|}~]+)*@([a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*([a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*(aero|arpa|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|[a-z][a-z])")).group()
                                target.email = email
                            except :
                                try:
                                    g2.go(g2.xpath(u'//a[contains(text(), "онтакт")]').get('href'))
                                    email = g2.rex(re.compile("[-a-z0-9!#$%&'*+/=?^_`{|}~]+(\.[-a-z0-9!#$%&'*+/=?^_`{|}~]+)*@([a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*([a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*(aero|arpa|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|[a-z][a-z])")).group()
                                    target.email = email
                                except :
                                    pass
                        except :
                            pass
                    target.save()
                    for phone in phones:
                        Phone(phone=phone, target = target).save()
                    count +=1
                    print "Записано клиентов: %s" % count
                else:
                    print "repeate"

                    #print tr_element.find('./td[2]').text
        except Exception, e:
            print "++++++"
            try:
                print e
            except :
                try:
                    print e.encode('utf8')
                except :
                    pass
            pass
        #print etree.tostring(i, pretty_print=True, encoding=unicode)
    time.sleep(1)
    """
    for p_element in g.xpath_list('//table[@class="ver9_block"]/tr/td/p'):
        repeate = False
        try:
            target = Target()
            phones = []
            target.category_id = 2
            internal_url = p_element.find('./a').get('href')
            target.name = p_element.find('./a/strong/font').text
            for strong_element in p_element.xpath('./strong'):
                strelement = etree.tostring(strong_element, encoding=unicode)
                if u'Адрес' in strelement:
                    target.address = strong_element.tail[9:]
                if u'Телефон' in strelement:
                    for part in strong_element.tail.split(','):
                        phone = custom_phone(part)
                        phones.append(phone)
                        if Phone.objects.filter(phone=phone):
                            repeate = True
                        #phone = Phone(phone=custom_phone(part), target = target).save()
            if not repeate:
                target.save()
                for phone in phones:
                    Phone(phone=phone, target = target).save()
        except Exception, e:
            print e
    time.sleep(10)
        #print etree.tostring(i, pretty_print=True, encoding=unicode)
        #for a in i.xpath('//a'):
        #    print etree.tostring(a, pretty_print=True, encoding=unicode)
        #for b in i.xpath('//strong'):
        #    print b.text
        #    if u'Адрес' in etree.tostring(b, encoding=unicode):
        #        print b.tail
     #   print etree.tostring(i, pretty_print=True)
     #   print "---"
     """
