#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as et
from xml.etree.ElementTree import ParseError as er

import dbf


#check dublicates
def parse_xml(fname):
    try:
        tree = et.ElementTree(file=fname)
    except er:
        exit('Parsing error')
    root = tree.getroot()
    for child in root.findall('./Custodians//CustodianElement//Owners//OwnerElement'):
        owner = child.find('Owner')
        Name = None if owner[0].find('Name') is None else owner[0].find('Name').text
        print('\tOwner type:', owner[0].tag, '\tCountStock: ', child.find('CountStock').text, '\tAccount: ', owner[0].find('Account').text, \
            '\tName: ', Name)
        
def conv(txt):
    
    return txt.encode('utf-8').decode('utf-8')

def process_dbf(fname):
    
    table = dbf.Table('dbase.dbf', 'DATE c(10); CUST_ID C(6); CUST_NAME c(70); DEPO_ID c(17);\
        KOD c(1); NAME c(254); RL c(254); R2 c(254); NALOG_CODE c(26); BORN_PLACE c(50);\
        BORN_DATE c(10); SUM_PAP n(19, 0); SUM_BLOCK n(19, 0); SUM_QUO n(19, 0); \
        OBT c(150); SUM_COST n(19, 2); PERCENT n(12, 6); BANK c(150); DIV_KIND n(1, 0);\
        SANKCII c(80)', codepage='cp1251')
       
    table.open(mode=dbf.READ_WRITE)
    rec = {}
    rec["DATE"] = '13.04.2018'
    rec["CUST_ID"] = '402842'
    rec["CUST_NAME"] = 'ТОВ "ОБ\'ЄДНАНА РЕЄСТРАЦІЙНА КОМПАНІЯ"'
    rec["DEPO_ID"] = '402842-UA10018839'
    rec["KOD"] = 'Ф'
    rec["NAME"] = 'Кос Костянтин (Україна)'
    rec["RL"] = 'Серiя ВА №111111 Видан. 04.11.1995р. Київським РВ УМВС України в Дон. обл.'
    rec["R2"] = 'пр.Пан, б25, корп.1, кв.16, м.Донецьк, Донецька область, 83001'
    rec["NALOG_CODE"] = '999999999'
    rec["BORN_PLACE"] = 'м.Донецьк 07.09.1979'
    rec["BORN_DATE"] = '08.07.1981'
    rec["SUM_PAP"] = 1020
    rec["SUM_BLOCK"] = 1020
    rec["SUM_QUO"]  = 1
    rec["OBT"] = "1020(б.р.423000);"
    rec["SUM_COST"] = 255
    rec["PERCENT"] = 0.002894
    rec["BANK"] = ""
    rec["DIV_KIND"] = 0 
    rec["SANKCII"] = ""
    table.append(rec)
    table.close()

def main():
    parse_xml('reestr.xml')
    #process_dbf('dbase.dbf')

if __name__ == "__main__":
    main()