#python script that recalculates rating of imdb listing
#coded using python 3.6 with Spyder by Josh Glenen on 2017

import requests
import math
from bs4 import BeautifulSoup #html parser

#temporary algorythm to determine better score
def adjustExtremes( num10, num1, numPos, numNeg, numTotal):
    if (num1+num10) / numTotal > 0.5:
        return removeExtremes( num10, num1, numPos, numNeg, numTotal)
    elif numPos > numNeg:
        print("Overall positive reception")
        numTotal = numTotal - num10
        num10  = math.floor(num10/2)
        numTotal = numTotal + num10
        num1 = 0
    elif numPos < numNeg:
        print("Overall negative reception")
        numTotal = numTotal - num1
        num1 = math.floor(num1/2)
        numTotal = numTotal + num10
        num10 = 0
    toReturn = [num10,num1,numTotal]
    return toReturn

def removeExtremes( num10, num1, numPos, numNeg, numTotal):
    print("10's and 1's were removed")
    MaxMin = numTotal - num10 - num1 
    toReturn = [num10,num1,MaxMin]
    return toReturn

#average calculation
def findMMM(array, total):
    
    #mode
    i = 0
    y = 0
    temp = 0
    for num in array:
        if temp < num:
            temp = num
            y = i
        i = i+1
    mode = 10 - y
    
    #median
    median = math.floor(total/2)
    i = 0
    y = 0
    for num in array:
        y = y + num
        if y >= median:
            median = 10 - i
            break
        i = i + 1
    
    #mean
    i = 0
    y = 0
    mean = 0
    for num in array:
        y = 10 - i
        mean = mean +num*y
        i = i+1
    mean = round(mean/total,2)
    
    string = "Mean: " + str(mean) + " Median: " + str(median) + " Mode: " + str(mode)
    print(string)



#takes an imdb url and finds the id, then rebuilds the url for consistancy
string = input("Paste the URL of the title: ")
idImdb = string.split('/', 5)
string = "http://www.imdb.com/title/" + idImdb[4] + "/ratings?"
print(string)
                            
#scrapes the html                  
myRequest = requests.get(string)
myContent = myRequest.content
myParsed = BeautifulSoup(myContent, "html.parser")
div = myParsed.find('div', {"id":'tn15content'})
table = div.find_all('table')
lis = table[0].find_all("td", {"align":"right"})

#organizes filtered data
x = 0
y = 0
num = [0,0,0,0,0,0,0,0,0,0]
for tag in lis:
   if x % 2 != 0:
       try: 
           num[y] = int(tag.text)      
       except AttributeError:
           pass
       y=y+1
   x=x+1

#Operations with the data, open for customization
numPos = num[0]+num[1]+num[2]+num[3]+num[4]
numNeg = num[9]+num[8]+num[7]+num[6]+num[5]
numTot = numPos+numNeg
array = adjustExtremes(num[0],num[9],numPos,numNeg,numTot)
num[0] = array[0]
num[9] = array[1]
numTot = array[2]
findMMM(num,numTot)





