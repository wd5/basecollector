#coding: utf-8
from time import sleep
from lxml import etree
from grab import Grab
from grab.error import *
import json
from utils import format_phone, get_mail, clear_string

parsed_packet_example = [
    {'name': u'',
     'city': u'',
     'additional': u'',
     'companies': [
         {'name': u'',
          'address': u'',
          'url': u'',
          'email': u'',
          'phones': [u'',],
          'additional': u'',
          }
     ]
    }
]

_links_filename = 'links.txt'
_output_filename = 'results__%s__%s.json'
_save_evry = 150
_sitename = u'http://avtostop.idainet.ru'
_link_postfix = u'/afirms.htm'

u'''
Подключаем jquery на сайт
var newScript = document.createElement("script");
newScript.type = "text/javascript";
newScript.src = "https://ajax.googleapis.com/ajax/libs/jquery/1.8/jquery.min.js";
var first = document.getElementsByTagName("head")[0].firstChild;
document.getElementsByTagName("head")[0].insertBefore(newScript, first);

со страницы пиздим ссылки
$('.Page p a').each(function(key, value) {console.log($(value).attr('href'))})
'''


def parse():
    u"""Из каждой ссылки выдирает информацию о компании"""
    def save(results, start, end):
        u"""Сохраняет результаты в файл"""
        text = json.dumps(contacts)
        f = open(_output_filename % (start, end), 'w')
        f.write(text)
        f.close()

    contacts = [
        {'name': u'Автостоянки',
         'city': u'Москва',
         'additional': u'',
         'companies': [],
         }
    ]
    f = open(_links_filename, 'r')
    file_length = len(f.readlines())
    f.close()
    f = open(_links_filename, 'r')
    start_line = 0
    last_saved = start_line
    for count, url in enumerate(f.readlines()[start_line:], start=start_line):
        print u'%d. %s' % (count, url)
        g = Grab()
        try:
            g.go(url)
        except (GrabNetworkError, GrabTimeoutError, GrabConnectionError, GrabAuthError) as details:
            print details
            save(contacts, last_saved, count)
            break
        company = dict()
        try:
            company['name'] = g.xpath('//h1[@class="zagstr"]').text
            address = g.xpath('//div[@class="Page"]/ul/li')
            company['address'] = etree.tostring(address, encoding=unicode, method="text").split(u'\n')[3][7:]
            company['url'] = u''
            company['email'] = u''
            company['additional'] = u''
            raw_phone = clear_string(g.xpath('//div[@class="Page"]/ul/li/b').text)
            raw_phone = format_phone(raw_phone)
            company['phones'] = [raw_phone,]
        except DataNotFound:
            pass

        contacts[0]['companies'].append(company)

        #защита от вылета. сохраняем каждые _save_evry и не сохраняем на первой
        if count % _save_evry == 0 and (count != start_line):
            save(contacts, last_saved, count)
            last_saved = count
            contacts[0]['companies'] = []
        #сохраняем в конце
        if (count + 1) == file_length:
            save(contacts, last_saved, count)
            contacts[0]['companies'] = []

        sleep(1)

if __name__ == '__main__':
    parse()