# -*- coding: utf-8 -*
import os
import logging
from grab import Grab

logging.basicConfig(level=logging.DEBUG)

# Config variables
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
SITE_URL = 'http://www.restoran.ru/msk/catalog/restaurants/all'
LOG_DIR = os.path.join(PROJECT_PATH, 'log')

f = open('clubs', 'r')
for url in f.readlines():
    g = Grab()
    g.go(url)
    print url
    try:
        phone = g.xpath('//*[@id="content"]/div[2]/div/ul/li[2]').text #Телефон
    except :
        continue
    try:
        name = g.xpath('//h1[@class="b-object-title"]').text #Название
    except :
        continue
    try:
        address = g.xpath('//address').text #Адрес
    except :
        pass
    try:
        site = g.xpath('//*[@id="content"]/div[2]/div/ul/li[3]/a').text #Сайт
    except :
        pass
