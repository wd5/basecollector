#coding: utf-8
from lxml import etree
from grab import Grab
from grab.error import GrabTimeoutError
import json
from utils import format_phone, get_mail

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

def run():
    u"""
    со страницы пиздим ссылки
     $('#block td a[target="_blank"]').each(function(key, value) {console.log($(value).attr('href'))})
    """
    f = open('/home/hellpain/dev/siteparser/med_clinik/management/commands/links.txt', 'r')
    contacts = [
        {'name': u'Медицинские клиники',
         'city': u'Москва',
         'additional': u'',
         'companies': [],
         }
    ]
    for url in f.readlines():
        print url
        g = Grab()
        try:
            g.go(url)
        except GrabTimeoutError:
            continue
        data = g.xpath('//dl[@class="doctor_info2"]')
        content = etree.tostring(data, encoding=unicode, method="text").replace(u'\t', u'')
        content_list = content.split(u'\n')
        company = dict()
        company['name'] = g.xpath('//div[@id="centerspace"]/h1').text
        company['url'] = g.xpath('//div[@class="clinic_info clinic_text"]/b/a').text
        company['email'] = get_mail(company['url']) or u''
        for count, value in enumerate(content_list):
            value = value.strip()
            if value == u'Телефон':
                company['phones'] = []
                for phone in content_list[count+1].split(u','):
                    phone = format_phone(phone)
                    company['phones'].append(phone)
            if value == u'Адрес':
                company['address'] = content_list[count+1]
        contacts[0]['companies'].append(company)
    text = json.dumps(contacts)
    f = open('results_med_clinik.json', 'w')
    f.write(text)
    f.close()

if __name__ == '__main__':
    run()