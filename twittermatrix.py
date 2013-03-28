import time
import serial
from numpy import *
import sys
import atexit
import twittersearch

ser = serial.Serial(port='/dev/ttyUSB0',baudrate=460800,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
direction = 0
counter = 0
linelength = 1
x = 4
y = 4
char_map = ""
framebuffer  =  zeros ((3,10,10), dtype=int16 )
# ------------------------------------------------------------------------------------
def init():
    global color_map
    make_charmap()
    ser.open()
    atexit.register(ser.close)
# ------------------------------------------------------------------------------------
def main():
  global testcolor
  current = ""
  init()
  make_charmap()

  while True:
    try:
      isvalid = 1
      latest = twittersearch.searchTweets("\"my favorite color\"").lower()
      raw = latest
      latest = twittersearch.cleanTweet(latest)
      # Filter retweets  
      if (latest == current): isvalid = 0
      #if (latest[0] == "r") and (latest[1] == "r"): isvalid = 0
      if (isvalid == 1):
        current = latest
        print ("*** "+raw)
        print (str(len(raw)) + " Characters")
        analysis = twittersearch.analyzeTweet(current)
        if(analysis > -1): 
          print ("Extracted Color: " + str(twittersearch.generateColor(current, analysis)))
          makePixel(twittersearch.generateColor(current, analysis)) 
    except: 
      pass
    time.sleep(.3)

# ------------------------------------------------------------------------------------
#  ONLY RGB LED MATRIX CONTROLLER STUFF DOWN THERE
# ------------------------------------------------------------------------------------

def makePixel(color):
  global counter
  global linelength
  global framebuffer
  global x
  global y
  global direction
  global testcolor
  for fract in range(0,100):
    ratio =fract/100.0
    framebuffer[0][x][y] = int(color[0]*ratio)
    framebuffer[1][x][y] = int(color[1]*ratio)
    framebuffer[2][x][y] = int(color[2]*ratio)
    senddata()
    time.sleep(.05)
  if (direction == 0): x+=1
  if (direction == 1): y+=1
  if (direction == 2): x-=1
  if (direction == 3): y-=1
  counter +=1
  if (counter == linelength):
    direction +=1
    if (direction == 2): linelength +=2
    if (direction == 4): 
      direction = 0
      linelength +=2
    counter = 0
  if (x == 0) and (y == 9):
    for fract in range(0,100):
      ratio =fract/100.0
      framebuffer[0][x][y] = int(0*ratio)
      framebuffer[1][x][y] = int(100*ratio)
      framebuffer[2][x][y] = int(0*ratio)
      senddata()
      time.sleep(.1)
    framebuffer *= 0
    direction = 0
    counter = 0
    linelength = 1
    x = 4
    y = 4

# ------------------------------------------------------------------------------------
def make_charmap():
  global char_map
  for i in range(0,256):
    char_map = char_map + (chr(int(i/255.0*230)))
# ------------------------------------------------------------------------------------
def senddata():
 # print ("sending data")
  data231 = chr(231)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 9, 0]],
char_map[framebuffer[1, 9, 0]],
char_map[framebuffer[2, 9, 0]],
char_map[framebuffer[0, 9, 1]],
char_map[framebuffer[1, 9, 1]],
char_map[framebuffer[2, 9, 1]],
char_map[framebuffer[0, 8, 1]],
char_map[framebuffer[1, 8, 1]],
char_map[framebuffer[2, 8, 1]],
char_map[framebuffer[0, 8, 0]],
char_map[framebuffer[1, 8, 0]],
char_map[framebuffer[2, 8, 0]])
 
  data232 = chr(232)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 8, 7]],
char_map[framebuffer[1, 8, 7]],
char_map[framebuffer[2, 8, 7]],
char_map[framebuffer[0, 9, 6]],
char_map[framebuffer[1, 9, 6]],
char_map[framebuffer[2, 9, 6]],
char_map[framebuffer[0, 8, 6]],
char_map[framebuffer[1, 8, 6]],
char_map[framebuffer[2, 8, 6]],
char_map[framebuffer[0, 9, 7]],
char_map[framebuffer[1, 9, 7]],
char_map[framebuffer[2, 9, 7]])

  data233 = chr(233)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 6, 9]],
char_map[framebuffer[1, 6, 9]],
char_map[framebuffer[2, 6, 9]],
char_map[framebuffer[0, 7, 9]],
char_map[framebuffer[1, 7, 9]],
char_map[framebuffer[2, 7, 9]],
char_map[framebuffer[0, 6, 8]],
char_map[framebuffer[1, 6, 8]],
char_map[framebuffer[2, 6, 8]],
char_map[framebuffer[0, 7, 8]],
char_map[framebuffer[1, 7, 8]],
char_map[framebuffer[2, 7, 8]])

  data234 = chr(234)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 7, 7]],
