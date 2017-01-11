#!/usr/bin/python

"""
    OpenTF Client
    
    update
    v0.1.1
    1. record, always log and show on UI during testing process.
    2. configer, auto save current data to system configure file. the number of send-button is configurable.
    3. auto testing, 
    4. get testing data, connect to the server to get special station upper&lower limits data. 
        usage:
            a. choose limits file
            b. fill the station name then
            c. click <Enter> in the station name Entry.
    5. catch the <KeyboardInterrupt> void exception message.
    
    todo:
        1. add <Command-X> to triger sendX click.
        2.
    """

from Tkinter import *
from ScrolledText import ScrolledText
from SimpleDialog import *
import logging
#import subprocess
from datetime import datetime
import threading
import time
import socket
import os

#from sc import *

import urllib
import httplib

#from Tkinter import Text
from idlelib.WidgetRedirector import WidgetRedirector

class ReadOnlyScrolledText(ScrolledText):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self.redirector = WidgetRedirector(self)
        self.insert = \
            self.redirector.register("insert", lambda *args, **kw: "break")
        self.delete = \
            self.redirector.register("delete", lambda *args, **kw: "break")
class OTF_TR(object):
    def __init__(self, initdir=None):
#        self.finishInit = False
        self.top = Tk()
        self.top.wm_title('OpenTF Client v0.1.1')
#        self.top.wm_minsize(width=600, height=400)
        self.top.resizable(width=False, height=False)

        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure (0, weight=1)
        
        self.top.protocol('WM_DELETE_WINDOW', self.on_closing)
        
        self.top.bind_class("Entry","<Command-a>", self.ctext_selectall)
#        self.top.bind("<Command-1>", self.Send_msg)

        self.configure = SystemConfigure('SystemConfigure.xml')
#
#        if self.configure.getValue()
        self.logger = self.getLogger()
        self.msg2send = []
        msgC = self.configure.getValueByKey('msg_count')
        if msgC==None or msgC=='' or not msgC.isdigit():
            # default value
            self.msg2send = ["Send_msg,@", "C39123456:0,@", "C39123456:2:1,@", "Check_status,@", "Ack,@",  ""]
        else:
            for i in range(0, int(msgC)):
                msg = self.configure.getValueByKey('msg%s'%i)
                if msg==None:
                    continue
                self.msg2send.append(msg)
            
#        self.sendButtons = []
        self.msgVars = []
        self.btns = []
        self.entrys = []
        self.receiveThreads = []
#        self.ereply = []

        hostLabel = Label(self.top, text='host')
        hostLabel.grid(row=0, column=0)
        
        self.ipVar = StringVar()
        self.ipEntry = Entry(self.top, textvariable=self.ipVar)
        self.ipEntry.grid(row=0, column=1, columnspan=2)
        
        self.portVar = StringVar()
        self.portEntry = Entry(self.top, textvariable=self.portVar)
        self.portEntry.grid(row=0, column=3)
        
        self.conctBt = Button(self.top, text='connect', command=self.connect, activeforeground='white', activebackground='blue')
        self.conctBt.grid(row=0, column=4, sticky='e')
        
        self.autoFlag = 0
        self.autoBt = Button(self.top, text='auto', command=self.autoTest)
        self.autoBt.grid(row=1, column=0, sticky='e')
        
        self.clearBt = Button(self.top, text='clear', command=self.clearText)
        self.clearBt.grid(row=1, column=1, sticky='e')
        
        
        aeflist = self.http_util('aefl').split('::')
#        print 'ae file list: %s'%aeflist
        for i in aeflist:
            if not i.endswith('.xlsx'):
                aeflist.remove(i)
        self.optionVar = StringVar()
        if aeflist!=None and len(aeflist)!=0 and not aeflist[0]=='':
            
            self.xBt = Button(self.top, text='.X.', command=self.xa)
            self.xBt.grid(row=1, column=2, sticky='e')
            
            self.optionVar.set(aeflist[0])
            
            self.optionMn = OptionMenu(self.top, self.optionVar, *aeflist )
    #        print self.optionMn.keys()
    #        print self.optionMn.menu()
            self.optionMn.grid(row=1, column=3)
            
            self.sn = StringVar() # station name
            self.snEntry = Entry(self.top, textvariable=self.sn)
            self.snEntry.bind("<Return>", self.getullimits)
            self.snEntry.grid(row=1, column=4, columnspan=1)
        
        self.freshSendFB(2)
        
        self.text = ReadOnlyScrolledText(self.top)
        self.text.grid(row=2+len(self.msg2send)/2, column=1, rowspan=1, columnspan=3)
        self.text.config(font=("consolas", 12), undo=False, wrap='word', state='normal')
