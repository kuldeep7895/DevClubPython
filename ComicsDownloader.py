#The Project automatically creates directory and downloads the comics of desired month to the desired directories
import html5lib
import bs4
import requests
import os

# INVOKING THE INPUT.TXT FILE

myfile = open('input.txt')
content = myfile.read()
all_contents = []
all_contents = content.split()


# METHOD THAT DOWNLOADS COMICS OF SPECIFIED MONTH AND WRITER

def download(month, year, writer):
    month=str(month[0]).capitalize()+month[1:]
    os.makedirs(year+"\\"+month)
    URL = 'http://explosm.net/comics/archive'
    req = requests.get(URL)
    soup = bs4.BeautifulSoup(req.content, 'html5lib')
    linksarr = []
    newurl = ''
    for i in soup.find_all("a"):
        linksarr.append(i)

    for i in range(len(linksarr)):
        if month in str(linksarr[i]) and year in str(linksarr[i]):
            newurl = str(linksarr[i])
            newurl = newurl[9:newurl.index('>') - 1]

    newreq = requests.get('http://explosm.net' + newurl)

    newsoup = bs4.BeautifulSoup(newreq.content, 'html5lib')
    linksarr1 = []
    newurl0 = ''

    for i in newsoup.find_all('a'):
        linksarr1.append(i)

    for i in range(len(linksarr1)):
        if writer in str(linksarr1[i]):
            newurl0 = str(linksarr1[i])
            newurl0 = newurl0[9:newurl0.index('>') - 1]



    newreq1 = requests.get('http://explosm.net' + newurl0)
    newsoup2 = bs4.BeautifulSoup(newreq1.content, 'html5lib')
    date=1
    linksarr2 = []
    newurl2 = ''
    for i in newsoup2.find_all('a'):
        linksarr2.append(i)
    for i in range(len(linksarr2)):
        if 'comic-thumbnail' in str(linksarr2[i]):
            newurl2 = str(linksarr2[i])
            used = newurl2.split(' ')
            newurl2 = used[1]
            newurl2 = 'http://explosm.net' + newurl2[6:newurl2.index('>') - 2]
            newreq2 = requests.get(newurl2)
            newsoup3 = bs4.BeautifulSoup(newreq2.content, 'html5lib')
            newurl3 = str(newsoup3.find_all(id='main-comic'))
            usedagain = newurl3.split()
            datefinder=str(str(newsoup3.find(id='comic-author'))).split()
            date=str(datefinder[2])
            date=date[0:date.index(">")-4]

            newurl3 = str(usedagain[2])
            newurl3 = 'http://' + newurl3[7:newurl3.index('>') - 2]

            myfile = open(year+"\\"+month+"\\"+date+"-"+writer+".png",'wb')
            newreq3 = requests.get(newurl3)
            myfile.write(newreq3.content)
            

# downloads the content
monthjoin={"january":1,"february":2,"march":3,"april":4,"may":5,"june":6,"july":7,"august":8,"september":9,"october":10,"november":11,"december":12}
remonthjoin={1:"january",2:"february",3:"march",4:"april",5:"may",6:"june",7:"july",8:"august",9:"september",10:"october",11:"november",12:"december"}

initialmonth=monthjoin[all_contents[0]]
initialyear=int(all_contents[1])
year=int(all_contents[1])
while year<=int(all_contents[3]):
    month=initialmonth
    while month<=12 and month>=initialmonth:
        download(remonthjoin[month],str(year), all_contents[4])
        if year == int(all_contents[3]) and month >= monthjoin[str(all_contents[2])]:
            month=13
        month=month+1
        print(month)
    initialmonth=1
    print(year)
    year+=1

