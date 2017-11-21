# python script that recalculates rating of imdb listing
# coded using python 3.6 with Spyder by Josh Glenen on 2017

import requests
import math
from bs4 import BeautifulSoup  # html parser


# temporary algorithm to determine better score
def adjustExtremes(num10, num1, numPos, numNeg, numTotal):
    if numTotal <= 0:
        return [0, 0, 0, "!No ratings available!"]
    if (num1 + num10) / numTotal > 0.33:
        return removeExtremes(num10, num1, numPos, numNeg, numTotal)
    if numPos > numNeg:
        string = "Overall positive reception for "
    else:
        string = "Overall negative reception for "
    if (numPos / numTotal) > 0.1:
        numTotal = numTotal - num10
        num10 = math.floor(num10 / 2)
        numTotal = numTotal + num10
    if (numNeg / numTotal) > 0.1:
        numTotal = numTotal - num1
        num1 = math.floor(num1 / 2)
        numTotal = numTotal + num1
    return [num10, num1, numTotal, string]



def removeExtremes(num10, num1, numPos, numNeg, numTotal):
    MaxMin = numTotal - num10 - num1
    return [0, 0, MaxMin, "Vote weights were corrected for "]


# average calculation
def findMMM(array, total):
    # mode
    i = 0
    y = 0
    temp = 0
    for num in array:
        if temp < num:
            temp = num
            y = i
        i = i + 1
    mode = 10 - y

    # median
    median = math.floor(total / 2)
    i = 0
    y = 0
    for num in array:
        y = y + num
        if y >= median:
            median = 10 - i
            break
        i = i + 1

    # mean
    i = 0
    y = 0
    mean = 0
    for num in array:
        y = 10 - i
        mean = mean + num * y
        i = i + 1
    if total == 0:
        return "!Insufficient ratings!"
    mean = round(mean / total, 2)

    string = "Mean: " + str(mean) + " Median: " + str(median) + " Mode: " + str(mode)
    return string


def getRatings(title):
    # takes an imdb id and name and returns a new rating

    string = "http://www.imdb.com/title/" + title[0] + "/ratings"
    myRequest = requests.get(string)
    myContent = myRequest.content
    myParsed = BeautifulSoup(myContent, "html.parser")
    div = myParsed.find('div', {"class": 'title-ratings-sub-page'})
    table = div.find_all('table')
    lis = table[0].find_all("div", {"class": "leftAligned"})

    # organizes filtered data
    y = -1
    num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for tag in lis:
        ## for debugging purposes ## print(tag.text)
        if (y >= 0) & (y <= 9):
            try:
                stringBuffer = tag.text
                num[y] = int(stringBuffer.replace(',', ''))

            except AttributeError:
                pass
        y = y+1

    # Operations with the data, to customize, alter adjustExtremes function
    numPos = num[0] + num[1] + num[2] + num[3] + num[4]
    numNeg = num[9] + num[8] + num[7] + num[6] + num[5]
    numTot = numPos + numNeg
    array = adjustExtremes(num[0], num[9], numPos, numNeg, numTot)
    num[0] = array[0]
    num[9] = array[1]
    numTot = array[2]
    return array[3] + title[1] + ":\n\n " + findMMM(num, numTot)


def findID(stringIN, index):
    string = "http://www.imdb.com/find?q=" + stringIN + "&s=tt"
    myRequest = requests.get(string)
    myContent = myRequest.content
    myParsed = BeautifulSoup(myContent, "html.parser")
    td = myParsed.find_all('td', {"class": 'result_text'})
                                            # tt = myParsed.find_all('h3', {"class": 'findSectionHeader'})
    try:
        myID1 = str(td[index])
        myID1 = myID1.split('/', 3)
        name = td[index].text.split(' aka', 2)
        return getRatings([myID1[2], name[0]])

    except IndexError:
        return "No title found! Did you check your spelling?"
