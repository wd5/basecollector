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
          }
     ]
    }
]
_sitename = u'http://www.timeout.ru'
_links_filename = 'links.txt'
_output_filename = 'results__%s__%s.json'
_save_evry = 100

def create_links():
    u"""Создаем файл ссылок для последующего парсинга"""
    def parse_network(url):
        u"""Для сети заведений возвращает ссылки на каждое заведение из сети"""
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
        g.go(_sitename+'/books/list/51/page/1:100/')
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
    u"""Из каждой ссылки выдирает информацию о компании"""
    def save(results, start, end):
        u"""Сохраняет результаты в файл"""
        text = json.dumps(contacts)
        f = open(_output_filename % (start, end), 'w')
        f.write(text)
        f.close()

    contacts = [
        {'name': u'Книжные магазины',
         'city': u'Москва',
         'additional': u'Книжные магазины',
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
            save(contacts, start_line, count)
            break
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

        #защита от вылета. сохраняем каждые _save_evry и не сохраняем на первой
        if (count-start_line) % _save_evry == 0 and (count != start_line):
            save(contacts, last_saved, count)
            last_saved = count
            contacts[0]['companies'] = []
        #сохраняем в конце
        if (count + 1) == file_length:
            save(contacts, last_saved, count)
            contacts[0]['companies'] = []

        sleep(0.1)

def beautify():
    u"""По-русски вывести json"""
    convert_json = open(_output_filename).read().decode("unicode_escape").encode("utf8")
    open(_output_filename, 'wb').write(convert_json)

if __name__ == '__main__':
    create_links()
    parse()
#    beautify()