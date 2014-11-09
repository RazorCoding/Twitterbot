from twitter import *
import socket
import re
import string
import time

safe = "Bursihido" #only safe user can command the bot

CONSUMER_KEY=''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

host="" # irc host addr
port=6667  # Port
nick="Tweetn" #Nick
ident="twitter" #ident
realname="tweeter" #realname
channel="" #channel

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) 
s.connect((host,port)) ## connecting server
s.sendall("NICK %s\r\n" % nick) #sending nick
s.sendall("USER %s %s bla :%s\r\n" % (ident, host, realname)) # sending ident host realname
data = s.recv(4096)  
for line in data.split('\r\n'):
    if line.find('PING') != -1:
        s.send("PONG %s\r\n" % line.split()[1])
        s.send("JOIN :%s\r\n" % channel)

t = Twitter(auth=OAuth(ACCESS_KEY,ACCESS_SECRET,CONSUMER_KEY,CONSUMER_SECRET))

f=s.makefile()
while 1:
    line = f.readline().rstrip() 
    print line
    if re.search(".*\001.*\001.*", line):
        user = line.split('!~')[0][1:]
        s.sendall('PRIVMSG {0} :stop plox\r\n'.format(user))
    else:
        if '!quit' in line: #if a user PRIVMSG's '!quit' quit
            user = line[line.find('!quit'):].rstrip().lstrip()
            if user in safe:
              s.sendall("QUIT :Quit: Leaving...\r\n")
            break
        if 'PING' in line: #if the server pings , ping back (keep connection)
            msg = line.split(':')[1].lstrip().rstrip()
            s.sendall("PONG {0}\r\n".format(msg))
            
        if '!fetch' in line:
            fetch = reversed(t.statuses.home_timeline(count=5))
            for e in fetch:
              s.send("PRIVMSG %s :%s \r\n" % (channel, e['text'].encode('utf-8')))