char_map[framebuffer[1, 7, 7]],
char_map[framebuffer[2, 7, 7]],
char_map[framebuffer[0, 6, 6]],
char_map[framebuffer[1, 6, 6]],
char_map[framebuffer[2, 6, 6]],
char_map[framebuffer[0, 7, 6]],
char_map[framebuffer[1, 7, 6]],
char_map[framebuffer[2, 7, 6]],
char_map[framebuffer[0, 6, 7]],
char_map[framebuffer[1, 6, 7]],
char_map[framebuffer[2, 6, 7]])

  data235 = chr(235)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 9, 9]],
char_map[framebuffer[1, 9, 9]],
char_map[framebuffer[2, 9, 9]],
char_map[framebuffer[0, 9, 8]],
char_map[framebuffer[1, 9, 8]],
char_map[framebuffer[2, 9, 8]],
char_map[framebuffer[0, 8, 9]],
char_map[framebuffer[1, 8, 9]],
char_map[framebuffer[2, 8, 9]],
char_map[framebuffer[0, 8, 8]],
char_map[framebuffer[1, 8, 8]],
char_map[framebuffer[2, 8, 8]])

  data236 = chr(236)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 5, 5]],
char_map[framebuffer[1, 5, 5]],
char_map[framebuffer[2, 5, 5]],
char_map[framebuffer[0, 5, 4]],
char_map[framebuffer[1, 5, 4]],
char_map[framebuffer[2, 5, 4]],
char_map[framebuffer[0, 4, 4]],
char_map[framebuffer[1, 4, 4]],
char_map[framebuffer[2, 4, 4]],
char_map[framebuffer[0, 4, 5]],
char_map[framebuffer[1, 4, 5]],
char_map[framebuffer[2, 4, 5]])

  data237 = chr(237)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 7, 4]],
char_map[framebuffer[1, 7, 4]],
char_map[framebuffer[2, 7, 4]],
char_map[framebuffer[0, 7, 5]],
char_map[framebuffer[1, 7, 5]],
char_map[framebuffer[2, 7, 5]],
char_map[framebuffer[0, 6, 4]],
char_map[framebuffer[1, 6, 4]],
char_map[framebuffer[2, 6, 4]],
char_map[framebuffer[0, 6, 5]],
char_map[framebuffer[1, 6, 5]],
char_map[framebuffer[2, 6, 5]])

  data238 = chr(238)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 9, 3]],
char_map[framebuffer[1, 9, 3]],
char_map[framebuffer[2, 9, 3]],
char_map[framebuffer[0, 8, 3]],
char_map[framebuffer[1, 8, 3]],
char_map[framebuffer[2, 8, 3]],
char_map[framebuffer[0, 8, 2]],
char_map[framebuffer[1, 8, 2]],
char_map[framebuffer[2, 8, 2]],
char_map[framebuffer[0, 9, 2]],
char_map[framebuffer[1, 9, 2]],
char_map[framebuffer[2, 9, 2]])

  data239 = chr(239)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 9, 4]],
char_map[framebuffer[1, 9, 4]],
char_map[framebuffer[2, 9, 4]],
char_map[framebuffer[0, 8, 5]],
char_map[framebuffer[1, 8, 5]],
char_map[framebuffer[2, 8, 5]],
char_map[framebuffer[0, 9, 5]],
char_map[framebuffer[1, 9, 5]],
char_map[framebuffer[2, 9, 5]],
char_map[framebuffer[0, 8, 4]],
char_map[framebuffer[1, 8, 4]],
char_map[framebuffer[2, 8, 4]])

  data240 = chr(240)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 2, 7]],
char_map[framebuffer[1, 2, 7]],
char_map[framebuffer[2, 2, 7]],
char_map[framebuffer[0, 3, 7]],
char_map[framebuffer[1, 3, 7]],
char_map[framebuffer[2, 3, 7]],
char_map[framebuffer[0, 3, 6]],
char_map[framebuffer[1, 3, 6]],
char_map[framebuffer[2, 3, 6]],
char_map[framebuffer[0, 2, 6]],
char_map[framebuffer[1, 2, 6]],
char_map[framebuffer[2, 2, 6]])

  data241 = chr(241)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 2, 8]],
char_map[framebuffer[1, 2, 8]],
char_map[framebuffer[2, 2, 8]],
char_map[framebuffer[0, 2, 9]],
char_map[framebuffer[1, 2, 9]],
char_map[framebuffer[2, 2, 9]],
char_map[framebuffer[0, 3, 9]],
char_map[framebuffer[1, 3, 9]],
char_map[framebuffer[2, 3, 9]],
char_map[framebuffer[0, 3, 8]],
char_map[framebuffer[1, 3, 8]],
char_map[framebuffer[2, 3, 8]])

  data242 = chr(242)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 4, 8]],
