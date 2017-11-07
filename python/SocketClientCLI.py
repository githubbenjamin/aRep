#!/usr/bin/python

"""
    2015-7-3
    
    virtual client

this is python script for testing Station overlay.

usage:
cd the script path first to avoid not found configure error. configure file should be defualtly named contentToSend.conf
just pull this script to the terminal and click the Enter button.


notes:
1. NO UI. this is a pity. maybe next version will have one.
2. exe permission. make sure that this script has a executable permission before running it.
3. configure. if you are trying the automatically testing, make sure the configure file edited appropriately already.

"""

import datetime

def curDateAndTime():
    now = datetime.datetime.now()
    return now.strftime('%Y/%m/%d %H:%M:%S.%f')


def sendMsgBySocketManually():
    print 'send message manually.'
    global sock
    sock.connect((ip_connect, port_connect))
    while 1:
        
        stringToSend = raw_input("please input to send: ")
        
        if cmp(stringToSend, 'Close_client,@') == 0:
            exit()
        
        print curDateAndTime()+' send    --> ' + stringToSend
        sock.send(stringToSend);
        
        receiveStr = sock.recv(bytes_n)
        if cmp(receiveStr, '')==0:
            sock.close()
            sock = sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.connect((ip_connect, port_connect))
            continue
        print curDateAndTime()+' receive <-- ' + receiveStr


def sendMsgBySocketAutomatically():
    cycleCounter = 0
    global sock
    global configFile,bytes_n,timeToCycle,ip_connect,port_connect,sleepSeconds
    print 'send message automatically.'
    
#    timeToCycle = int(input('please input a number to specify cycle time(0 for infinity): '))
    file_object = open(configFile)
    allLines = file_object.readlines()
    if len(allLines) <=0:
        print('read automatically running configure file failure. please check it.')
        print('exit system.')
        sock.close()
        exit;
    if timeToCycle == 0:
        while 1:
            print curDateAndTime()+' connect to ' + ip_connect + ' count: ' + str(cycleCounter)
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.connect((ip_connect, port_connect))
            for lineNumber in range(0, len(allLines)):
                print curDateAndTime()+' send    --> ' + allLines[lineNumber].strip('\n')
                if sock == None:
                    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    sock.connect((ip_connect, port_connect))
                sock.send(allLines[lineNumber].strip('\n'))
                
                if lineNumber == (len(allLines)-1):
                    print curDateAndTime()+' one cycle finish.'
                    print ''
                    sock.recv(bytes_n)
                    sock.close()
                    cycleCounter += 1
                    #                    time.sleep(0.2)
                    break
                receiveStr = sock.recv(bytes_n)
                if receiveStr == None or cmp(receiveStr, '')==0:
                    print curDateAndTime()+' receive none'
                    sock.close()
                    break
                if cmp(receiveStr, 'NACK,@')==0:
                    print curDateAndTime()+' receive NACK,@'
                    sock.close()
                    break
                if cmp(receiveStr, 'SYNC_ERROR,@') == 0:
                    print('synchrosize error occur, exit system.')
                    sock.close()
                    exit()
                if cmp(receiveStr, 'exceed Max connection count 1')==0:
                    print curDateAndTime()+' receive <-- ' + receiveStr
                    sock.close()
                    break
                print curDateAndTime()+' receive <-- ' + receiveStr
            time.sleep(sleepSeconds)
    
    
    for i in range(0,timeToCycle):
        print curDateAndTime()+' connect to ' + ip_connect + ' count: ' + str(cycleCounter)
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((ip_connect, port_connect))
        for lineNumber in range(0, len(allLines)):
            print curDateAndTime()+' send    --> ' + allLines[lineNumber].strip('\n')
            sock.send(allLines[lineNumber].strip('\n'))
            
            if lineNumber == (len(allLines)-1):
                print curDateAndTime()+' one cycle finish.'
                print ''
                sock.recv(bytes_n)
                sock.close()
                cycleCounter += 1
                #                time.sleep(0.2)
                continue
            
            receiveStr = sock.recv(bytes_n)
            
            if receiveStr == None or cmp(receiveStr, '')==0:
                print curDateAndTime()+' receive none'
                lineNumber = 0
                sock.close()
                continue
            
            print curDateAndTime()+' receive <-- ' + receiveStr
            if cmp(receiveStr, 'SYNC_ERROR,@') == 0:
                print('synchrosize error occur, exit system.')
                sock.close()
            exit
        time.sleep(sleepSeconds)

import sys, getopt
def usage():
    print """
        Usage: 
        client2.py (-c ip -p prot (-a 0)|-m ) | -d  [-s 0] [-f file] [-h]
        -d                  default, ip = 127.0.0.1, port = 2941, infinitily automatical.
        -c ip               ip to connect
        -p port             port to connect
        -a number           automatical, number is cycle time, 0 means infinity.
        -s number           seconds to sleep between cycle during automatical connection. 0 as default.
        -m                  manually.
        -f file_name        configure file name.
        -h                  help.
        """
import time
import socket
def main():
    global configFile,bytes_n,timeToCycle,ip_connect,port_connect,sleepSeconds

    
    configFile = 'contentToSend.conf'
    bytes_n = 1024
    sleepSeconds = 0
    
    print 'Welcome to virtual client'
    
    opts, args = getopt.getopt(sys.argv[1:], "hdc:p:a:s:mf:")
    
    what_connect = 2
    how_connect = 1
    
    for op, value in opts:
        if op == "-d":
            ip_connect = value
            port_connect = 2941
            timeToCycle = 0
            manualOperation = 0
            what_connect = 0
            how_connect = 0
#            print 'connect defaultly.'
        elif op == "-c":
            ip_connect = value
            what_connect -= what_connect
            print "connect ip: " + ip_connect
        elif op == "-p":
            port_connect = int(value)
            what_connect -= what_connect
            print "connect port: " + str(port_connect)
        elif op == "-a":
            timeToCycle = int(value)
            manualOperation = 0
            how_connect -= 1
        elif op == "-s":
            sleepSeconds = float(value)
        elif op == "-m":
            manualOperation = 1
            how_connect -= 1
        elif op == "-f":
            configFile = value
        elif op == "-h":
            usage()
            sys.exit()

    if not what_connect == 0:
        print 'pleas use -c and -p to set connection ip and port. -h for help.'
        exit()
    if not how_connect == 0:
        print 'pleas use -a or -m to set conncetion autmatically or not. -h for help.'
        exit()

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    if manualOperation == 1:
#        print 'Manually connect.'
        sendMsgBySocketManually()
    elif manualOperation == 0:
#        print 'Automatically connect.'
        sendMsgBySocketAutomatically()

    sock.close
    print 'client close'
    
    
if __name__ == "__main__":
    main()
