from PyQt4 import QtCore, QtGui
import paho.mqtt.client as mqtt
import sys
import numpy

host='52.90.36.67' 

mqttc=mqtt.Client()
mqttc.connect(host,1883,60)
mqttc.loop_start()
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

     
        
class Ui_Form(object):
    
    def __init__(self):
        self.items=''
    
    def setupUi(self, Form):
        
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(600, 600)
        self.toolButton_2 = QtGui.QToolButton(Form)
        self.toolButton_2.setGeometry(QtCore.QRect(240, 150, 261, 61))
        self.toolButton_2.setObjectName(_fromUtf8("toolButton_2"))
        self.toolButton_3 = QtGui.QToolButton(Form)
        self.toolButton_3.setGeometry(QtCore.QRect(240, 210, 261, 61))
        self.toolButton_3.setObjectName(_fromUtf8("toolButton_3"))
        self.toolButton_4 = QtGui.QToolButton(Form)
        self.toolButton_4.setGeometry(QtCore.QRect(240, 270, 261, 61))
        self.toolButton_4.setObjectName(_fromUtf8("toolButton_4"))
        self.toolButton_5 = QtGui.QToolButton(Form)
        self.toolButton_5.setGeometry(QtCore.QRect(240, 320, 261, 61))
        self.toolButton_5.setObjectName(_fromUtf8("toolButton_2"))
        '''self.toolButton_6 = QtGui.QToolButton(Form)
        self.toolButton_6.setGeometry(QtCore.QRect(550, 210, 261, 61))
        self.toolButton_6.setObjectName(_fromUtf8("toolButton_2"))'''
        self.textEdit = QtGui.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(80, 40, 371, 61))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        
        
        self.retranslateUi(Form)
        QtCore.QObject.connect(self.toolButton_5, QtCore.SIGNAL(_fromUtf8("clicked()")), self.submit)
        #QtCore.QObject.connect(self.toolButton_5, QtCore.SIGNAL(_fromUtf8("clicked()")), self.bot2)
        QtCore.QObject.connect(self.toolButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.message1)
        QtCore.QObject.connect(self.toolButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), self.message2)
        QtCore.QObject.connect(self.toolButton_4, QtCore.SIGNAL(_fromUtf8("clicked()")), self.message3)
        QtCore.QMetaObject.connectSlotsByName(Form)

    #bot_name = ' '
        
    #def bot1(self):
        #bot_name = 'bot1'
        #print bot_name
        
    #def bot2(self):
        #bot_name = 'bot2'
        #print bot_name
        
    
    def message1(self):
        self.items += 'coffee|'
        print "Coffee"
        #mqttc.publish("gui","coffee",2)
    def message2(self):
        self.items += 'tea|'
        print "Tea"
        #mqttc.publish("gui","tea",2)
    def message3(self):
        self.items += 'snacks|'
        print "Snacks"
        #mqttc.publish("gui","snacks",2)
        
    def submit(self):
        print self.items
        #self.items = '|'.join(items)
        print "Items: ", self.items
        mqttc.publish("gui",self.items,2)
        self.items=''

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.toolButton_2.setText(_translate("Form", "Coffee", None))
        self.toolButton_3.setText(_translate("Form", "Tea", None))
        self.toolButton_4.setText(_translate("Form", "Snacks", None))
        self.toolButton_5.setText(_translate("Form", "Submit", None))
        #self.toolButton_6.setText(_translate("Form", "Robot 2", None))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:26pt; font-weight:600;\">WARE HOUSE ROBOT</span></p></body></html>", None))


if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
    mqttc.loop_stop()
    mqttc.disconnect()