char_map[framebuffer[1, 4, 8]],
char_map[framebuffer[2, 4, 8]],
char_map[framebuffer[0, 4, 9]],
char_map[framebuffer[1, 4, 9]],
char_map[framebuffer[2, 4, 9]],
char_map[framebuffer[0, 5, 9]],
char_map[framebuffer[1, 5, 9]],
char_map[framebuffer[2, 5, 9]],
char_map[framebuffer[0, 5, 8]],
char_map[framebuffer[1, 5, 8]],
char_map[framebuffer[2, 5, 8]])

  data243 = chr(243)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 4, 7]],
char_map[framebuffer[1, 4, 7]],
char_map[framebuffer[2, 4, 7]],
char_map[framebuffer[0, 4, 6]],
char_map[framebuffer[1, 4, 6]],
char_map[framebuffer[2, 4, 6]],
char_map[framebuffer[0, 5, 6]],
char_map[framebuffer[1, 5, 6]],
char_map[framebuffer[2, 5, 6]],
char_map[framebuffer[0, 5, 7]],
char_map[framebuffer[1, 5, 7]],
char_map[framebuffer[2, 5, 7]])

  data244 = chr(244)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 3, 2]],
char_map[framebuffer[1, 3, 2]],
char_map[framebuffer[2, 3, 2]],
char_map[framebuffer[0, 2, 3]],
char_map[framebuffer[1, 2, 3]],
char_map[framebuffer[2, 2, 3]],
char_map[framebuffer[0, 3, 3]],
char_map[framebuffer[1, 3, 3]],
char_map[framebuffer[2, 3, 3]],
char_map[framebuffer[0, 2, 2]],
char_map[framebuffer[1, 2, 2]],
char_map[framebuffer[2, 2, 2]])

  data245 = chr(245)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 2, 1]],
char_map[framebuffer[1, 2, 1]],
char_map[framebuffer[2, 2, 1]],
char_map[framebuffer[0, 3, 1]],
char_map[framebuffer[1, 3, 1]],
char_map[framebuffer[2, 3, 1]],
char_map[framebuffer[0, 3, 0]],
char_map[framebuffer[1, 3, 0]],
char_map[framebuffer[2, 3, 0]],
char_map[framebuffer[0, 2, 0]],
char_map[framebuffer[1, 2, 0]],
char_map[framebuffer[2, 2, 0]])

  data246 = chr(246)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 1, 2]],
char_map[framebuffer[1, 1, 2]],
char_map[framebuffer[2, 1, 2]],
char_map[framebuffer[0, 1, 3]],
char_map[framebuffer[1, 1, 3]],
char_map[framebuffer[2, 1, 3]],
char_map[framebuffer[0, 0, 2]],
char_map[framebuffer[1, 0, 2]],
char_map[framebuffer[2, 0, 2]],
char_map[framebuffer[0, 0, 3]],
char_map[framebuffer[1, 0, 3]],
char_map[framebuffer[2, 0, 3]])

  data247 = chr(247)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 1, 0]],
char_map[framebuffer[1, 1, 0]],
char_map[framebuffer[2, 1, 0]],
char_map[framebuffer[0, 0, 0]],
char_map[framebuffer[1, 0, 0]],
char_map[framebuffer[2, 0, 0]],
char_map[framebuffer[0, 1, 1]],
char_map[framebuffer[1, 1, 1]],
char_map[framebuffer[2, 1, 1]],
char_map[framebuffer[0, 0, 1]],
char_map[framebuffer[1, 0, 1]],
char_map[framebuffer[2, 0, 1]])

  data248 = chr(248)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 6, 0]],
char_map[framebuffer[1, 6, 0]],
char_map[framebuffer[2, 6, 0]],
char_map[framebuffer[0, 7, 1]],
char_map[framebuffer[1, 7, 1]],
char_map[framebuffer[2, 7, 1]],
char_map[framebuffer[0, 7, 0]],
char_map[framebuffer[1, 7, 0]],
char_map[framebuffer[2, 7, 0]],
char_map[framebuffer[0, 6, 1]],
char_map[framebuffer[1, 6, 1]],
char_map[framebuffer[2, 6, 1]])

  data249 = chr(249)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 6, 3]],
