# -*- coding: utf-8 -*-


try:
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtWidgets import QFileDialog, QAction
except:
    print()
    print("PyQt5 module Not Found")
    print("Install: pip3 install PyQt5")
    sys.exit(1)

try:
    import dbf
except:
    print()
    print("dbf module Not Found")
    print("Install: pip3 install dbf")
    sys.exit(1)


import configparser
import os
from datetime import datetime
import xml.etree.ElementTree as et
from xml.etree.ElementTree import ParseError as er

from typing import List

class Ui_MainWindow(QtWidgets.QMainWindow):

    config_path: str = 'settings.ini'
    dbf_path: str = ""
    xml_fname: str = ""
    DEBUG: int = 0
    owners: List = []
    infos: List = []

    def check_conditions(self):
        if not os.path.isdir(self.dbf_path):
            self.log("Некорректный путь для сохранения DBF файлов")
            return False
        if not os.path.exists(self.XMLNameLabel.text()):
            self.log("Укажите XML файл с реестром ")
            return False
        return True

    def closeEvent(self, event):
        self.save_config(self.config_path)
        #print('event!')
        event.accept()

    def get_config(self, path):
        if not os.path.exists(path):
            with open(path, 'w') as f:
                pass
            
        
        config = configparser.ConfigParser()
        config.read(path)
        self.dbf_path = config.get('Settings', 'dbf_path', fallback="")
        self.DEBUG = config.get('Settings', 'debug', fallback=0)
    
    def save_config(self, path):

        config = configparser.ConfigParser()
        config.add_section("Settings")
        config.set("Settings", "dbf_path", self.dbf_path)
        config.set("Settings", "debug", str(self.DEBUG))
                
        with open(path, "w") as config_file:
            config.write(config_file)
        
        
    def __init__(self):
        super().__init__()
        
        self.get_config(self.config_path)
    
    
        self.setObjectName("MainWindow")
        self.resize(400, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(400, 500))
        self.setMaximumSize(QtCore.QSize(400, 500))

        self.setWindowIcon(QtGui.QIcon('./img/3d.png'))

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        debugAct = QAction('Debug', self, checkable=True)
        debugAct.setStatusTip('Debug')
        
        debugAct.setChecked(bool(int(self.DEBUG)))
        debugAct.triggered.connect(self.check_debug)
        fileMenu.addAction(debugAct)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.XMLgroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.XMLgroupBox.setGeometry(QtCore.QRect(10, 10, 381, 61))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.XMLgroupBox.setFont(font)
        self.XMLgroupBox.setObjectName("XMLgroupBox")
        self.XMLButton = QtWidgets.QPushButton(self.XMLgroupBox)
        self.XMLButton.setGeometry(QtCore.QRect(10, 22, 31, 31))
        self.XMLButton.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.XMLButton.setText("")
        #icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap(":/Open/img/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.XMLButton.setIcon(QtGui.QIcon("./img/folder.png"))
        self.XMLButton.setObjectName("XMLButton")
        self.XMLNameLabel = QtWidgets.QLabel(self.XMLgroupBox)
        self.XMLNameLabel.setGeometry(QtCore.QRect(50, 25, 321, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.XMLNameLabel.setFont(font)
        self.XMLNameLabel.setText("")
        self.XMLNameLabel.setWordWrap(True)
        self.XMLNameLabel.setObjectName("XMLNameLabel")
        self.DBFgroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.DBFgroupBox.setGeometry(QtCore.QRect(10, 80, 381, 61))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.DBFgroupBox.setFont(font)
        self.DBFgroupBox.setObjectName("DBFgroupBox")
        self.DBFButton = QtWidgets.QPushButton(self.DBFgroupBox)
        self.DBFButton.setGeometry(QtCore.QRect(10, 22, 31, 31))
        self.DBFButton.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.DBFButton.setText("")
        self.DBFButton.setIcon(QtGui.QIcon("./img/folder.png"))
        self.DBFButton.setObjectName("DBFButton")
        self.DBFNameLabel = QtWidgets.QLabel(self.DBFgroupBox)
        self.DBFNameLabel.setGeometry(QtCore.QRect(50, 25, 321, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.DBFNameLabel.setFont(font)
        self.DBFNameLabel.setText("")
        self.DBFNameLabel.setWordWrap(True)
        self.DBFNameLabel.setObjectName("DBFNameLabel")
        self.processButton = QtWidgets.QPushButton(self.centralwidget)
        self.processButton.setGeometry(QtCore.QRect(130, 150, 121, 31))
        self.processButton.setObjectName("processButton")
        self.LogEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.LogEdit.setGeometry(QtCore.QRect(0, 190, 401, 290))
        self.LogEdit.setReadOnly(True)
        self.LogEdit.setObjectName("LogEdit")
        self.setCentralWidget(self.centralwidget)

        self.XMLButton.clicked.connect(self.load_xml_file)
        self.DBFButton.clicked.connect(self.load_save_dir)
        self.processButton.clicked.connect(self.process_parsing)


        self.retranslateUi(self) #
        QtCore.QMetaObject.connectSlotsByName(self)#
    
    def check_debug(self, state):
        self.DEBUG = int(state)
        

    def load_xml_file(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ =  QFileDialog.getOpenFileName(caption="Open File", filter="XML files (*.xml);;Any files (*.*)", options=options)
        if fileName:
            self.XMLNameLabel.setText(fileName)
            self.xml_fname = fileName

    def load_save_dir(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        dirName =  QFileDialog.getExistingDirectory(caption="Choose directory to save", directory=self.dbf_path)     #getOpenFileName(caption="Choose directory to save", options=options)
        if dirName:
            self.DBFNameLabel.setText(dirName)
            self.dbf_path = dirName
    
    def process_parsing(self):
        #print(len(self.LogEdit.toPlainText().split("\n")))
        if not self.check_conditions():
            self.log("Заполните начальные данные")
        else:
            self.log("Данные корректны")
        #self.LogEdit.append("Clicked!")
        if self.parse_xml(self.xml_fname):
            self.process_owner(self.dbf_path+'/owners.dbf')
            self.process_info(self.dbf_path+'/info.dbf')
        #self.log('')
        self.infos = []
        self.owners = []

        

    def log(self, text):
        self.LogEdit.append(text)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.XMLgroupBox.setTitle(_translate("MainWindow", "XML файл рестра"))
        self.DBFgroupBox.setTitle(_translate("MainWindow", "Директория для сохранения файлов *.dbf"))
        self.processButton.setText(_translate("MainWindow", "Преобразовать"))
        self.DBFNameLabel.setText(_translate("MainWindow", self.dbf_path))

    def parse_xml(self, fname):
    
        try:
            tree = et.ElementTree(file=fname)
        except er:
            self.log('Ошибка парсинга XML')
            return False
        root = tree.getroot()
        
        if root.find('RecordDate') is None:
            self.log('Ошибка парсинга: не найдена секция <RecordDate>')
            return False
        else:
            dt = datetime.strptime(root.find('RecordDate').text[:10], "%Y-%m-%d")
            record_date = dt.strftime("%d.%m.%Y")

        issue = root.find('Issue')
        paper = {}

        if not (issue is None):

            for fnm in {'ISIN', 'Kind', 'Class', 'RegNum', 'NominalValue'}:
                paper[fnm] = issue.findtext(fnm)

            depo = root.find('Depository')
            self.add_info(depo, paper)

            issuer = root.find('Issuer')
            self.add_info(issuer, paper)

            for child in root.findall('./Custodians//CustodianElement'):
                self.add_info(child, paper)

        
        for childs in root.findall('./Custodians//CustodianElement//OwnerElements//OwnerElement//Owners'):
            for owner_type in childs:
                record = {}
                record['DATE'] = record_date
                record['KOD'] = 'Ф' if owner_type.tag == 'OwnerIndividual' else 'Ю'
                name = owner_type.findtext('Name', "")

                ctzn = owner_type.findtext('Citizenship', '-') 
                citizenship = "Україна" if ctzn == 'UA' else ctzn
                
                record['NAME'] = "{0} ({1})".format(name, citizenship) 
                record['DEPO_ID'] = owner_type.findtext('Account', "")
                record['R2'] = self.get_address(owner_type.find('Address/Address'))
                self.owners.append(record)
            #print('\tOwner type:', owner[0].tag, '\tCountStock: ', child.find('CountStock').text, '\tAccount: ', owner[0].find('Account').text, \
            #    '\tName: ', Name)
        if self.DEBUG:
            for o in self.owners:
                self.log(str(o))
            for o in self.infos:
                self.log(str(o))
        return True

    def add_info(self, node, paper):
        record = {}
        record['PAPER_ID'] = paper['ISIN']
        record['PAPER_KIND'] = paper['Class'][:19]
        record['REG_NUM'] = paper['RegNum']
        record['NOMINAL'] = paper['NominalValue']
        record['CUST_ID'] = node.findtext('MDOCode', "")
        record['EDRPOU'] = node.findtext('EDRPOU')
        record['NAME'] = node.findtext('Name')
        record['ADDRESS'] = self.get_address(node.find('Address'))
        self.infos.append(record)

    def get_address(self, node):

        fields = ['AddInfo', 'Street', 'House', 'Aprt', 'City', 'District', 'State', 'PostCode']
        adr = []
        if node.find('Address'):
            node = node.find('Address')

        for field in fields:
            if node.findtext(field):
                adr.append(node.findtext(field))

        return ", ".join(adr)

    def process_owner(self, fname):

        #self.log(fname)
        
        table = dbf.Table(fname, 'DATE c(10); CUST_ID C(6); CUST_NAME c(70); DEPO_ID c(17);\
            KOD c(1); NAME c(254); RL c(254); R2 c(254); NALOG_CODE c(26); BORN_PLACE c(50);\
            BORN_DATE c(10); SUM_PAP n(19, 0); SUM_BLOCK n(19, 0); SUM_QUO n(19, 0); \
            OBT c(150); SUM_COST n(19, 2); PERCENT n(12, 6); BANK c(150); DIV_KIND n(1, 0);\
            SANKCII c(80)', codepage='cp1251')
        
        table.open(mode=dbf.READ_WRITE)

        for owner in self.owners:
            rec = {}
            rec["DATE"] = owner['DATE']
            rec["CUST_ID"] = owner.get('CUST_ID', '')
            rec["CUST_NAME"] = owner.get('CUST_NAME', '')
            rec["DEPO_ID"] = owner['DEPO_ID']
            rec["KOD"] = owner.get('KOD', '')
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
        self.log('Таблица OWNERS создана. Добавлено {0} записей'.format(len(self.owners)))
        table.close()

    def process_info(self, fname):

        table = dbf.Table(fname, 'PAPER_ID c(12); PAPER_KIND c(20); REG_NUM c(20); NOMINAL n(15, 2); \
        CUST_ID c(6); EDRPOU c(26); NAME c(70); ADDRESS c(120); LICENSE c(46); PHONE c(40)', codepage='cp1251')
       
        table.open(mode=dbf.READ_WRITE)

        for info in self.infos:
            rec = {}
            for fld in info:
                rec[fld] = info[fld]
            rec['LICENSE'] = ''
            rec['PHONE'] = ''
            table.append(rec)

        self.log('Таблица INFO создана. Добавлено {0} записей'.format(len(self.infos)))
        table.close()
        
        
#import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    #ui.setupUi(MainWindow)
    #MainWindow.show()
    ui.show()
    sys.exit(app.exec_())
