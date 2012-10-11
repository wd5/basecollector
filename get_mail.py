# -*- coding: utf-8 -*-
from grab import Grab, base
import re
import time

def get_mail(site):
    g = Grab()
    print u"Ищу на сайте %s" % site
    email = False
    try:
        g.go('http://' + site)
        try:
            email = g.rex(re.compile("[-a-z0-9!#$%&'*+/=?^_`{|}~]+(\.[-a-z0-9!#$%&'*+/=?^_`{|}~]+)*@([a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*([a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*(aero|arpa|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|[a-z][a-z])")).group()
        except :
            print "На главной мыла не нашел"
            try:
                g.go(g.xpath(u'//a[contains(text(), "онтакт")]').get('href'))
                email = g.rex(re.compile("[-a-z0-9!#$%&'*+/=?^_`{|}~]+(\.[-a-z0-9!#$%&'*+/=?^_`{|}~]+)*@([a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*([a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*(aero|arpa|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|[a-z][a-z])")).group()
            except :
                print "Раздел контакты не найден"
                try:
                    g.go('http://' + site + '/contacts')
                    email = g.rex(re.compile("[-a-z0-9!#$%&'*+/=?^_`{|}~]+(\.[-a-z0-9!#$%&'*+/=?^_`{|}~]+)*@([a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*([a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*(aero|arpa|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|[a-z][a-z])")).group()
                except :
                    print "Попытка пройти по /contacts не удалась"
        if not email:
            try:
                g.go(g.xpath(u'//a[contains(text(), "нас")]').get('href'))
                email = g.rex(re.compile("[-a-z0-9!#$%&'*+/=?^_`{|}~]+(\.[-a-z0-9!#$%&'*+/=?^_`{|}~]+)*@([a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*([a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*(aero|arpa|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|[a-z][a-z])")).group()
            except :
                print "Раздел о нас не найден"
                try:
                    g.go(g.xpath(u'//a[contains(text(), "проезд")]').get('href'))
                    email = g.rex(re.compile("[-a-z0-9!#$%&'*+/=?^_`{|}~]+(\.[-a-z0-9!#$%&'*+/=?^_`{|}~]+)*@([a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*([a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*(aero|arpa|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|[a-z][a-z])")).group()
                except :
                    print "Раздел схема проезда не найден"
        else:
            print u"Нашел мыло: %s" % email
    except :
        print u"Ошибка на сайте %s" % site
    print "-------------"
    return email