char_map[framebuffer[1, 6, 3]],
char_map[framebuffer[2, 6, 3]],
char_map[framebuffer[0, 6, 2]],
char_map[framebuffer[1, 6, 2]],
char_map[framebuffer[2, 6, 2]],
char_map[framebuffer[0, 7, 2]],
char_map[framebuffer[1, 7, 2]],
char_map[framebuffer[2, 7, 2]],
char_map[framebuffer[0, 7, 3]],
char_map[framebuffer[1, 7, 3]],
char_map[framebuffer[2, 7, 3]])

  data250 = chr(250)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 5, 2]],
char_map[framebuffer[1, 5, 2]],
char_map[framebuffer[2, 5, 2]],
char_map[framebuffer[0, 5, 3]],
char_map[framebuffer[1, 5, 3]],
char_map[framebuffer[2, 5, 3]],
char_map[framebuffer[0, 4, 2]],
char_map[framebuffer[1, 4, 2]],
char_map[framebuffer[2, 4, 2]],
char_map[framebuffer[0, 4, 3]],
char_map[framebuffer[1, 4, 3]],
char_map[framebuffer[2, 4, 3]])

  data251 = chr(251)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 5, 0]],
char_map[framebuffer[1, 5, 0]],
char_map[framebuffer[2, 5, 0]],
char_map[framebuffer[0, 5, 1]],
char_map[framebuffer[1, 5, 1]],
char_map[framebuffer[2, 5, 1]],
char_map[framebuffer[0, 4, 1]],
char_map[framebuffer[1, 4, 1]],
char_map[framebuffer[2, 4, 1]],
char_map[framebuffer[0, 4, 0]],
char_map[framebuffer[1, 4, 0]],
char_map[framebuffer[2, 4, 0]])

  data252 = chr(252)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 0, 4]],
char_map[framebuffer[1, 0, 4]],
char_map[framebuffer[2, 0, 4]],
char_map[framebuffer[0, 0, 5]],
char_map[framebuffer[1, 0, 5]],
char_map[framebuffer[2, 0, 5]],
char_map[framebuffer[0, 1, 5]],
char_map[framebuffer[1, 1, 5]],
char_map[framebuffer[2, 1, 5]],
char_map[framebuffer[0, 1, 4]],
char_map[framebuffer[1, 1, 4]],
char_map[framebuffer[2, 1, 4]])

  data253 = chr(253)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 2, 5]],
char_map[framebuffer[1, 2, 5]],
char_map[framebuffer[2, 2, 5]],
char_map[framebuffer[0, 2, 4]],
char_map[framebuffer[1, 2, 4]],
char_map[framebuffer[2, 2, 4]],
char_map[framebuffer[0, 3, 5]],
char_map[framebuffer[1, 3, 5]],
char_map[framebuffer[2, 3, 5]],
char_map[framebuffer[0, 3, 4]],
char_map[framebuffer[1, 3, 4]],
char_map[framebuffer[2, 3, 4]])

  data254 = chr(254)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 0, 9]],
char_map[framebuffer[1, 0, 9]],
char_map[framebuffer[2, 0, 9]],
char_map[framebuffer[0, 1, 9]],
char_map[framebuffer[1, 1, 9]],
char_map[framebuffer[2, 1, 9]],
char_map[framebuffer[0, 0, 8]],
char_map[framebuffer[1, 0, 8]],
char_map[framebuffer[2, 0, 8]],
char_map[framebuffer[0, 1, 8]],
char_map[framebuffer[1, 1, 8]],
char_map[framebuffer[2, 1, 8]])

  data255 = chr(255)+"%s%s%s%s%s%s%s%s%s%s%s%s" % (
char_map[framebuffer[0, 1, 7]],
char_map[framebuffer[1, 1, 7]],
char_map[framebuffer[2, 1, 7]],
char_map[framebuffer[0, 1, 6]],
char_map[framebuffer[1, 1, 6]],
char_map[framebuffer[2, 1, 6]],
char_map[framebuffer[0, 0, 7]],
char_map[framebuffer[1, 0, 7]],
char_map[framebuffer[2, 0, 7]],
char_map[framebuffer[0, 0, 6]],
char_map[framebuffer[1, 0, 6]],
char_map[framebuffer[2, 0, 6]])


  
  ser.write(data231)
  ser.write(data232)
  ser.write(data233)
  ser.write(data234)
  ser.write(data235)
  ser.write(data236)
  ser.write(data237)
  ser.write(data238)
  ser.write(data239)
  ser.write(data240)
  ser.write(data241)
  ser.write(data242)
  ser.write(data243)
  ser.write(data244)
  ser.write(data245)
  ser.write(data246)
  ser.write(data247)
  ser.write(data248)
  ser.write(data249)
  ser.write(data250)
  ser.write(data251)
  ser.write(data252)
  ser.write(data253)
  ser.write(data254)
  ser.write(data255)
  


# ------------------------------------------------------------------------------------


if __name__ == '__main__': main()
