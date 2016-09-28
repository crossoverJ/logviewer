from PyQt4 import QtGui, QtCore
import json
import sys

class toolBar(QtGui.QToolBox):
    dict = {"FV_curve":{'list':[{'name':'H1','list':[],'keyword':'Extracted_H1','leftword':'Extracted_H1 FV:','rightword':'Normalized','line_width':1,'color':(0,0,255),'convert':"float",'div':1000000,'pass2next':False,'checked':1},
                        {'name':'H2','list':[],'keyword':'Extracted_H2','leftword':'Extracted_H2 FV:','rightword':'Normalized','line_width':1,'color':(0,255,127),'convert':"float",'div':1000000,'pass2next':False,'checked':1},
                        {'name':'V','list':[],'keyword':'Extracted_V','leftword':'Extracted_V FV:','rightword':'Normalized','line_width':1,'color':(255,105,180),'convert':"float",'div':1000000,'pass2next':False,'checked':1},
                        {'name':'HV','list':[],'keyword':'Extracted_HV','leftword':'Extracted_HV FV:','rightword':'Normalized','line_width':1,'color':(255,0,0),'convert':"float",'div':1000000,'pass2next':False,'checked':1},
                        {'name':'Lens Pos','list':[],'keyword':'af_actuator_move_focus','leftword':'curr_step_pos:','rightword':', curr_len_pos:','line_width':2,'color':(128,0,128),'convert':"int",'div':1,'pass2next':False,'checked':1}],
                        'checked':1},
            "Defocus_curve":{'list':[{'name':'Win1','list':[],'keyword':'af_pdaf_proc_pd: grid(0)','leftword':'defocus(dac)=','rightword':', conf','line_width':1,'color':(0,0,255),'convert':"int",'div':1,'pass2next':False,'checked':1},
                            {'name':'Win2','list':[],'keyword':'af_pdaf_proc_pd: grid(1)','leftword':'defocus(dac)=','rightword':', conf','line_width':1,'color':(0,255,127),'convert':"int",'div':1,'pass2next':False,'checked':1},
                            {'name':'Win3','list':[],'keyword':'af_pdaf_proc_pd: grid(2)','leftword':'defocus(dac)=','rightword':', conf','line_width':1,'color':(255,105,180),'convert':"int",'div':1,'pass2next':False,'checked':1},
                            {'name':'Win4','list':[],'keyword':'af_pdaf_proc_pd: grid(3)','leftword':'defocus(dac)=','rightword':', conf','line_width':1,'color':(255,0,0),'convert':"int",'div':1,'pass2next':False,'checked':1},
                            {'name':'Win5','list':[],'keyword':'af_pdaf_proc_pd: grid(4)','leftword':'defocus(dac)=','rightword':', conf','line_width':2,'color':(128,0,128),'convert':"int",'div':1,'pass2next':False,'checked':1},
                            {'name':'Win6','list':[],'keyword':'af_pdaf_proc_pd: grid(5)','leftword':'defocus(dac)=','rightword':', conf','line_width':2,'color':(128,0,128),'convert':"int",'div':1,'pass2next':False,'checked':1}],
                            'checked':0}
            }
    def __init__(self,parent):
        super(toolBar, self).__init__(parent)
        #self.writeJson(self.dict)
        self.filterList = self.readJson()
        #print self.filterList
        for name in self.filterList:
            print name
            filterGroup = self.filterList[name]
            groupbox = QtGui.QGroupBox()
            vlayout = QtGui.QVBoxLayout(groupbox)
            vlayout.setMargin(10)
            vlayout.setAlignment(QtCore.Qt.AlignLeft)
            cnt = 0
            for filterSingle in filterGroup['list']:
                button = QtGui.QCheckBox(filterSingle['name'])
                #button = myCheckBox(filterSingle['name'],filterSingle['name'])
                button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                if filterSingle.has_key('checked'):
                    button.setChecked((filterSingle['checked']))
                else:
                    filterSingle['checked'] = 0
                vlayout.addWidget(button)
                filterSingle['button'] = button
                button.clicked.connect(self.OnClicked)
                button.customContextMenuRequested.connect(self.rightClicked)
                #self.connect(button,QtCore.SIGNAL('sgnl(str)'),self.rightClicked)
                cnt+=1
            vlayout.addStretch(1)
            self.addItem(groupbox,name)
            #groupbox.setCheckable(True)
            #groupbox.setStyleSheet("QGroupBox{border: 1px groove blue; border-radius:5px;border-style: outset;}")
            filterGroup['box'] = groupbox
        for name in self.filterList:
            print name,self.filterList[name]['checked']
            if self.filterList[name]['checked']:
                print self.indexOf(self.filterList[name]['box'])
                self.setCurrentIndex(self.indexOf(self.filterList[name]['box']))
        self.connect(self,QtCore.SIGNAL("currentChanged(int)"),self.OnChanged)
        self.cb = self.dummyCallback

    def OnClicked(self):
        print "onclicked"
        for name in self.filterList:
            filterGroup = self.filterList[name]
            for idx,filterSingle in enumerate(filterGroup['list']):
                if filterSingle.has_key('button'):
                    if filterSingle['button'].isChecked():
                        self.filterList[name]['list'][idx]['checked'] = 1
                    else:
                        self.filterList[name]['list'][idx]['checked'] = 0
        '''
        for name in self.filterList:
            filterGroup = self.filterList[name]
            for filterSingle in filterGroup['list']:
                print filterSingle['checked']
        '''
        name = str(self.itemText(self.currentIndex()))
        self.cb(self.filterList[name]['list'])

    def rightClicked(self):
        name = str(self.itemText(self.currentIndex()))
        print name,self.sender().text(),'right clicked'
        l = self.getlistByName(name,self.sender().text())
        if l == '':
            return
        isSaved = [0]
        dlg = lineConfig(l,isSaved)
        dlg.exec_()
        print 'issaved',isSaved
        if isSaved[0]:
            print l
            self.updateList()

    def OnChanged(self):
        name = str(self.itemText(self.currentIndex()))
        #print name
        for n in self.filterList:
            self.filterList[n]['checked'] = 0     
        self.filterList[name]['checked'] = 1
        for n in self.filterList:
            print n,self.filterList[n]['checked']
        self.cb(self.filterList[name]['list'])

    def quit(self):
        for name in self.filterList:
            filterGroup = self.filterList[name]
            for filterSingle in filterGroup['list']:
                if filterSingle.has_key('button'):
                    filterSingle.pop('button')
                else:
                    print "no button"
            if filterGroup.has_key('box'):
                filterGroup.pop('box')
        self.writeJson(self.filterList)

    def readJson(self):
        jsonfile =  open("config.json","r")
        jsonobj = json.load(jsonfile)
        jsonfile.close()
        return jsonobj

    def writeJson(self,dic):
        jsonfile = open("config.json","w")
        string = json.dumps(dic,indent=4)
        jsonfile.write(string)
        jsonfile.close()

    def setCallback(self,cb):
        self.cb = cb

    def dummyCallback(self,flt):
        print 'cb'
    def getlistByName(self,groupName,listName):
        listSingle = self.filterList[groupName]['list']
        for l in listSingle:
            if l['name'] == listName:
                return l
        return ''
    def updateList(self):
        print 'updatelist'
        for name in self.filterList:
            filterGroup = self.filterList[name]
            for filterSingle in filterGroup['list']:
                if filterSingle.has_key('button'):
                    filterSingle['button'].setText(filterSingle['name'])


