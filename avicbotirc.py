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
channel    = "##Avic,#cvn-sw"
port       = 6667
server     = "chat.freenode.net"
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
    ircsock.send ("USER " + uname + " 2 3 " + realname + "\n")
    ircsock.send ("NICK "+ botnick + "\n")
    ircsock.send ("PRIVMSG NickServ :identify PASSWORD \n")
    JoinChan (channel)          # Join channel

    while true:                 # Main loop
                                # Receive server data
        ircmsg = ircsock.recv (bufsize)
                                # newlines go alway
        ircmsg = ircmsg.strip ('\n\r')

        print ircmsg            # Echo input
        time.sleep(0.2)
        
        m1 = re.match (pattern1, ircmsg, re.I)
        m2 = re.match (pattern2, ircmsg, re.I)
        if ((m1 == None) and (m2 != None)): m1 = m2

        if (m1 != None):        # Yes
            word = m1.group (1) # Word found
            word = word.lower() # Make word lower case
                                # Print a reply
            if (word in Replies):
                sendmsg (channel, Replies [word])
                time.sleep(0.1)

        if ircmsg.find ("PING :") != -1:
            ping()

#  !die command to part channel
        if ircmsg.find(":!die "+botnick) != -1: 
            sendmsg(channel, "Do you wanna build a snowman? \n")
            time.sleep(0.1)
            sendmsg(channel, "It doesn't have to be a snowman. \n")
            time.sleep(0.1)
            sendmsg(channel, "Ok, Bye :( \n")
            sendmsg(master, "I have to leave now :( \n")
            break

# SULINFO rebulid
# https://tools.wmflabs.org/guc/?user=USERNAME&blocks=true
        if ircmsg.find (":!guc ") != -1:
            say_split = ircmsg.split ("!guc ")
            sendmsg (channel, "https://tools.wmflabs.org/guc/?user=" + say_split [1] + "&blocks=true")
            sendmsg (master, "https://tools.wmflabs.org/guc/?user=" + say_split [1] + "&blocks=true")

# CAUTH rebuild
# https://meta.wikimedia.org/wiki/Special:CentralAuth/USERNAME
        if ircmsg.find (":!cauth ") != -1:
            say_split = ircmsg.split ("!cauth ")
            sendmsg (channel, "https://meta.wikimedia.org/wiki/Special:CentralAuth/" + say_split [1])
            sendmsg (master, "https://meta.wikimedia.org/wiki/Special:CentralAuth/" + say_split [1])
 
# LINK rebulid - this needs a regex rebuild still
# http://avicbot.org/LINK
        if ircmsg.find (":!link ") != -1:
            say_split = ircmsg.split ("!link ")
            sendmsg (channel, "http://avicbot.org/" + say_split [1])
            sendmsg (master, "http://avicbot.org/" + say_split [1])

# Say command
        if ircmsg.find (":!say ") != -1:
            say_split = ircmsg.split ("!say ")
            sendmsg (channel, say_split [1])
            sendmsg (master, "Message sent: " + say_split [1])

# !sing parameter
        if ircmsg.find ("!sing") != -1:
            sendmsg (channel, "Daisy, Daisy, Give me your answer, do.\n")
            time.sleep(0.1)
            sendmsg (channel, "I'm half crazy all for the love of you.\n")

# !random parameter
# This was chosen by a fair roll of a d20.
        if ircmsg.find ("!random") != -1:
            sendmsg (channel, "7.\n")

# !commands parameter
        if ircmsg.find ("!commands") != -1:
            sendmsg (channel, "Commands:\n")
            time.sleep(0.1)
            sendmsg (channel, "!say: Say stuff, !lang ISO code does lookup\n")
            time.sleep(0.1)
            sendmsg (channel, "!cauth: give you centralauth page for a user\n")
            time.sleep(0.1)
            sendmsg (channel, "!guc: gives Global User Contribs page \n")
            time.sleep(0.1)
            sendmsg (channel, "!die: Makes me leave :(\n")

