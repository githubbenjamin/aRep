netstat
arp
nslookup
nbtscan
gethostbyname
[admin@v015213 ~/lpmall]$ nmblookup -A 10.19.30.17
C:\Users\xxxx>netstat -a 10.16.214.60
route
rlogin\nssh
vnc://10.175.70.173
vnc://10.175.71.113
nc -w 10 -n -z 127.0.0.1 1990-1999
lsof -n -P -i TCP -s TCP:LISTEN
tcpdump -i 2941 -w capture.cap host bleacher.local

mac下一般用smb服务来进行远程文件访问，但要用FTP的话，高版本的mac os默认关掉了，可以用如下命令打开:
sudo -s launchctl load -w /System/Library/LaunchDaemons/ftp.plist
相应的，要关闭则：
sudo -s launchctl unload -w /System/Library/LaunchDaemons/ftp.plist

/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user

ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
ruby -e "$(curl -fsSL http://localhost:8080/tools/tclient)"

defaults write com.apple.NetworkBrowser BrowseAllInterfaces 1

openssl base64 -in jo.sh -out based_jo.sh

openssl enc -des3 -salt -in jo.sh -out jo.sh_des3.bin
openssl enc -des3 -salt -d -out jo2.sh -in jo.sh_des3.bin

system_profiler SPUSBDataType -xml >system_usb_info.xml

Linux

setsebool ftpd_disable_trans 1

# 
sudo sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db 'select * from access'

sudo sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db “REPLACE INTO access VALUES(‘kTCCServiceAccessibility’,’com.getdropbox.dropbox’,0,1,1,NULL, NULL);”
