import requests as r
from bs4 import BeautifulSoup
import re
import shutil
from clint.textui import progress
import os
import zipfile
print("Enter the site's url from rawdevart: ")
mainUrl = str(input()) #https://rawdevart.com/comic/tate-no-yuusha-no-nariagari/
print("Enter the manga name: ")
mangaName = str(input())

mainRequest = r.get(mainUrl)

mainSoup = BeautifulSoup(mainRequest.text, features="html.parser")

for t in mainSoup.select('a[title*=Chapter]'):
	print("Starting download of chapter...")
	chapterUrl = "https://rawdevart.com" + t['href']
	chapterRequest = r.get(chapterUrl)
	chapterSoup = BeautifulSoup(chapterRequest.text, features="html.parser")
	currentChapter = -1
	for script in chapterSoup.find_all("script"):
		if len(script.contents) >= 1:
			if "pages" in script.contents[0]:
				regex = r"\"[^,;]+"
				matches = re.finditer(regex, str(script.contents[0]), re.MULTILINE)
				for matchNum, match in enumerate(matches, start=1):
					urlToDl = match.group().replace('"', '')
					chapterAndPart = re.findall(r"\/\d+", urlToDl)
					if currentChapter != chapterAndPart[0].replace('/', ''):
						currentChapter = chapterAndPart[0].replace('/', '')
					if not os.path.exists("mangas/" + mangaName + "/" + chapterAndPart[0].replace('/', '')):
						os.makedirs("mangas/" + mangaName + "/"+ chapterAndPart[0].replace('/', ''))
					localN = str(os.path.join(os.environ["HOMEPATH"], "Desktop")) + "/mangas/" + mangaName + "/" + chapterAndPart[0].replace('/', '') +"/" + mangaName + "_" + chapterAndPart[0].replace('/', '') + "_" + chapterAndPart[1].replace('/', '') + ".jpg"
					print("Downloading: " + mangaName + "_" + chapterAndPart[0].replace('/', '') + "_" + chapterAndPart[1].replace('/', '') + ".jpg")
					with r.get(urlToDl, stream=True) as res:
						with open(localN, 'wb+') as f:
							total_length = int(res.headers.get('content-length'))
							for chunk in progress.bar(res.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
								if chunk:
									f.write(chunk)
									f.flush()
				break
	print("Making archive...")
	shutil.make_archive(str(os.path.join(os.environ["HOMEPATH"], "Desktop")) + "/mangas/" + mangaName + "/output/" + mangaName + "_" + currentChapter, 'zip', str(os.path.join(os.environ["HOMEPATH"], "Desktop")) + "/mangas/"  + mangaName + "/" + chapterAndPart[0].replace('/', ''))
	print("Deleting temporary data...")
	shutil.rmtree(str(os.path.join(os.environ["HOMEPATH"], "Desktop")) + "/mangas/" + mangaName + "/" + currentChapter)
	print("Done!")
print("Every chapter available has been downloaded! Enjoy!")