class lineConfig(QtGui.QDialog):
    listCopy = {}
    def __init__(self,listSingle,issaved,parent=None):
        super(lineConfig, self).__init__(parent)
        self.setWindowTitle('config')
        self.listSingle = listSingle
        self.issaved = issaved
        self.nameLabel = QtGui.QLabel(self.tr('name'))
        self.keyWordLabel = QtGui.QLabel(self.tr('keyword'))
        self.leftWordLabel = QtGui.QLabel(self.tr('left words'))
        self.rightWordLabel = QtGui.QLabel(self.tr('right words'))
        self.lineWidthLabel = QtGui.QLabel(self.tr('line width'))
        self.colorLabel = QtGui.QLabel(self.tr('color'))
        self.cancelButton = QtGui.QPushButton('cancel')

        self.nameInput = QtGui.QLineEdit(listSingle['name'])
        self.keyWordInput = QtGui.QLineEdit(listSingle['keyword'])
        self.leftWordInput = QtGui.QLineEdit(listSingle['leftword'])
        self.rightWordInput = QtGui.QLineEdit(listSingle['rightword'])
        self.lineWidthInput = QtGui.QSpinBox()
        self.lineWidthInput.setRange(1,10)
        self.lineWidthInput.setValue(listSingle['line_width'])
        self.colorInput = QtGui.QPushButton()
        preColor = QtGui.QColor(listSingle['color'][0],listSingle['color'][1],listSingle['color'][2]).name()
        self.colorInput.setStyleSheet('background-color:'+str(preColor))
        self.saveButton = QtGui.QPushButton('save')

        self.colorInput.clicked.connect(self.chooseColor)
        self.saveButton.clicked.connect(self.OnSave)
        self.cancelButton.clicked.connect(self.OnCancel)
        layout = QtGui.QGridLayout()
        layout.addWidget(self.nameLabel,0,0)
        layout.addWidget(self.keyWordLabel,1,0)
        layout.addWidget(self.leftWordLabel,2,0)
        layout.addWidget(self.rightWordLabel,3,0)
        layout.addWidget(self.lineWidthLabel,4,0)
        layout.addWidget(self.colorLabel,5,0)
        layout.addWidget(self.cancelButton,6,0)

        layout.addWidget(self.nameInput,0,1)
        layout.addWidget(self.keyWordInput,1,1)
        layout.addWidget(self.leftWordInput,2,1)
        layout.addWidget(self.rightWordInput,3,1)
        layout.addWidget(self.lineWidthInput,4,1)
        layout.addWidget(self.colorInput,5,1)
        layout.addWidget(self.saveButton,6,1)

        self.setLayout(layout)
        for name in self.listSingle:
            self.listCopy[name] = self.listSingle[name]

    def chooseColor(self):
        c = QtGui.QColorDialog.getColor(QtCore.Qt.blue)
        cname = str(c.name())
        if c.isValid():
            p = self.colorInput.palette()
            p.setColor(QtGui.QPalette.Button,c)
            self.colorInput.setStyleSheet('background-color:'+cname)
        cname = cname.replace('#','')
        rgbColor = [int(cname[0:2],16),int(cname[2:4],16),int(cname[4:6],16)]
        print rgbColor
        self.listCopy['color'] = tuple(rgbColor)

    def OnSave(self):
        print 'save'
        rc = self.checkValid()
        if not rc=='':
            QtGui.QMessageBox.information(self,"Information",self.tr(rc+' is empty!'))  
            print rc
            print 'invalid'
            return
        for name in self.listCopy:
            self.listSingle[name] = self.listCopy[name]
        self.issaved[0] = 1
        #print type(self.issaved)
        self.close()

    def OnCancel(self):
        print 'cancel'
        self.issaved[0] = 0
        self.close()

    def translateName(self,name):
        name = str(name)
        dic =  {'name':'name',
                'keyword':'keyword',
                'left words':'leftword',
                'right words':'rightword',
                'line width':'line_width',
                'color':'color'}
        if dic.has_key(name):
            return dic[name]
        else:
            return name

    def checkValid(self):
        if self.nameInput.text().isEmpty():
            print 'name is empty !'
            return self.nameLabel.text()
        self.listCopy[self.translateName(self.nameLabel.text())] = str(self.nameInput.text())

        if self.keyWordInput.text().isEmpty():
            print 'name is empty !'
            return self.keyWordLabel.text()
        self.listCopy[self.translateName(self.keyWordLabel.text())] = str(self.keyWordInput.text())

        if self.leftWordInput.text().isEmpty():
            print 'name is empty !'
            return self.leftWordLabel.text()
        self.listCopy[self.translateName(self.leftWordLabel.text())] = str(self.leftWordInput.text())

        if self.rightWordInput.text().isEmpty():
            print 'name is empty !'
            return self.rightWordLabel.text()
        self.listCopy[self.translateName(self.rightWordLabel.text())] = str(self.rightWordInput.text())

        self.listCopy[self.translateName(self.lineWidthLabel.text())] = int(self.lineWidthInput.value())
        return ''