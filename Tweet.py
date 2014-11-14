#!/usr/bin/env python2

from twitter import *
import socket, re, string, time

SAFE_USER = 'Bursihido' #only safe user can command the bot
BUFSIZ = 4096
NUM_TWEETS = 10

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

def remove_non_ascii(s):
  return ''.join(i for i in s if ord(i)<128)

def campareLines():
    fold = open('old.txt', 'ra+')
    fnew = open('new.txt', 'r')
    for line1 in fnew:
       for line2 in fold:
          if line1==line2:
            return True
          else:
            return False

def campareTweets(t): 
  fold = open('old.txt', 'ra+')
  fnew, arry = open('new.txt', 'w+'), []
  acnt, ftch = 0, t.statuses.home_timeline(count = NUM_TWEETS)
  
  while True: # try-except block is to detect pop() errors on last element 
    try:
      aobj = ftch.pop()
    except:
      print '',

    arry.append(remove_non_ascii(aobj['text']))
    acnt += 1
    if acnt == NUM_TWEETS:
      break

  for atwt in arry:
    fnew.write(atwt)
    fnew.write("\n")
  fnew.close()

  Flag = campareLines()
  
  if Flag == False:
    for fnew in arry:
      fold.write(fnew)
      fold.write("\n")
    fold.close
    for atwt in arry:
      s.send("PRIVMSG %s :%s \r\n" % (channel, atwt.encode('utf-8')))

  return arry

host='' # irc host addr
port=6667  # Port
nick='Tweetn' #Nick
ident='twitter' #ident
realname='tweeter' #realname
channel='' #channel
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) 
s.connect((host,port)) ## connecting server
s.sendall("NICK %s\r\n" % nick) #sending nick
s.sendall("USER %s %s bla :%s\r\n" % (ident, host, realname)) # sending ident host realname

data = s.recv(BUFSIZ) # BUFSIZ = 4096 

for line in data.split("\r\n"):
  if line.find('PING') != -1:
    s.send("PONG %s\r\n" % line.split()[1])
    s.send("JOIN :%s\r\n" % channel)

t = Twitter(auth=OAuth(ACCESS_KEY,ACCESS_SECRET,CONSUMER_KEY,CONSUMER_SECRET))
f = s.makefile()

while True:
  line = f.readline().rstrip()
  print line

  if re.search(".*\001.*\001.*", line):
    user = line.split('!~')[0][1:]
  else:
    if 'PING' in line: #if the server pings , ping back (keep connection)
      msg = line.split(':')[1].lstrip().rstrip()
      s.sendall("PONG {0}\r\n".format(msg))
      campareTweets(t)
    elif 'PRIVMSG' in line: # PRIVMSG lines only below
       next
