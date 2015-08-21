#!/bin/bash

qdel avicbotirc
sleep 60
jstart -mem 500m ~/irc/avicbotirc.sh

