#!/usr/bin/ruby

require 'tk'
require 'logger'
require 'socket'
require 'date'

#root = TkRoot.new { title "Hello, World!"}
#
#TkLabel.new(root) do
#    text "Hello, World!"
#    pack { padx 15; pady 15; side 'left'}
#end

#log = Logger.new("soapserver.log", 5, 10*1024)
#log.info("this is log.")

#Tk.mainloop

class TClient
    def ipportOK?(ip, port)
        if (ip =~ /^\d{1,3}(\.\d{1,3}){3}$/ && port =~ /^\d+$/)
            true
        else
            false
        end
#        if (port =~ /^\d+$/)
#            puts 'port ok'
#        end

    end
    
    def connect
#        @log.info("connect")
        hostname = @ipEntry.get()
        port = @portEntry.get()
#        puts hostname, port

        begin
        if (ipportOK?(hostname, port))
#            puts 'ip port ok'
            @log.info("ip port ok, initial socket.")
            @s = TCPSocket.new hostname, port.to_i
        end
        
        rescue
            setIPRed
            return
        end
        
        @log.info("connect #{hostname} success.")
        @ipEntry.configure('background'=>"green")
        
#        puts @s.methods
        td = Thread.new{receiveMsg(@s)}
        
        td.abort_on_exception = true
#        td.join

    end #connect
    
    def initialize
        @log = Logger.new("tclient.log", 5, 10*1024)
        
        root = TkRoot.new do
            title 'T Client'
            minsize(600, 400)
        end
        @label = TkLabel.new(root) do
            text 'host ip '
            grid('row'=>0, 'column'=>0)
        end
        
        @ipEntry = TkEntry.new(root){
            
            grid('row'=>0, 'column'=>1, 'columnspan' =>2)
        }
#        puts @ipEntry.methods
        @portEntry = TkEntry.new(root){
            
            grid('row'=>0, 'column'=>3, 'columnspan' =>1)
        }
        
        @buttonConnect = TkButton.new(root)
        @buttonConnect.configure('text' => 'Connect')
        @buttonConnect.command {connect}
#        @buttonConnect.pack('side'=>'left', 'padx'=>0, 'pady'=>100)
        @buttonConnect.grid('row'=>0, 'column'=>4)
#        puts @buttonConnect.methods

#        @buttonQuit = TkButton.new(root) do
#            text 'quit'
#            command 'exit'
#            grid('column'=>4, 'row'=>0)
##            pack('side'=>'left')
#        end

        @entry1 = TkEntry.new(root){
            grid('row'=>1, 'column'=>0, 'columnspan' =>2)
        }
        @sendb1 = TkButton.new(root){
            text 'send'
            grid('row'=>1, 'column'=>2, 'columnspan' =>1)
        }
        @entry2 = TkEntry.new(root){
            grid('row'=>1, 'column'=>3, 'columnspan' =>2)
        }
        
        @sendb2 = TkButton.new(root){
            text 'send'
            
            grid('row'=>1, 'column'=>5, 'columnspan' =>1)
        }
        
        @entry3 = TkEntry.new(root){
            grid('row'=>2, 'column'=>0, 'columnspan' =>2)
        }
        @sendb3 = TkButton.new(root){
            text 'send'
            grid('row'=>2, 'column'=>2, 'columnspan' =>1)
        }
        @entry4 = TkEntry.new(root){
            grid('row'=>2, 'column'=>3, 'columnspan' =>2)
        }
        
        @sendb4 = TkButton.new(root){
            text 'send'
            
            grid('row'=>2, 'column'=>5, 'columnspan' =>1)
        }
        
        @sendb1.command {sendMsg(@entry1.get)}
        @sendb2.command {sendMsg(@entry2.get)}
        @sendb3.command {sendMsg(@entry3.get)}
        @sendb4.command {sendMsg(@entry4.get)}

        @ipEntry.set('127.0.0.1')
        @portEntry.set('2941')
        @entry1.set('Send_msg,@')
        @entry2.set('F39123456:0:1,@')
        @entry3.set('Check_status,@')
        @entry4.set('Ack,@')
        
        @txt = TkText.new(root) do
            width 50
            height 15
            borderwidth 1
            font TkFont.new('')
#            readonly true
            grid('row'=>3, 'column'=>1, 'columnspan' =>4, 'rowspan'=>4)
#            pack('side' => 'left', 'padx'=>'5', 'pady'=>'20')
        end
#        @txt.insert('end', "HHKK\nUUUUIII")
#        @txt.insert('end', 'Another string. OHww')
#        puts @txt.methods
        Tk.mainloop
        
    end #initialize
    
    def sendMsg(msg)
        @log.info("send: #{msg}")
        @txt.insert('end', "#{curDT} >> #{msg}\n")
#        puts 'send: '+msg
        if msg == ''
            return
        end
        begin
            @s.write(msg)
        rescue
            setIPRed
            if !@s.nil? && !@s.closed?
                @s.close
            end
        end
    end
    
    def receiveMsg(s)
#        puts 's is closed: '+s.closed?.to_s

        while !@s.closed?
            begin
            rcv = @s.recv(1024*4)
            rescue Errno::ECONNRESET
                puts 'erro'
                setIPRed
                @s.close
                next
                
            end
            if rcv == ''
#                puts 'receive blank'
                next
            end
#            puts 's is closed: '+@s.closed?.to_s
#            puts 'eof? '+s.eof?.to_s
#            puts 'peer name'+ s.getpeername
#            puts 'receive: '+rcv

            @log.info("receive: #{rcv}")
            @txt.insert('end', "#{curDT} << #{rcv}\n")
            sleep(0.5)
        end
    end
    
    def setIPRed
#        puts 'set ip red.'
        @ipEntry.configure('background'=>"red")
    end
    
    def curDT
        
        Time.now.strftime("%Y-%m-%d %H:%M:%S")
    end


end #class

c = TClient.new