#        print self.text.keys()

        ip_t = self.configure.getValueByKey('ip')
        if ip_t!=None and ip_t!='':
            self.ipVar.set(ip_t)
        else:
            self.ipVar.set('127.0.0.1')
        port_t = self.configure.getValueByKey('port')
        if port_t!=None and port_t!='':
            self.portVar.set(port_t)
        else:
            self.portVar.set('2941')
        
#        self.text.insert(float(1), "a text.\n")
#        print '%s'%self.text.get(1.0, END).split('\n')
#        self.text.insert(END, "b text.\n")
#        self.text.insert(END, "c text.\n")
#        at = self.text.get(0.0, END).split('\n')
#        print "%s, %d"%(at, len(at) )
#        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket = None
        self.cc = 0

#        self.finishInit = True
#        self.terminal = False
        self.logger.info("system initial finished.")
        self.top.mainloop()
        
    
    def on_closing(self):
        # save current msg
        msg_count = len(self.msgVars)
        self.configure.setValueByKey('%s'%msg_count,'msg_count')
        for i in range(0, msg_count):
            self.configure.setValueByKey(self.msgVars[i].get(), 'msg%s'%i)
        self.configure.save()
        
        ##
        ip = self.ipVar.get()
        if self.isIPOK(ip):
            self.configure.setValueByKey(ip, 'ip')
        port = self.portVar.get()
        if port.isdigit():
            self.configure.setValueByKey(port, 'port')
        
        ##
        self.logger.info("system quit.\n")
#        print 'on closing'
#        if self.socket != None:
#            self.socket.close()
#            self.socket.shutdown(socket.SHUT_RDWR)
#            self.socket = None
#        print 'finish socket close'

#        self.terminal = True
        self.top.quit()
        self.top.destroy()
        
#        os.exist()

    def isIPOK(self, ip):
        rst = re.match(r'^\d{1,3}(\.\d{1,3}){3}$', ip)
        if rst==None:
            return False
        return True
    
    def xa(self):
#        print dir(self.optionMn['menu'])
        pass
#        print 'xa'

#        self.top.quit()
    def getullimits(self, z):
#        print '%s, %s'%(type(z), z.keycode)
#        print 'get upper low limits'
        ul = self.http_util('ullimits')
        tt = 'upper&lower limits'
        sdl_text = 'Success to get upper&lower, which one you want to copy to clipboard?'
        sdl_bn = ['upper', 'lower', 'cancel']
        if ul=='' or len(ul.split('\n'))!=2:
            tt = 'upper&lower limits::Fail to get'
            sdl_text= 'Maybe server is NOT online.\nMaybe parse fail.'
        
        dlg_ac = SimpleDialog(self.top,
                              title = tt,
                              text = sdl_text,
                              buttons = sdl_bn,
                              default = 0,
                              )
        choose_index = dlg_ac.go()
#        print ul
#        print choose_index
        if sdl_bn[choose_index] in ['upper', 'lower']:
#            self.top.withdraw()
            self.top.clipboard_clear()
#            temp_str = ul.split('\n')[choose_index]
#            print 'choose text, %s'%temp_str
            self.top.clipboard_append(ul.split('\n')[choose_index])

#        print choose_index

    def connect(self):
#        ip = "127.0.0.1"
#        port = 2941

#        if self.socket == None:
#            print 'debug, socket none'
#            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        print 'socket:',self.socket, self.socket.getpeername()

#        if not self.finishInit:
#            return
        if self.cc%20==0:
            self.clearBt.invoke()
        
        ip = self.ipVar.get()
        port = self.portVar.get()
        if self.socket == None:
            self.logger.info('socket is None')
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        

        try:
            if self.isIPOK(ip) and port.isdigit():
                self.logger.info("connect (%s, %s), count:%s"%(ip, port, self.cc))
                self.append2text("connected %s\n"%self.cc)
                error_code = self.socket.connect_ex( (ip, int(port)) )
                if error_code != 0:
#                    print ''
#                    print 'error code: ',error_code
                    if error_code == 56:
                        # connect second, last not close.
                        return
#                    if error_code == 61:
                        # server not start.
#                        self.setIPRed()
#                        return
                    self.setIPRed()
                    self.socket.close()
#                    self.socket = None ## definately not set the self.socket None here.
                    return
        
            else:
                self.logger.info('ip or port not ok')
                self.setIPRed()
                return
        except:
#            print 'connect exception.'
            self.logger.info("connect exception.")
