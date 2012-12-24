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
_save_evry = 200

START_LINE = 0 #НАЧИНАЕМ С НУЛЯ ИЛИ ВЫСТАВЛЯЕМ НА НУЖНУЮ ПОЗИЦИЮ ПОСЛЕ ВЫЛЕТА
_sitename = u'http://www.vsesadiki.ru/'


u'''
Подключаем jquery на сайт
var newScript = document.createElement("script");
newScript.type = "text/javascript";
newScript.src = "https://ajax.googleapis.com/ajax/libs/jquery/1.8/jquery.min.js";
var first = document.getElementsByTagName("head")[0].firstChild;
document.getElementsByTagName("head")[0].insertBefore(newScript, first);

со страницы пиздим ссылки
$('.joomlatable a').each(function (index) { console.log($(this).attr('href')) } );
'''


def create_links():
    u"""Создаем файл ссылок для последующего парсинга"""
    def parse_network(url):
        u"""Для сети заведений возвращает ссылки на каждое заведение из сети"""
        gg  = Grab()
        while True:
            try:
                gg.go(url)
                break
            except (GrabNetworkError, GrabTimeoutError, GrabConnectionError, GrabAuthError):
                print u'Терпим'
                sleep(5)
        network_links_list = []
        network_links = gg.xpath_list('//div[@class="z-list"]/h3/a')
        for network_link in network_links:
            print u'\t%s' % network_link.get('href')
            network_links_list.append(_sitename + network_link.get('href'))
        return network_links_list

    g = Grab()
    try:
        g.go(_sitename)
    except GrabTimeoutError:
        print u'time out'
        exit()
    links = g.xpath_list('//div[@class="z-list"]/h3/a')
    links_list = []
    for link in links:
        print link.get('href')
        if u'place' in link.get('href'):
            print u'Добавили\n'
            links_list.append(_sitename+link.get('href'))
        if u'network' in link.get('href'):
            print u'Ищем в network'
            links_list = links_list + parse_network(_sitename+link.get('href'))
            print u'\n'
            sleep(0.1)
    text_data = u'\n'.join(links_list)
    f = open(_links_filename, 'w')
    f.write(text_data)
    f.close()


def parse():
    u"""Из каждой ссылки выдирает информацию о компании"""
    def save(results, start, end):
        u"""Сохраняет результаты в файл"""
        text = json.dumps(contacts)
        f = open(_output_filename % (start, end), 'w')
        f.write(text)
        f.close()

    contacts = [
        {'name': u'Частные детские сады',
         'city': u'Москва',
         'additional': u'',
         'companies': [],
         }
    ]
    f = open(_links_filename, 'r')
    file_length = len(f.readlines())
    f.close()
    f = open(_links_filename, 'r')
    last_saved = START_LINE
    for count, url in enumerate(f.readlines()[START_LINE:], start=START_LINE):
        print u'%d. %s' % (count, url)
        g = Grab()
        try:
            g.go(_sitename + url)
        except (GrabNetworkError, GrabTimeoutError, GrabConnectionError, GrabAuthError) as details:
            print details
            save(contacts, last_saved, count)
            break
        company = dict()
        try:
            company['name'] = clear_string(g.xpath('//h1[@class="title"]').text)
            info = g.xpath_list('//div[@class="jwts_tabbertab"]/p')
            for some_info in info:
                if not some_info.text:
                    continue
                if u'Телефон' in some_info.text:
                    company['phones'] = []
                    for phone in some_info.text.split(u','):
                        company['phones'].append(format_phone(phone))
                if u'Адрес' in some_info.text:
                    company['address'] = clear_string(some_info.text)
            company['url'] = clear_string(g.xpath('//div[@class="jwts_tabbertab"]/p/a').text) or u''
        except DataNotFound:
            pass

        contacts[0]['companies'].append(company)

        #защита от вылета. сохраняем каждые _save_evry и не сохраняем на первой
        if count % _save_evry == 0 and (count != START_LINE):
            save(contacts, last_saved, count)
            last_saved = count
            contacts[0]['companies'] = []
        #сохраняем в конце
        if count + 1 == file_length:
            save(contacts, last_saved, count)

        sleep(0.2)

if __name__ == '__main__':
#    create_links()
    parse()