# -*- coding: utf-8 -*-
import re

def new_phone(phone):
    phone = re.sub("\D", "", phone)
    if len(phone) == 10:
        new_phone = '+7(%s)%s-%s-%s' % (phone[:3], phone[3:-4], phone[6:-2], phone[8:])
        return new_phone

def custom_phone(phone):
    try:
        raw_phone = phone.strip().replace(' ','')
        raw_phone = re.compile('[+\d\-\(\)]*\d').match(raw_phone).group()
        #(495)565-37-70
        if re.compile('^\(\d{3}\)\d{3}-\d{2}-\d{2}$').match(raw_phone):
            return '+7' + raw_phone
        #8-926-797-22-92
        elif re.compile('^\d{1}-\d{3}-\d{3}-\d{2}-\d{2}$').match(raw_phone):
            return re.sub('^\d{1}-(?P<code>\d{3})-(?P<phone1>\d{3})-(?P<phone2>\d{2})-(?P<phone3>\d{2})$', '+7(\g<code>)\g<phone1>-\g<phone2>-\g<phone3>', raw_phone)
        #565-37-70
        elif re.compile('^\d{3}-\d{2}-\d{2}$').match(raw_phone):
            return re.sub('^(?P<phone1>\d{3})-(?P<phone2>\d{2})-(?P<phone3>\d{2})$', '+7(495)\g<phone1>-\g<phone2>-\g<phone3>', raw_phone)
        #8(495)565-37-70
        elif re.compile('^8\(\d{3}\)\d{3}-\d{2}-\d{2}$').match(raw_phone):
            return '+7' + raw_phone[1:]
        #(495)-797-2-292
        elif re.compile('^\(\d{3}\)\d{3}-\d{1}-\d{3}$').match(raw_phone):
            spphone = raw_phone.split('-')
            print '+7' + spphone[0] + '-' + spphone[1] + spphone[2][:1] + '-' + spphone[2][1:]
        #(4967)62-68-50
        elif re.compile('^\(\d{4}\)\d{2}-\d{2}-\d{2}$').match(raw_phone):
            return '+7' + raw_phone
        #+7(495)565-37-70
        elif re.compile('^+7\(\d{3}\)\d{3}-\d{2}-\d{2}$').match(raw_phone):
            return raw_phone
        else:
            return new_phone(raw_phone)
    except Exception, e:
        raw_phone = phone.strip().replace(' ','')
        return new_phone(raw_phone)

