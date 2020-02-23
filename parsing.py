import string
import re

text_string = ";Good morning!, Welcome to HackCU. Today is Saturday;. Where are my pants?! "


#takes every word and makes it a separate string
#uses regular expressions 
m = re.sub("[^\w]", " ", text_string).split()

print(m)