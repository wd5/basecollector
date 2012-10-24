# -*- coding: utf-8 -*-
import os
from datetime import datetime

os.environ['PYTHONPATH'] = '/Users/vladimir/PycharmProjects/basecollector'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.contrib.auth.models import User

from django.db import models

class Company_DB(models.Model):
    u'Компания для обзвона'
    date_time_created = models.DateTimeField(auto_now_add = True, verbose_name= u'Дата внесения компании в БД')
    name = models.CharField(max_length = 100, verbose_name= u'Название организации')
    address = models.CharField(max_length = 100, verbose_name= u'Адрес', blank= True, null=True)
    #будет ли показываться? становится False в случае накопившихся сообщениях об ошибке из CompanyFeedback
    active = models.BooleanField(default= True, verbose_name= u'Активная?')
    #удалена ли?
    deleted = models.BooleanField(default= False, verbose_name= u'Удалена?')
    packet = models.ForeignKey('Packet', verbose_name= u'Категория')
    url = models.URLField(verbose_name= u'Сайт', blank= True, null= True)
    email = models.EmailField(verbose_name= u'E-mail', blank= True, null= True)
    last_validated = models.DateTimeField(verbose_name=u'Последний раз звонили', blank= True, default= datetime.now())

    class Meta:
        verbose_name = u'База компаний'
        verbose_name_plural = u'База компаний'
        db_table = 'company_base_company_db'

    def __unicode__(self):
        return u'%d. %s'%(self.pk, self.name)

class Packet(models.Model):
    u'Пакет из базы'
    date_time_created = models.DateTimeField(auto_now_add = True, verbose_name= u'Время создания')
    name = models.CharField(max_length=40, unique=True, verbose_name=u'Название пакета')
    city = models.ForeignKey('City', verbose_name=u'Город/Респ/Край/Обл')
    #какой компании принадлежит запись
    company = models.ManyToManyField('company.Company', through='target.BoughtPackets',
        blank= True, null= True, verbose_name=u'Компании владельцы')
    tags = models.ManyToManyField('Tags', verbose_name=u'Облако тегов для поиска', blank=True, null=True)
    private = models.BooleanField(default= False, verbose_name=u'Приватный пакет')
    description = models.CharField(max_length=300, verbose_name=u'Описание', blank=True, null=True)
    price_100 = models.IntegerField(default=30, verbose_name=u'Цена за 100 шт.')

    class Meta:
        verbose_name = u'Пакет'
        verbose_name_plural = u'Пакеты'
        db_table = 'company_base_packet'

    def __unicode__(self):
        return u'%d. %s' % (self.pk, self.name)

    def get_company_db_count(self):
        u'Сколько записей есть в Company_DB по этому пакету'
        return self.company_db_set.count()


class Tags(models.Model):
    u'Тэги для поиска'
    date_time_created = models.DateTimeField(auto_now_add = True, verbose_name= u'Время создания')
    name = models.CharField(max_length=40, unique=True, verbose_name=u'Название')

    class Meta:
        verbose_name = u'Тег'
        verbose_name_plural = u'Теги'
        db_table = 'company_base_packet_tags'

    def __unicode__(self):
        return u'%d. %s' % (self.pk, self.name)


class Phone_Company_DB(models.Model):
    u'Телефонный номер компании'
    date_time_created = models.DateTimeField(auto_now_add = True, verbose_name= u'Время создания')
    company_db = models.ForeignKey('Company_DB', verbose_name= u'Компания владелец')
    phone = models.CharField(max_length = 20, verbose_name= u'Телефон')

    class Meta:
        verbose_name = u'Телефон'
        verbose_name_plural = u'Телефоны'
        db_table = 'company_base_phone_company_db'

    def __unicode__(self):
        return u'%d. номер телефона %s' % (self.pk, self.company_db)


class Extension_Phone(models.Model):
    u'Дополнительный номер к телефону'
    date_time_created = models.DateTimeField(auto_now_add = True, verbose_name= u'Время создания')
    phone = models.ForeignKey('Phone_Company_DB', verbose_name= u'Телефон')
    extension = models.CharField(max_length = 10, verbose_name= u'Добавочный телефон')

    class Meta:
        verbose_name = u'Доп. телефон'
        verbose_name_plural = u'Доп. телефоны'
        db_table = 'company_base_extension_phone'

    def __unicode__(self):
        return u'%d. дополнительный номер к %s ' % (self.pk, self.phone)
