#coding: utf-8
from lxml import etree
from grab import Grab
from grab.error import GrabTimeoutError, DataNotFound
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
          }
     ]
    }
]
_sitename = u'http://www.timeout.ru'
_links_filename = 'links.txt'
_output_filename = 'results_restorans.json'

def create_links():
    u"""Создаем файл ссылок для последующего парсинга"""
    def parse_network(url):
        u"""Для сети ресторанов возвращает ссылки на каждый ресторан из сети"""
        gg  = Grab()
        gg.go(url)
        network_links_list = []
        network_links = gg.xpath_list('//div[@class="z-list"]/h3/a')
        for network_link in network_links:
            print u'\t%s' % network_link.get('href')
            network_links_list.append(_sitename + network_link.get('href'))
        return network_links_list

    g = Grab()
    try:
        g.go(_sitename+'/restaurant/list/71/page/1:30/')
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
    text_data = u'\n'.join(links_list)
    f = open(_links_filename, 'w')
    f.write(text_data)
    f.close()


def parse():
    contacts = [
        {'name': u'Рестораны и бары',
         'city': u'Москва',
         'additional': u'',
         'companies': [],
         }
    ]
    f = open('links.txt', 'r')
    for url in f.readlines():
        print url
        g = Grab()
        try:
            g.go(url)
        except GrabTimeoutError:
            continue
        company = dict()
        try:
            company['name'] = clear_string(g.xpath('//div[@class="headingH2"]/h1').text)
            company['address'] = clear_string(g.xpath('//span[@class="street-address"]').text)
            company['url'] = clear_string(g.xpath('//p/noindex/a').text) or u''
            company['email'] = get_mail(company['url']) or u''
            raw_phone = clear_string(g.xpath('//span[@class="tel"]').text)
            company['phones'] = []
            for phone in raw_phone.split(','):
                company['phones'].append(format_phone(phone))
        except DataNotFound:
            pass

        contacts[0]['companies'].append(company)
    text = json.dumps(contacts)
    f = open(_output_filename, 'w')
    f.write(text)
    f.close()

def beautify():
    convert_json = open(_output_filename).read().decode("unicode_escape").encode("utf8")
    open(_output_filename, 'wb').write(convert_json)

if __name__ == '__main__':
#    create_links()
    parse()
#    beautify()