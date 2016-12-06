#!/usr/bin/python3

import os
import requests
import bs4
import zipfile
import shutil

# Link to download subtitles for your RELEASE directly
url = 'https://subscene.com/subtitles/release?q='

workPath = os.path.dirname(os.path.realpath(__file__))
pwd = workPath + '/'
dir = os.listdir(workPath)

# Check if folder contains video file
for metaFile in dir:
    if metaFile[-3:] == "mkv":
        break
metaName = metaFile[0:-4]


def scrapeSubtitleLink(url, bsTag):
    # Retrieve all related subtitles
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elems = soup.select(bsTag)
    # Find English Subtitle with best match in the results
    i = 0
    for elem in elems:
        if elem.text.strip()[0:7] == 'English':
            okSub = i
            if elem.text.strip()[7:].strip() == metaName:
                bestSub = i
                break
        i += 1
    if bestSub:
        bestSub = okSub
    return 'https://subscene.com' + elems[bestSub].a.get('href').strip()


def scrapeSubtitleLink2(url, bsTag):
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elem = soup.select(bsTag)
    return 'https://subscene.com' + elem[0].a.get('href').strip()


def downloadSubZip(url):
    subZip = requests.get(url)
    with open(pwd + 'subZip.zip', 'wb') as fd:
        for chunk in subZip.iter_content(100000):
            fd.write(chunk)
    return pwd + 'subZip.zip'


def extractSub(file):
    theZip = zipfile.ZipFile(file)
    filesInZip = theZip.namelist()
    if len(filesInZip) == 1:
        subName = str(filesInZip[0])
        print('One file in archive found: ' + subName)
        theZip.extractall(path=workPath)
        shutil.move(pwd + subName, pwd + metaName + subName[-4:])
        return pwd + metaName + subName[-4:]


# Find the movie
subUrl = scrapeSubtitleLink(url+metaName, 'td[class=a1]')
print("Movie found: " + subUrl)

# Identify correct subtitle
downloadUrl = scrapeSubtitleLink2(subUrl, 'div[class=download]')
print("Download from: " + downloadUrl)

# Download the zip file
subtlzip = downloadSubZip(downloadUrl)
print("Zip saved to: " + subtlzip)

# Extract and raname subtitle
readySub = extractSub(pwd + 'subZip.zip')
print("Subtitle ready: " + readySub)

# Delete zip file
os.remove(pwd + 'subZip.zip')
print('clean up')
