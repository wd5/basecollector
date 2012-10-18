#coding: utf-8
import re
from grab import Grab


def format_phone(phone):
    old_phone = phone
    phone = re.sub(u'\D', u'', phone)
    tt = u''
    if len(phone) == 10:
        new_phone = u'+7(%s)%s-%s-%s' % (phone[:3], phone[3:6], phone[6:8], phone[8:])
        return new_phone
    elif len(phone) == 11 and (phone[0] == u'7' or phone[0] == u'8'):
        new_phone = u'+7(%s)%s-%s-%s' % (phone[1:4], phone[4:7], phone[7:9], phone[9:])
        return new_phone
    else:
        return old_phone


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
                g.go(g.xpath('//a[contains(text(), "онтакт")]'.decode('utf8')).get('href'))
                print u"Найден раздел контакты : %s" % g.xpath('//a[contains(text(), "онтакт")]'.decode('utf8')).get('href')
                try:
                    email = g.rex(re.compile("[-a-z0-9!#$%&'*+/=?^_`{|}~]+(\.[-a-z0-9!#$%&'*+/=?^_`{|}~]+)*@([a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*([a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*(aero|arpa|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|[a-z][a-z])")).group()
                except:
                    print u"В разделе контакты мыло не найдено"
            except:
                print u"Раздел контакты не найден"
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