# Languages
        if ircmsg.find ("!lang en?") != -1:
            sendmsg(channel, "en is English! \n")
        if ircmsg.find ("!lang sv?") != -1:
            sendmsg(channel, "sv is Swedish! \n")
        if ircmsg.find ("!lang de?") != -1:
            sendmsg(channel, "de is German! \n")
        if ircmsg.find ("!lang nl?") != -1:
            sendmsg(channel, "nl is Dutch! \n")
        if ircmsg.find ("!lang fr?") != -1:
            sendmsg(channel, "fr is French! \n")
        if ircmsg.find ("!lang war?") != -1:
            sendmsg(channel, "war is Waray-Waray! \n")
        if ircmsg.find ("!lang ru?") != -1:
            sendmsg(channel, "ru is Russian! \n")
        if ircmsg.find ("!lang it?") != -1:
            sendmsg(channel, "it is Italian! \n")
        if ircmsg.find ("!lang ceb?") != -1:
            sendmsg(channel, "ceb is Cebuano! \n")
        if ircmsg.find ("!lang es?") != -1:
            sendmsg(channel, "es is Spanish! \n")
        if ircmsg.find ("!lang vi?") != -1:
            sendmsg(channel, "vi is Vietnamese! \n")
        if ircmsg.find ("!lang pl?") != -1:
            sendmsg(channel, "pl is Polish! \n")
        if ircmsg.find ("!lang ja?") != -1:
            sendmsg(channel, "ja is Japanese! \n")
        if ircmsg.find ("!lang pt?") != -1:
            sendmsg(channel, "pt is Portuguese! \n")
        if ircmsg.find ("!lang zh?") != -1:
            sendmsg(channel, "zh is Chinese! \n")
        if ircmsg.find ("!lang uk?") != -1:
            sendmsg(channel, "uk is Ukrainian! \n")
        if ircmsg.find ("!lang ca?") != -1:
            sendmsg(channel, "ca is Catalan! \n")
        if ircmsg.find ("!lang fa?") != -1:
            sendmsg(channel, "fa is Persian! \n")
        if ircmsg.find ("!lang sh?") != -1:
            sendmsg(channel, "sh is Serbo-Croatian! \n")
        if ircmsg.find ("!lang no?") != -1:
            sendmsg(channel, "no is Norwegian! \n")
        if ircmsg.find ("!lang ar?") != -1:
            sendmsg(channel, "ar is Arabic! \n")
        if ircmsg.find ("!lang fi?") != -1:
            sendmsg(channel, "fi is Finnish! \n")
        if ircmsg.find ("!lang id?") != -1:
            sendmsg(channel, "id is Indonesian! \n")
        if ircmsg.find ("!lang ro?") != -1:
            sendmsg(channel, "ro is Romanian! \n")
        if ircmsg.find ("!lang hu?") != -1:
            sendmsg(channel, "hu is Hungarian! \n")
        if ircmsg.find ("!lang cs?") != -1:
            sendmsg(channel, "cs is Czech! \n")
        if ircmsg.find ("!lang ko?") != -1:
            sendmsg(channel, "ko is Korean! \n")
        if ircmsg.find ("!lang sr?") != -1:
            sendmsg(channel, "sr is Serbian! \n")
        if ircmsg.find ("!lang ms?") != -1:
            sendmsg(channel, "ms is Malay! \n")
        if ircmsg.find ("!lang tr?") != -1:
            sendmsg(channel, "tr is Turkish! \n")
        if ircmsg.find ("!lang min?") != -1:
            sendmsg(channel, "min is Minangkabau! \n")
        if ircmsg.find ("!lang eo?") != -1:
            sendmsg(channel, "eo is Esperanto! \n")
        if ircmsg.find ("!lang kk?") != -1:
            sendmsg(channel, "kk is Kazakh! \n")
        if ircmsg.find ("!lang eu?") != -1:
            sendmsg(channel, "eu is Basque! \n")
        if ircmsg.find ("!lang da?") != -1:
            sendmsg(channel, "da is Danish! \n")
        if ircmsg.find ("!lang sk?") != -1:
            sendmsg(channel, "sk is Slovak! \n")
        if ircmsg.find ("!lang bg?") != -1:
            sendmsg(channel, "bg is Bulgarian! \n")
        if ircmsg.find ("!lang hy?") != -1:
            sendmsg(channel, "hy is Armenian! \n")
        if ircmsg.find ("!lang he?") != -1:
            sendmsg(channel, "he is Hebrew! \n")
        if ircmsg.find ("!lang lt?") != -1:
            sendmsg(channel, "lt is Lithuanian! \n")
        if ircmsg.find ("!lang hr?") != -1:
            sendmsg(channel, "hr is Croatian! \n")
        if ircmsg.find ("!lang sl?") != -1:
            sendmsg(channel, "sl is Slovenian! \n")
        if ircmsg.find ("!lang et?") != -1:
            sendmsg(channel, "et is Estonian! \n")
        if ircmsg.find ("!lang uz?") != -1:
            sendmsg(channel, "uz is Uzbek! \n")
        if ircmsg.find ("!lang gl?") != -1:
            sendmsg(channel, "gl is Galician! \n")
        if ircmsg.find ("!lang nn?") != -1:
            sendmsg(channel, "nn is Norwegian (Nynorsk)! \n")
        if ircmsg.find ("!lang vo?") != -1:
            sendmsg(channel, "vo is Volapuk! \n")
        if ircmsg.find ("!lang la?") != -1:
            sendmsg(channel, "la is Latin! \n")
        if ircmsg.find ("!lang simple?") != -1:
            sendmsg(channel, "simple is Simple English! \n")
        if ircmsg.find ("!lang el?") != -1:
            sendmsg(channel, "el is Greek! \n")
        if ircmsg.find ("!lang hi?") != -1:
            sendmsg(channel, "hi is Hindi! \n")
        if ircmsg.find ("!lang ce?") != -1:
            sendmsg(channel, "ce is Chechen! \n")
        if ircmsg.find ("!lang be?") != -1:
            sendmsg(channel, "be is Belarusian! \n")
        if ircmsg.find ("!lang az?") != -1:
            sendmsg(channel, "az is Azerbaijani! \n")
        if ircmsg.find ("!lang ka?") != -1:
            sendmsg(channel, "ka is Georgian! \n")
        if ircmsg.find ("!lang th?") != -1:
            sendmsg(channel, "th is Thai! \n")
        if ircmsg.find ("!lang oc?") != -1:
            sendmsg(channel, "oc is Occitan! \n")
        if ircmsg.find ("!lang mk?") != -1:
            sendmsg(channel, "mk is Macedonian! \n")
        if ircmsg.find ("!lang mg?") != -1:
            sendmsg(channel, "mg is Malagasy! \n")
        if ircmsg.find ("!lang ur?") != -1:
            sendmsg(channel, "ur is Urdu! \n")
        if ircmsg.find ("!lang new?") != -1:
            sendmsg(channel, "new is Newar! \n")
        if ircmsg.find ("!lang ta?") != -1:
            sendmsg(channel, "ta is Tamil! \n")
        if ircmsg.find ("!lang tt?") != -1:
            sendmsg(channel, "tt is Tatar! \n")
        if ircmsg.find ("!lang cy?") != -1:
            sendmsg(channel, "cy is Welsh! \n")
        if ircmsg.find ("!lang pms?") != -1:
            sendmsg(channel, "pms is Piedmontese! \n")
        if ircmsg.find ("!lang tl?") != -1:
            sendmsg(channel, "tl is Tagalog! \n")
        if ircmsg.find ("!lang bs?") != -1:
            sendmsg(channel, "bs is Bosnian! \n")
        if ircmsg.find ("!lang lv?") != -1:
            sendmsg(channel, "lv is Latvian! \n")
        if ircmsg.find ("!lang te?") != -1:
            sendmsg(channel, "te is Telugu! \n")
        if ircmsg.find ("!lang be-x-old?") != -1:
            sendmsg(channel, "be-x-old is Belarusian (Taraskievica)! \n")
        if ircmsg.find ("!lang br?") != -1:
            sendmsg(channel, "br is Breton! \n")
        if ircmsg.find ("!lang ht?") != -1:
            sendmsg(channel, "ht is Haitian! \n")
        if ircmsg.find ("!lang sq?") != -1:
            sendmsg(channel, "sq is Albanian! \n")
        if ircmsg.find ("!lang jv?") != -1:
            sendmsg(channel, "jv is Javanese! \n")
        if ircmsg.find ("!lang lb?") != -1:
            sendmsg(channel, "lb is Luxembourgish! \n")
        if ircmsg.find ("!lang mr?") != -1:
            sendmsg(channel, "mr is Marathi! \n")
        if ircmsg.find ("!lang ml?") != -1:
            sendmsg(channel, "ml is Malayalam! \n")
        if ircmsg.find ("!lang is?") != -1:
            sendmsg(channel, "is is Icelandic! \n")
        if ircmsg.find ("!lang zh-yue?") != -1:
            sendmsg(channel, "zh-yue is Cantonese! \n")
        if ircmsg.find ("!lang bn?") != -1:
            sendmsg(channel, "bn is Bengali! \n")
        if ircmsg.find ("!lang af?") != -1:
            sendmsg(channel, "af is Afrikaans! \n")
        if ircmsg.find ("!lang ga?") != -1:
            sendmsg(channel, "ga is Irish! \n")
        if ircmsg.find ("!lang ba?") != -1:
            sendmsg(channel, "ba is Bashkir! \n")
        if ircmsg.find ("!lang ky?") != -1:
            sendmsg(channel, "ky is Kirghiz! \n")
        if ircmsg.find ("!lang pnb?") != -1:
            sendmsg(channel, "pnb is Western Punjabi! \n")
        if ircmsg.find ("!lang cv?") != -1:
            sendmsg(channel, "cv is Chuvash! \n")
        if ircmsg.find ("!lang tg?") != -1:
            sendmsg(channel, "tg is Tajik! \n")
        if ircmsg.find ("!lang sco?") != -1:
            sendmsg(channel, "sco is Scots! \n")
        if ircmsg.find ("!lang fy?") != -1:
            sendmsg(channel, "fy is West Frisian! \n")
        if ircmsg.find ("!lang lmo?") != -1:
            sendmsg(channel, "lmo is Lombard! \n")
        if ircmsg.find ("!lang my?") != -1:
            sendmsg(channel, "my is Burmese! \n")
        if ircmsg.find ("!lang yo?") != -1:
            sendmsg(channel, "yo is Yoruba! \n")
        if ircmsg.find ("!lang an?") != -1:
            sendmsg(channel, "an is Aragonese! \n")
        if ircmsg.find ("!lang sw?") != -1:
            sendmsg(channel, "sw is Swahili! \n")
        if ircmsg.find ("!lang ne?") != -1:
            sendmsg(channel, "ne is Nepali! \n")
        if ircmsg.find ("!lang ast?") != -1:
            sendmsg(channel, "ast is Asturian! \n")
        if ircmsg.find ("!lang zh-min-nan?") != -1:
            sendmsg(channel, "zh-min-nan is Min Nan! \n")
        if ircmsg.find ("!lang io?") != -1:
            sendmsg(channel, "io is Ido! \n")
        if ircmsg.find ("!lang gu?") != -1:
            sendmsg(channel, "gu is Gujarati! \n")
        if ircmsg.find ("!lang scn?") != -1:
            sendmsg(channel, "scn is Sicilian! \n")
        if ircmsg.find ("!lang bpy?") != -1:
            sendmsg(channel, "bpy is Bishnupriya Manipuri! \n")
        if ircmsg.find ("!lang nds?") != -1:
            sendmsg(channel, "nds is Low Saxon! \n")
        if ircmsg.find ("!lang ku?") != -1:
            sendmsg(channel, "ku is Kurdish! \n")
        if ircmsg.find ("!lang als?") != -1:
            sendmsg(channel, "als is Alemannic! \n")
        if ircmsg.find ("!lang qu?") != -1:
            sendmsg(channel, "qu is Quechua! \n")
        if ircmsg.find ("!lang su?") != -1:
            sendmsg(channel, "su is Sundanese! \n")
        if ircmsg.find ("!lang pa?") != -1:
            sendmsg(channel, "pa is Punjabi! \n")
        if ircmsg.find ("!lang kn?") != -1:
            sendmsg(channel, "kn is Kannada! \n")
        if ircmsg.find ("!lang ckb?") != -1:
            sendmsg(channel, "ckb is Sorani! \n")
        if ircmsg.find ("!lang mn?") != -1:
            sendmsg(channel, "mn is Mongolian! \n")
        if ircmsg.find ("!lang bar?") != -1:
            sendmsg(channel, "bar is Bavarian! \n")
        if ircmsg.find ("!lang ia?") != -1:
            sendmsg(channel, "ia is Interlingua! \n")
        if ircmsg.find ("!lang nap?") != -1:
            sendmsg(channel, "nap is Neapolitan! \n")
        if ircmsg.find ("!lang arz?") != -1:
            sendmsg(channel, "arz is Egyptian Arabic! \n")
        if ircmsg.find ("!lang bug?") != -1:
            sendmsg(channel, "bug is Buginese! \n")
        if ircmsg.find ("!lang bat-smg?") != -1:
            sendmsg(channel, "bat-smg is Samogitian! \n")
        if ircmsg.find ("!lang wa?") != -1:
            sendmsg(channel, "wa is Walloon! \n")
        if ircmsg.find ("!lang gd?") != -1:
            sendmsg(channel, "gd is Scottish Gaelic! \n")
        if ircmsg.find ("!lang am?") != -1:
            sendmsg(channel, "am is Amharic! \n")
        if ircmsg.find ("!lang map-bms?") != -1:
            sendmsg(channel, "map-bms is Banyumasan! \n")
        if ircmsg.find ("!lang yi?") != -1:
            sendmsg(channel, "yi is Yiddish! \n")
        if ircmsg.find ("!lang mzn?") != -1:
            sendmsg(channel, "mzn is Mazandarani! \n")
        if ircmsg.find ("!lang si?") != -1:
            sendmsg(channel, "si is Sinhalese! \n")
        if ircmsg.find ("!lang fo?") != -1:
            sendmsg(channel, "fo is Faroese! \n")
        if ircmsg.find ("!lang nah?") != -1:
            sendmsg(channel, "nah is Nahuatl! \n")
        if ircmsg.find ("!lang vec?") != -1:
            sendmsg(channel, "vec is Venetian! \n")
        if ircmsg.find ("!lang sah?") != -1:
            sendmsg(channel, "sah is Sakha! \n")
        if ircmsg.find ("!lang os?") != -1:
            sendmsg(channel, "os is Ossetian! \n")
        if ircmsg.find ("!lang mrj?") != -1:
            sendmsg(channel, "mrj is Hill Mari! \n")
        if ircmsg.find ("!lang sa?") != -1:
            sendmsg(channel, "sa is Sanskrit! \n")
        if ircmsg.find ("!lang li?") != -1:
            sendmsg(channel, "li is Limburgish! \n")
        if ircmsg.find ("!lang hsb?") != -1:
            sendmsg(channel, "hsb is Upper Sorbian! \n")
        if ircmsg.find ("!lang roa-tara?") != -1:
            sendmsg(channel, "roa-tara is Tarantino! \n")
        if ircmsg.find ("!lang or?") != -1:
            sendmsg(channel, "or is Oriya! \n")
        if ircmsg.find ("!lang pam?") != -1:
            sendmsg(channel, "pam is Kapampangan! \n")
        if ircmsg.find ("!lang mhr?") != -1:
            sendmsg(channel, "mhr is Meadow Mari! \n")
        if ircmsg.find ("!lang se?") != -1:
            sendmsg(channel, "se is Northern Sami! \n")
        if ircmsg.find ("!lang mi?") != -1:
            sendmsg(channel, "mi is Maori! \n")
        if ircmsg.find ("!lang ilo?") != -1:
            sendmsg(channel, "ilo is Ilokano! \n")
        if ircmsg.find ("!lang bcl?") != -1:
            sendmsg(channel, "bcl is Central Bicolano! \n")
        if ircmsg.find ("!lang hif?") != -1:
            sendmsg(channel, "hif is Fiji Hindi! \n")
        if ircmsg.find ("!lang gan?") != -1:
            sendmsg(channel, "gan is Gan! \n")
        if ircmsg.find ("!lang ps?") != -1:
            sendmsg(channel, "ps is Pashto! \n")
        if ircmsg.find ("!lang rue?") != -1:
            sendmsg(channel, "rue is Rusyn! \n")
        if ircmsg.find ("!lang glk?") != -1:
            sendmsg(channel, "glk is Gilaki! \n")
        if ircmsg.find ("!lang nds-nl?") != -1:
            sendmsg(channel, "nds-nl is Dutch Low Saxon! \n")
        if ircmsg.find ("!lang diq?") != -1:
            sendmsg(channel, "diq is Zazaki! \n")
        if ircmsg.find ("!lang bo?") != -1:
            sendmsg(channel, "bo is Tibetan! \n")
        if ircmsg.find ("!lang azb?") != -1:
            sendmsg(channel, "azb is South Azerbaijani! \n")
        if ircmsg.find ("!lang vls?") != -1:
            sendmsg(channel, "vls is West Flemish! \n")
        if ircmsg.find ("!lang bh?") != -1:
            sendmsg(channel, "bh is Bihari! \n")
        if ircmsg.find ("!lang fiu-vro?") != -1:
            sendmsg(channel, "fiu-vro is Voro! \n")
        if ircmsg.find ("!lang xmf?") != -1:
            sendmsg(channel, "xmf is Mingrelian! \n")
        if ircmsg.find ("!lang co?") != -1:
            sendmsg(channel, "co is Corsican! \n")
        if ircmsg.find ("!lang tk?") != -1:
            sendmsg(channel, "tk is Turkmen! \n")
        if ircmsg.find ("!lang sc?") != -1:
            sendmsg(channel, "sc is Sardinian! \n")
        if ircmsg.find ("!lang gv?") != -1:
            sendmsg(channel, "gv is Manx! \n")
        if ircmsg.find ("!lang vep?") != -1:
            sendmsg(channel, "vep is Vepsian! \n")
        if ircmsg.find ("!lang km?") != -1:
            sendmsg(channel, "km is Khmer! \n")
        if ircmsg.find ("!lang hak?") != -1:
            sendmsg(channel, "hak is Hakka! \n")
        if ircmsg.find ("!lang csb?") != -1:
            sendmsg(channel, "csb is Kashubian! \n")
        if ircmsg.find ("!lang lrc?") != -1:
            sendmsg(channel, "lrc is Northern Luri! \n")
        if ircmsg.find ("!lang kv?") != -1:
            sendmsg(channel, "kv is Komi! \n")
        if ircmsg.find ("!lang zea?") != -1:
            sendmsg(channel, "zea is Zeelandic! \n")
        if ircmsg.find ("!lang crh?") != -1:
            sendmsg(channel, "crh is Crimean Tatar! \n")
        if ircmsg.find ("!lang frr?") != -1:
            sendmsg(channel, "frr is North Frisian! \n")
        if ircmsg.find ("!lang zh-classical?") != -1:
            sendmsg(channel, "zh-classical is Classical Chinese! \n")
        if ircmsg.find ("!lang eml?") != -1:
            sendmsg(channel, "eml is Emilian-Romagnol! \n")
        if ircmsg.find ("!lang wuu?") != -1:
            sendmsg(channel, "wuu is Wu! \n")
        if ircmsg.find ("!lang ay?") != -1:
            sendmsg(channel, "ay is Aymara! \n")
        if ircmsg.find ("!lang udm?") != -1:
            sendmsg(channel, "udm is Udmurt! \n")
        if ircmsg.find ("!lang stq?") != -1:
            sendmsg(channel, "stq is Saterland Frisian! \n")
        if ircmsg.find ("!lang kw?") != -1:
            sendmsg(channel, "kw is Cornish! \n")
        if ircmsg.find ("!lang nrm?") != -1:
            sendmsg(channel, "nrm is Norman! \n")
        if ircmsg.find ("!lang as?") != -1:
            sendmsg(channel, "as is Assamese! \n")
        if ircmsg.find ("!lang rm?") != -1:
            sendmsg(channel, "rm is Romansh! \n")
        if ircmsg.find ("!lang szl?") != -1:
            sendmsg(channel, "szl is Silesian! \n")
        if ircmsg.find ("!lang so?") != -1:
            sendmsg(channel, "so is Somali! \n")
        if ircmsg.find ("!lang koi?") != -1:
            sendmsg(channel, "koi is Komi-Permyak! \n")
        if ircmsg.find ("!lang lad?") != -1:
            sendmsg(channel, "lad is Ladino! \n")
        if ircmsg.find ("!lang sd?") != -1:
            sendmsg(channel, "sd is Sindhi! \n")
        if ircmsg.find ("!lang fur?") != -1:
            sendmsg(channel, "fur is Friulian! \n")
        if ircmsg.find ("!lang mt?") != -1:
            sendmsg(channel, "mt is Maltese! \n")
        if ircmsg.find ("!lang ie?") != -1:
            sendmsg(channel, "ie is Interlingue! \n")
        if ircmsg.find ("!lang gn?") != -1:
            sendmsg(channel, "gn is Guarani! \n")
        if ircmsg.find ("!lang pcd?") != -1:
            sendmsg(channel, "pcd is Picard! \n")
        if ircmsg.find ("!lang dv?") != -1:
            sendmsg(channel, "dv is Divehi! \n")
        if ircmsg.find ("!lang dsb?") != -1:
            sendmsg(channel, "dsb is Lower Sorbian! \n")
        if ircmsg.find ("!lang lij?") != -1:
            sendmsg(channel, "lij is Ligurian! \n")
        if ircmsg.find ("!lang cbk-zam?") != -1:
            sendmsg(channel, "cbk-zam is Zamboanga Chavacano! \n")
        if ircmsg.find ("!lang cdo?") != -1:
            sendmsg(channel, "cdo is Min Dong! \n")
        if ircmsg.find ("!lang ksh?") != -1:
            sendmsg(channel, "ksh is Ripuarian! \n")
        if ircmsg.find ("!lang ext?") != -1:
            sendmsg(channel, "ext is Extremaduran! \n")
        if ircmsg.find ("!lang gag?") != -1:
            sendmsg(channel, "gag is Gagauz! \n")
        if ircmsg.find ("!lang mwl?") != -1:
            sendmsg(channel, "mwl is Mirandese! \n")
        if ircmsg.find ("!lang ang?") != -1:
            sendmsg(channel, "ang is Anglo-Saxon! \n")
        if ircmsg.find ("!lang lez?") != -1:
            sendmsg(channel, "lez is Lezgian! \n")
        if ircmsg.find ("!lang ug?") != -1:
            sendmsg(channel, "ug is Uyghur! \n")
        if ircmsg.find ("!lang ace?") != -1:
            sendmsg(channel, "ace is Acehnese! \n")
        if ircmsg.find ("!lang pi?") != -1:
            sendmsg(channel, "pi is Pali! \n")
        if ircmsg.find ("!lang pag?") != -1:
            sendmsg(channel, "pag is Pangasinan! \n")
        if ircmsg.find ("!lang nv?") != -1:
            sendmsg(channel, "nv is Navajo! \n")
        if ircmsg.find ("!lang frp?") != -1:
            sendmsg(channel, "frp is Franco-Provencal! \n")
        if ircmsg.find ("!lang sn?") != -1:
            sendmsg(channel, "sn is Shona! \n")
        if ircmsg.find ("!lang kab?") != -1:
            sendmsg(channel, "kab is Kabyle! \n")
        if ircmsg.find ("!lang myv?") != -1:
            sendmsg(channel, "myv is Erzya! \n")
        if ircmsg.find ("!lang ln?") != -1:
            sendmsg(channel, "ln is Lingala! \n")
        if ircmsg.find ("!lang pfl?") != -1:
            sendmsg(channel, "pfl is Palatinate German! \n")
        if ircmsg.find ("!lang xal?") != -1:
            sendmsg(channel, "xal is Kalmyk! \n")
        if ircmsg.find ("!lang krc?") != -1:
            sendmsg(channel, "krc is Karachay-Balkar! \n")
        if ircmsg.find ("!lang haw?") != -1:
            sendmsg(channel, "haw is Hawaiian! \n")
        if ircmsg.find ("!lang rw?") != -1:
            sendmsg(channel, "rw is Kinyarwanda! \n")
        if ircmsg.find ("!lang pdc?") != -1:
            sendmsg(channel, "pdc is Pennsylvania German! \n")
        if ircmsg.find ("!lang kaa?") != -1:
            sendmsg(channel, "kaa is Karakalpak! \n")
        if ircmsg.find ("!lang to?") != -1:
            sendmsg(channel, "to is Tongan! \n")
        if ircmsg.find ("!lang kl?") != -1:
            sendmsg(channel, "kl is Greenlandic! \n")
        if ircmsg.find ("!lang arc?") != -1:
            sendmsg(channel, "arc is Aramaic! \n")
        if ircmsg.find ("!lang nov?") != -1:
            sendmsg(channel, "nov is Novial! \n")
        if ircmsg.find ("!lang kbd?") != -1:
            sendmsg(channel, "kbd is Kabardian Circassian! \n")
        if ircmsg.find ("!lang av?") != -1:
            sendmsg(channel, "av is Avar! \n")
        if ircmsg.find ("!lang bxr?") != -1:
            sendmsg(channel, "bxr is Buryat! \n")
        if ircmsg.find ("!lang lo?") != -1:
            sendmsg(channel, "lo is Lao! \n")
        if ircmsg.find ("!lang bjn?") != -1:
            sendmsg(channel, "bjn is Banjar! \n")
        if ircmsg.find ("!lang ha?") != -1:
            sendmsg(channel, "ha is Hausa! \n")
        if ircmsg.find ("!lang tet?") != -1:
            sendmsg(channel, "tet is Tetum! \n")
        if ircmsg.find ("!lang pap?") != -1:
            sendmsg(channel, "pap is Papiamentu! \n")
        if ircmsg.find ("!lang tpi?") != -1:
            sendmsg(channel, "tpi is Tok Pisin! \n")
        if ircmsg.find ("!lang na?") != -1:
            sendmsg(channel, "na is Nauruan! \n")
        if ircmsg.find ("!lang tyv?") != -1:
            sendmsg(channel, "tyv is Tuvan! \n")
        if ircmsg.find ("!lang lbe?") != -1:
            sendmsg(channel, "lbe is Lak! \n")
        if ircmsg.find ("!lang jbo?") != -1:
            sendmsg(channel, "jbo is Lojban! \n")
        if ircmsg.find ("!lang ty?") != -1:
            sendmsg(channel, "ty is Tahitian! \n")
        if ircmsg.find ("!lang roa-rup?") != -1:
            sendmsg(channel, "roa-rup is Aromanian! \n")
        if ircmsg.find ("!lang mdf?") != -1:
            sendmsg(channel, "mdf is Moksha! \n")
        if ircmsg.find ("!lang za?") != -1:
            sendmsg(channel, "za is Zhuang! \n")
        if ircmsg.find ("!lang ig?") != -1:
            sendmsg(channel, "ig is Igbo! \n")
        if ircmsg.find ("!lang wo?") != -1:
            sendmsg(channel, "wo is Wolof! \n")
        if ircmsg.find ("!lang nso?") != -1:
            sendmsg(channel, "nso is Northern Sotho! \n")
        if ircmsg.find ("!lang srn?") != -1:
            sendmsg(channel, "srn is Sranan! \n")
        if ircmsg.find ("!lang kg?") != -1:
            sendmsg(channel, "kg is Kongo! \n")
        if ircmsg.find ("!lang ab?") != -1:
            sendmsg(channel, "ab is Abkhazian! \n")
        if ircmsg.find ("!lang ltg?") != -1:
            sendmsg(channel, "ltg is Latgalian! \n")
        if ircmsg.find ("!lang zu?") != -1:
            sendmsg(channel, "zu is Zulu! \n")
        if ircmsg.find ("!lang om?") != -1:
            sendmsg(channel, "om is Oromo! \n")
        if ircmsg.find ("!lang chy?") != -1:
            sendmsg(channel, "chy is Cheyenne! \n")
        if ircmsg.find ("!lang rmy?") != -1:
            sendmsg(channel, "rmy is Romani! \n")
        if ircmsg.find ("!lang cu?") != -1:
            sendmsg(channel, "cu is Old Church Slavonic! \n")
        if ircmsg.find ("!lang tw?") != -1:
            sendmsg(channel, "tw is Twi! \n")
        if ircmsg.find ("!lang mai?") != -1:
            sendmsg(channel, "mai is Maithili! \n")
        if ircmsg.find ("!lang gom?") != -1:
            sendmsg(channel, "gom is Goan Konkani! \n")
        if ircmsg.find ("!lang tn?") != -1:
            sendmsg(channel, "tn is Tswana! \n")
        if ircmsg.find ("!lang chr?") != -1:
            sendmsg(channel, "chr is Cherokee! \n")
        if ircmsg.find ("!lang pih?") != -1:
            sendmsg(channel, "pih is Norfolk! \n")
        if ircmsg.find ("!lang bi?") != -1:
            sendmsg(channel, "bi is Bislama! \n")
        if ircmsg.find ("!lang got?") != -1:
            sendmsg(channel, "got is Gothic! \n")
        if ircmsg.find ("!lang sm?") != -1:
            sendmsg(channel, "sm is Samoan! \n")
        if ircmsg.find ("!lang ss?") != -1:
            sendmsg(channel, "ss is Swati! \n")
        if ircmsg.find ("!lang mo?") != -1:
            sendmsg(channel, "mo is Moldovan! \n")
        if ircmsg.find ("!lang rn?") != -1:
            sendmsg(channel, "rn is Kirundi! \n")
        if ircmsg.find ("!lang ki?") != -1:
            sendmsg(channel, "ki is Kikuyu! \n")
        if ircmsg.find ("!lang xh?") != -1:
            sendmsg(channel, "xh is Xhosa! \n")
        if ircmsg.find ("!lang pnt?") != -1:
            sendmsg(channel, "pnt is Pontic! \n")
        if ircmsg.find ("!lang bm?") != -1:
            sendmsg(channel, "bm is Bambara! \n")
        if ircmsg.find ("!lang iu?") != -1:
            sendmsg(channel, "iu is Inuktitut! \n")
        if ircmsg.find ("!lang ee?") != -1:
            sendmsg(channel, "ee is Ewe! \n")
        if ircmsg.find ("!lang lg?") != -1:
            sendmsg(channel, "lg is Luganda! \n")
        if ircmsg.find ("!lang ts?") != -1:
            sendmsg(channel, "ts is Tsonga! \n")
        if ircmsg.find ("!lang st?") != -1:
            sendmsg(channel, "st is Sesotho! \n")
        if ircmsg.find ("!lang ks?") != -1:
            sendmsg(channel, "ks is Kashmiri! \n")
        if ircmsg.find ("!lang ak?") != -1:
            sendmsg(channel, "ak is Akan! \n")
        if ircmsg.find ("!lang fj?") != -1:
            sendmsg(channel, "fj is Fijian! \n")
        if ircmsg.find ("!lang ik?") != -1:
            sendmsg(channel, "ik is Inupiak! \n")
        if ircmsg.find ("!lang sg?") != -1:
            sendmsg(channel, "sg is Sango! \n")
        if ircmsg.find ("!lang ff?") != -1:
            sendmsg(channel, "ff is Fula! \n")
        if ircmsg.find ("!lang dz?") != -1:
            sendmsg(channel, "dz is Dzongkha! \n")
        if ircmsg.find ("!lang ny?") != -1:
            sendmsg(channel, "ny is Chichewa! \n")
        if ircmsg.find ("!lang ti?") != -1:
            sendmsg(channel, "ti is Tigrinya! \n")
        if ircmsg.find ("!lang ch?") != -1:
            sendmsg(channel, "ch is Chamorro! \n")
        if ircmsg.find ("!lang ve?") != -1:
            sendmsg(channel, "ve is Venda! \n")
        if ircmsg.find ("!lang tum?") != -1:
            sendmsg(channel, "tum is Tumbuka! \n")
        if ircmsg.find ("!lang cr?") != -1:
            sendmsg(channel, "cr is Cree! \n")
        if ircmsg.find ("!lang ng?") != -1:
            sendmsg(channel, "ng is Ndonga! \n")
        if ircmsg.find ("!lang cho?") != -1:
            sendmsg(channel, "cho is Choctaw! \n")
        if ircmsg.find ("!lang kj?") != -1:
            sendmsg(channel, "kj is Kuanyama! \n")
        if ircmsg.find ("!lang mh?") != -1:
            sendmsg(channel, "mh is Marshallese! \n")
        if ircmsg.find ("!lang ho?") != -1:
            sendmsg(channel, "ho is Hiri Motu! \n")
        if ircmsg.find ("!lang ii?") != -1:
            sendmsg(channel, "ii is Sichuan Yi! \n")
        if ircmsg.find ("!lang aa?") != -1:
            sendmsg(channel, "aa is Afar! \n")
        if ircmsg.find ("!lang mus?") != -1:
            sendmsg(channel, "mus is Muscogee! \n")
        if ircmsg.find ("!lang hz?") != -1:
            sendmsg(channel, "hz is Herero! \n")
        if ircmsg.find ("!lang kr?") != -1:
            sendmsg(channel, "kr is Kanuri! \n")

# Main routine

Main()
exit (zero)
