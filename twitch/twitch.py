#!/usr/bin/env python
# AvicBotIRC.py 
# Authors: Avicennasis
# License:  MIT license Copyright (c) 2015 Avicennasis
# Revision: see git

# Import libraries
import re, socket, os, time

#Definitions
zero      = 0                   # Zero
one       = 1                   # One
false     = 0                   # Boolean False
true      = 1                   # Boolean True

# Program parameters

# botnick  = nick of the bot
# bufsize  = Input buffer size
# channel  = IRC channel
# port     = port number
# server   = server hostname
# master   = Owner of the bot
# uname    = Bot username 
# realname = Bot's "real name"

botnick    = "AvicBot"
bufsize    = 10240
channel    = "#noobenheim"
port       = 6667
server     = "irc.twitch.tv"
master     = "Avicennasis"
uname      = "AvicBot"
realname   = "Avicennasis"

#Dictionary
Replies = dict()
Replies ['die'      ] = "No, you"
Replies ['goodbye'  ] = "I'll miss you"
Replies ['sayonara' ] = "I'll miss you"
Replies ['scram'    ] = "No, you"
Replies ['shout'    ] = "NO I WON'T"
Replies ['dance'    ] = "*" + botnick + " dances*"
Replies ['hello'    ] = "Hi"
Replies ['howdy'    ] = "Hi"
Replies ['time'     ] = "It is TIME for a RHYME"
Replies ['master'   ] = master + " is my master"

#ping
def ping():
    global ircsock
    ircsock.send ("PONG :pingis\n")

#sendmsg
def sendmsg (chan, msg):
    global ircsock
    ircsock.send ("PRIVMSG "+ chan +" :"+ msg + "\n")

#JoinChan
def JoinChan (chan):
    global ircsock
    ircsock.send ("JOIN "+ chan +"\n")

#ProcHello
def ProcHello():
    global ircsock
    ircsock.send ("PRIVMSG "+ channel +" :Hello!\n")

# Main routine
def Main():
    global ircsock, Replies
                                #reply regex
    pattern1 = '.*:(\w+)\W*%s\W*$' % (botnick)
    pattern2 = '.*:%s\W*(\w+)\W*$' % (botnick)

    ircsock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    ircsock.connect ((server, port))
    ircsock.send ("PASS oauth:TOKEN \n")
    ircsock.send ("USER " + uname + " 2 3 " + realname + "\n")
    ircsock.send ("NICK "+ botnick + "\n")
    JoinChan (channel)          # Join channel

    while true:                 # Main loop
                                # Receive server data
        ircmsg = ircsock.recv (bufsize)
                                # newlines go alway
        ircmsg = ircmsg.strip ('\n\r')

        print ircmsg            # Echo input
        time.sleep(0.5)

        m1 = re.match (pattern1, ircmsg, re.I)
        m2 = re.match (pattern2, ircmsg, re.I)
        if ((m1 == None) and (m2 != None)): m1 = m2

        if (m1 != None):        # Yes
            word = m1.group (1) # Word found
            word = word.lower() # Make word lower case
                                # Print a reply
            if (word in Replies):
                sendmsg (channel, Replies [word])

        if ircmsg.find ("PING :") != -1:
            ping()

#  !die command to part channel
        if ircmsg.find(":!die "+botnick) != -1: 
            sendmsg(channel, "Do you wanna build a snowman? \n")
            time.sleep(2)
            sendmsg(channel, "It doesn't have to be a snowman. \n")
            time.sleep(2)
            sendmsg(channel, "Ok, Bye :( \n")
            sendmsg(master, "I have to leave now :( \n")
            break

# Say command
        if ircmsg.find (":!say ") != -1:
            say_split = ircmsg.split ("!say ")
            sendmsg (channel, say_split [1])
            sendmsg (master, "Message sent: " + say_split [1])

# !sing parameter
# Note that twitch seems to ignore multiple lines - need to add a delay here
        if ircmsg.find ("!sing") != -1:
            sendmsg (channel, "Daisy, Daisy, Give me your answer, do.\n")
            time.sleep(2)
            sendmsg (channel, "I'm half crazy all for the love of you.\n")

# !random parameter
# This was chosen by a fair roll of a d20.
        if ircmsg.find ("!random") != -1:
            sendmsg (channel, "7.\n")

# !commands parameter
# Note that twitch seems to ignore multiple lines - need to add a delay here
        if ircmsg.find ("!commands") != -1:
            sendmsg (channel, "Commands:\n")
            time.sleep(2)
            sendmsg (channel, "!say: I echo back whatever you say\n")
            time.sleep(2)
            sendmsg (channel, "!sing: I sing, duh\n")
            time.sleep(2)
            sendmsg (channel, "!die: Makes me leave :(\n")


# Main routine

Main()
exit (zero)