#            print 'error code: ',errorlist[-1]
            self.socket.close()
            self.socket = None
            self.setIPRed()
            return

        try:
            thread_rcv = threading.Thread(target = self.receiveMsg, args = (), name = 'otfc_receving')
            thread_rcv.setDaemon(True) # this very importent.
            thread_rcv.start()
            self.receiveThreads.append(thread_rcv)
        except:
#            print "Error: unable to start receving message thread"
            self.logger.info("Error: unable to start receving message thread")
#        "Error: unable to start receving message thread"
        self.cc+=1

        self.ipEntry.configure(background="green")



    def sendMSG(self, btnID):
#        print 'buttons',
#        for j in self.btns:
#            
#            print '%s'%j.config('text')[-1],
#        print ''

        msg = self.msgVars[int(btnID[-1])].get()
#        print 'index:%s msg:%s'%(btnID, msg)
#        if not self.finishInit:
#            print 'not finished'
#            return
        if msg=='':
            return
        try:
            self.logger.info("send >>%s"%msg)
#            print "send >>%s"%msg
            self.append2text(">>%s\n"%msg)
            self.socket.send(msg)
            
        except:
            self.setIPRed()
            if self.socket != None:
                self.socket.close()
                self.logger.info('socket already closed while sending msg')
                return
        

    def receiveMsg(self):
        # getpeername
        isConnected = True
        while isConnected:
#            print '1'
            try:
                rcv = self.socket.recv(1024*4)
            except:
                isConnected = False
                self.setIPRed()
#                print 'closed already.'

            if rcv == '':
                isConnected = False
#                print 'rcv blank'
                self.append2text("\n")
                self.socket.close()
                self.socket = None
#                self.socket.connect(('127.0.0.1', 2941))
#                print 'socket:',self.socket
#                print ' ----:',self.socket.getpeername()
                return
            print 'recevie << %s'%rcv
            self.append2text("<<%s\n"%rcv)
            self.logger.info('recevie << %s'%rcv)
            time.sleep(0.2)
#        print 222222
    #break
    def append2text(self, msg):
#        self.text.config(state='normal')
        self.text.insert(END, msg)
        self.text.see(END)
#        self.text.config(state='disabled')
#        pt = self.text.get(0.0, END)
#        if len(pt)>=1 and pt[-1].isspace():
#            pt = pt[:-1]


    def setIPRed(self):
        self.ipEntry.configure(background="red")

    def freshSendFB(self, baseRow):
        # check
        if self.msg2send==None or len(self.msg2send)==0:
            return
        columnNumber = 2
        self.msgVars = []
#        print 'start echo line'
        for i in range(0, len(self.msg2send)):
            self.msgVars.append(StringVar())
            self.msgVars[-1].set(self.msg2send[i])
            self.entrys.append(Entry(self.top, textvariable=self.msgVars[-1], width=20))
            self.entrys[-1].grid(row=baseRow+i/columnNumber, column=(i%columnNumber)*3, columnspan=2)
#sendButton = Button(self.top, text='send%s'%i, command=lambda: self.sendMSG('send%s'%i))
            self.btns.append(Button(self.top, text='send%s'%i, command=lambda: self.sendMSG('send%s'%i)) )
            #sendButton.grid(row=baseRow+i/columnNumber, column=(i%columnNumber)*2+2)
            self.btns[-1].grid(row=baseRow+i/columnNumber, column=(i%columnNumber)*2+2)
#            self.btns.append(sendButton)
#            print '----2'
        for b in self.btns:
            b.configure(command=lambda m=b.config('text')[-1] :self.sendMSG(m))
    def autoTest(self):
        self.autoFlag += 1
        self.autoFlag %= 1000
        if self.autoFlag%2 == 1:
            thread_autot = threading.Thread(target = self.testThread, args = (), name = 'otfc_autot')
            thread_autot.setDaemon(True)
            thread_autot.start()
        

    def testThread(self):
        while self.autoFlag%2 == 1:
            self.conctBt.invoke()
            time.sleep(0.3)
            for b in self.btns:
                b.invoke()
                time.sleep(0.3)
            time.sleep(0.2)

    def clearText(self):
#        self.text.config(state='normal')
        self.text.delete(0.0, END)
#        self.text.config(state='disabled')

    def http_util(self, cmd_key):
        if cmd_key not in ['aefl', 'ullimits']:
            return ''
        sn = ''
        sl = ''
        if cmd_key=='ullimits':
            sn = self.sn.get()
            sl = self.optionVar.get()
