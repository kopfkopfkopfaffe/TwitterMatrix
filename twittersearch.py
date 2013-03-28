import urllib
import simplejson
import time

current = ""
isvalid = 1
colorlist = ["grey","lime","white","violet","yellow","orange","pink","purple","blue","red","green"]
colors = [[100,100,100] , [191,255,0] , [255,255,255] , [143,0,255] , [255,255,0] , [255,127,0] , [255,0,102] , [128,0,128], [0,0,255] , [255,0,0] , [0,255,0]]

# ------------------------------------------------------------------------------------
# PROPS for tweet-searching go to GLOWING PYTHON
# http://glowingpython.blogspot.de/2011/04/how-to-use-twitter-search-api.html
# ------------------------------------------------------------------------------------

def searchTweets(query):
 search = urllib.urlopen("http://search.twitter.com/search.json?q="+query+"&result_type=recent")
 dict = simplejson.loads(search.read())
 result = dict["results"][0]
 return result["text"]

def analyzeTweet(tweet):
 match = -1
 for word in tweet.split():
   if (match > -1): break
   for colornumber in range(0,len(colorlist)):
     #print("comparing "+ word + " and "+ colorlist[color])
     if (word == colorlist[colornumber]): 
       match = colornumber
       break
 return match

def generateColor(tweet, colornumber):
  mycolor = [0,0,0]
  length = len(tweet)
  ratio = length/140.0
  if (ratio > 1): ratio = 1.0
  #print ("Ratio: " + str(ratio))
  for element in range(0,len(colors[colornumber])):
    mycolor[element] = int(ratio*colors[colornumber][element])
  return mycolor

def cleanTweet(tweet):
  tweetlist = list(tweet)
  for letter in range(0,len(tweetlist)):
    if (ord(tweetlist[letter])<97) or (ord(tweetlist[letter])>122):
      tweetlist[letter] = " "
  tweet = "".join(tweetlist)
  return tweet

# Test loop for standalone operation:

#while(1):
#  isvalid = 1
#  latest = searchTweets("\"my favorite color\"").lower()
#  latest=cleanTweet(latest)
#  if (latest == current): isvalid = 0
#  if (latest[0] == "R") and (latest[1] == "T"): isvalid = 0
#  #for bit in latest:
#  #  if (bit == "@"): isvalid = 0
#  if (isvalid == 1):
#    current = latest
#    print ("*** "+current)
#    print len(current)
#    analysis = analyzeTweet(current)
#    if(analysis > -1): 
#      print analysis
#      print generateColor(current, analysis)
#  time.sleep(3)

