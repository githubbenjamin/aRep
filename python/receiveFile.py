#!/usr/bin/env python
#coding=utf-8

from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import time
import os,shutil

class   PostHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        rst = self.save_uploaded_file('file01', os.path.abspath('./upload'))
        #if os.path.exists(os.path.abspath('./upload'))
        self.wfile.write("fail" if rst==None else rst)

    def do_GET(self):
#        for i in self.headers:
#            print '%s->%s'%(i, self.headers[i])
#        host = self.headers.get('WWW-Authenticate')
#        print('Authorization:', host)
        self.send_response(200)
        self.end_headers()
        uploadPage = """
            <html>
            <head>
            <title>upload file</title>
            </head>
            <body>
            
            <form action="/" method="post" enctype="multipart/form-data">
            <label for="file">Filename:</label>
            <input type="file" name="file01" id="file" />
            <br />
            <input type="submit" name="submit" value="Submit" />
            </form>
            
            </body>
            </html>
            """
        self.wfile.write(uploadPage)

    def save_uploaded_file(self, form_field, upload_dir):
        form = cgi.FieldStorage(
                                fp=self.rfile,
                                headers=self.headers,
                                environ={'REQUEST_METHOD':'POST',
                                'CONTENT_TYPE':self.headers['Content-Type'],
                                })
        print('form keys: %s'%form.keys())
        if not form.has_key(form_field):
            print('form has not key[%s]'%form_field)
            return
        fileitem = form[form_field]
        if not fileitem.file:
            print('form has not file')
            return
        
        outpath = os.path.join(upload_dir, fileitem.filename)
        print('save file to path: '+outpath)
        with open(outpath, 'wb') as fout:
            shutil.copyfileobj(fileitem.file, fout, 100000)
        return fileitem.filename

if __name__=='__main__':
    from BaseHTTPServer import HTTPServer
    try:
        import commands
        (status, output) = commands.getstatusoutput("ifconfig | grep 10.175 | awk '{print $2}'")
        print "local ip: %s"%output
        sever = HTTPServer((output, 80), PostHandler)
        print 'Starting server, use <Ctrl-C> to stop'
        sever.serve_forever()
    except KeyboardInterrupt, e:
        print e