#        print '--%s--%s--'%(sn, sl)
        params = urllib.urlencode({'Submit': cmd_key,\
                              'Stationname': sn,\
                              'Select': sl})
        headers = {"Content-type":"application/x-www-form-urlencoded","Accept":"text/plain"}
        conn = httplib.HTTPConnection("seagull.local:80")
        try:
            conn.request("POST","/tdata", params, headers)
        except:
            return ''
        res = conn.getresponse()
        rlt = res.read()
#        print 'http get:\n%s'%rlt
        return rlt
    def ctext_selectall(self, event):
        event.widget.selection_range(0, END)
    def getLogger(self):
        # get current date for log file name
        now = datetime.now()
        dateStr = str(datetime.date(now))
        # create logger
        logger = logging.getLogger("./otfClient_log-%s"%dateStr)
        logger.setLevel(logging.INFO)
        # create console handler and set level to debug
        ch = logging.FileHandler("./otfClient_log-%s.txt"%dateStr, "a")
        ch.setLevel(logging.DEBUG)
        # create formatter
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        logger.addHandler(ch)
        
        return logger


"""
    SystemConfigure
    author: Benjamin
    version: 0.1.7
    date: 2016-05-06
    
    v0.1.7 2016-05-06
    1. create new file when the configure file not exist for Class SystemConfigure.
    2. save xml file with pretty format for Class SystemConfigure.
    3. change the judge condition when adding 'w' mode to configure file.
    
    2015-10-29
    system configure
    2015-11-04 debug
    """
import xml.dom.minidom
import os

def printGreen(msg):
    print '\33[0m\33[32m'+msg+'\33[0m'

def printRed(msg):
    print '\33[0m\33[31m'+msg+'\33[0m'


class SystemConfigure:
    '''System Configure
        impliment system configure function by key&value structure.
        note,
        usually you need invoke the save() method to write data to local file after setting and removing action.
        '''
    def __init__(self,xmlFilePath="systemconfig.xml"):
        self.filePath = xmlFilePath
        try:
            self.xmlDoc = xml.dom.minidom.parse(self.filePath)
        except xml.parsers.expat.ExpatError:
            print "read xml file fail"
            self.newNoneKeyFile()
            self.xmlDoc = xml.dom.minidom.parse(self.filePath)
        #            return
        except IOError:
            print "IO error,"
            self.newNoneKeyFile()
            self.xmlDoc = xml.dom.minidom.parse(self.filePath)
    
        #check file writable mode
        file_state = os.stat(xmlFilePath)
        #        print '---%o'%file_state.st_mode
        is_writable = file_state.st_mode&0100200
        #        print '---%o'%is_writable
        if is_writable not in [0100200]:
            os.chmod(xmlFilePath,file_state.st_mode+0000200)
        #        print '---%o'%os.stat(xmlFilePath).st_mode
        
        self.topElement = self.xmlDoc.documentElement
    def newNoneKeyFile(self):
        'new a none key file. automatical invoke while configure file not exists.'
        tmpfile = open(self.filePath, "w")
        tmpfile.writelines(['''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<root>\n</root>'''])
        tmpfile.close()
    
    def getValueByKey(self, key):
        'get value by the key.'
        try:
            aChild = self.topElement.getElementsByTagName(key)[0]
        except IndexError:
            return None
        #        print str(aChild.firstChild)
        if aChild.firstChild==None:
            return ''
        else:
            return aChild.firstChild.data
    def setValueByKey(self,value, key):
        'set value by key.'
        theChilds = self.topElement.getElementsByTagName(key)
        if not theChilds.length ==0:
            if theChilds[0].firstChild==None:
                text = self.xmlDoc.createTextNode(value)
                theChilds[0].appendChild(text)
            else:
                theChilds[0].firstChild.data = value
        else:
            aElement = self.xmlDoc.createElement(key)
            text = self.xmlDoc.createTextNode(value)
            aElement.appendChild(text)
            self.topElement.appendChild(aElement)
    def removeByKey(self,key):
        'remove the node by the key.'
        theChilds = self.topElement.getElementsByTagName(key)
        for aChild in theChilds:
            self.topElement.removeChild(aChild)
    def save(self):
        'manually invake if needing to update local configure file.'
        f = open(self.filePath, "w")
        allXmlLines = self.xmlDoc.toprettyxml(indent = "\t", newl = "\n", encoding = "utf-8").split("\n")
        allLines2write = []
        for aline in allXmlLines:
            if cmp(aline.strip(),"")==0:
                continue
            allLines2write.append(aline+'\n')
        f.writelines(allLines2write)
        f.close()

def main():
    try:
        t = OTF_TR()
    except KeyboardInterrupt:
        print 'KeyboardInterrupt'
#	mainloop()

if __name__ == '__main__':
    #    sys.argv
    main()
