#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as et
from xml.etree.ElementTree import ParseError as er

import dbf


owners = []

def get_field_text(node, field_name, default_value=""):
    return default_value if node.find(field_name) is None else node.find(field_name).text

def get_address(node):

    fields = ['Street', 'House', 'Aprt', 'City', 'District', 'State', 'PostCode']
    adr = []

    for field in fields:
        if node.findtext(field):
            adr.append(node.findtext(field))

    return ", ".join(adr)


#check dublicates
def parse_xml(fname):
    global owners

    try:
        tree = et.ElementTree(file=fname)
    except er:
        exit('Parsing error')
    root = tree.getroot()

    record_date = root.find('RecordDate').text[:10]

    for childs in root.findall('./Custodians//CustodianElement//OwnerElements//OwnerElement//Owners'):
        for owner_type in childs:
            record = {}
            record['DATE'] = record_date
            record['KOD'] = 'Ф' if owner_type.tag == 'OwnerIndividual' else 'Ю'
            name = get_field_text(owner_type, 'Name')
            citizenship = get_field_text(owner_type, 'Citizenship', '-')
            record['NAME'] = "{0} ({1})".format(name, citizenship) 
            record['DEPO_ID'] = get_field_text(owner_type, 'Account')
            record['R2'] = get_address(owner_type.find('Address/Address'))
            owners.append(record)
        #print('\tOwner type:', owner[0].tag, '\tCountStock: ', child.find('CountStock').text, '\tAccount: ', owner[0].find('Account').text, \
        #    '\tName: ', Name)
    for o in owners:
        print(o)
def conv(txt):
    
    return txt.encode('utf-8').decode('utf-8')

def process_dbf(fname):

    global owners
    
    table = dbf.Table('dbase.dbf', 'DATE c(10); CUST_ID C(6); CUST_NAME c(70); DEPO_ID c(17);\
        KOD c(1); NAME c(254); RL c(254); R2 c(254); NALOG_CODE c(26); BORN_PLACE c(50);\
        BORN_DATE c(10); SUM_PAP n(19, 0); SUM_BLOCK n(19, 0); SUM_QUO n(19, 0); \
        OBT c(150); SUM_COST n(19, 2); PERCENT n(12, 6); BANK c(150); DIV_KIND n(1, 0);\
        SANKCII c(80)', codepage='cp1251')
       
    table.open(mode=dbf.READ_WRITE)

    for owner in owners:
        rec = {}
        rec["DATE"] = owner['DATE']
        rec["CUST_ID"] = ''
        rec["CUST_NAME"] = ''
        rec["DEPO_ID"] = owner['DEPO_ID']
        rec["KOD"] = owner['KOD']
        rec["NAME"] = owner['NAME']
        rec["RL"] = ''
        rec["R2"] = owner['R2']
        rec["NALOG_CODE"] = ''
        rec["BORN_PLACE"] = ''
        rec["BORN_DATE"] = ''
        rec["SUM_PAP"] = 1
        rec["SUM_BLOCK"] = 0
        rec["SUM_QUO"]  = 0
        rec["OBT"] = ""
        rec["SUM_COST"] = 1
        rec["PERCENT"] = 0
        rec["BANK"] = ""
        rec["DIV_KIND"] = 0 
        rec["SANKCII"] = ""
        table.append(rec)
    print('Database complete!')
    table.close()

def main():
    parse_xml('reestr.xml')
    #process_dbf('dbase.dbf')

if __name__ == "__main__":
    main()