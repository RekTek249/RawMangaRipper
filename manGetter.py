import requests as r
from bs4 import BeautifulSoup
import re
import shutil
from clint.textui import progress
import os
import zipfile

#Input url
print("Enter the site's url from rawdevart: ")
mainUrl = str(input())

#Input name
print("Enter the manga name: ")
mangaName = str(input())


#Get the html from the mainUrl
mainRequest = r.get(mainUrl)

#Parse the html with bs4
mainSoup = BeautifulSoup(mainRequest.text, features="html.parser")


#Chapter loop, looks for 'a' tags with a title containing "Chapter"
for t in mainSoup.select('a[title*=Chapter]'):
	print("Starting download of chapter...")
	chapterUrl = "https://rawdevart.com" + t['href']

	#Request and parse html from the chapter page
	chapterRequest = r.get(chapterUrl)
	chapterSoup = BeautifulSoup(chapterRequest.text, features="html.parser")

	#Keep track of the current chapter for file names
	currentChapter = -1

	#Script tag loop
	for script in chapterSoup.find_all("script"):
		#len check to make sure we don't get an indexoutofbounds
		if len(script.contents) >= 1:

			#Looking for the script tag containing a "pages" array with links to jpg files
			if "pages" in script.contents[0]:

				#Regex pattern to get a list of urls from the js array
				regex = r"\"[^,]+"
				matches = re.finditer(regex, str(script.contents[0]), re.MULTILINE)

				#Image/jpg/part/page loop
				for matchNum, match in enumerate(matches, start=1):

					#Get rid of the extra double quotes in the url. TODO: do with first regex
					urlToDl = match.group().replace('"', '')

					#[0] = Chapter number
					#[1] = Part number (used for ordering)
					chapterAndPart = re.findall(r"\/\d+", urlToDl)
					chapterAndPart[0] = chapterAndPart[0].replace('/', '')
					chapterAndPart[1] = chapterAndPart[1].replace('/', '')

					#Updating the currentChapter variable. TODO: this can be done better
					if currentChapter != chapterAndPart[0]:
						currentChapter = chapterAndPart[0]

					#Making the subfolders that will contain the jpg files until they're zipped
					if not os.path.exists("mangas/" + mangaName + "/" + chapterAndPart[0]):
						os.makedirs("mangas/" + mangaName + "/"+ chapterAndPart[0])
					
					#mangas/%name%/%chapterID%/%partID%/%name%_%chapterID%_%partID%.jpg
					localN = "mangas/" + mangaName + "/" + chapterAndPart[0] +"/" + mangaName + "_" + chapterAndPart[0] + "_" + chapterAndPart[1] + ".jpg"
					print("Downloading: " + mangaName + "_" + chapterAndPart[0] + "_" + chapterAndPart[1] + ".jpg")

					#Download the jpg file, adding a cute little progress bar
					with r.get(urlToDl, stream=True) as res:
						with open(localN, 'wb+') as f:
							total_length = int(res.headers.get('content-length'))
							for chunk in progress.bar(res.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
								if chunk:
									f.write(chunk)
									f.flush()
				break

	#When a chapter is completely downloaded, make an archive and delete the folder containing the jpg files
	print("Making archive...")
	shutil.make_archive("mangas/" + mangaName + "/output/" + mangaName + "_" + currentChapter, 'zip', "mangas/"  + mangaName + "/" + chapterAndPart[0])
	print("Deleting temporary data...")
	shutil.rmtree("mangas/" + mangaName + "/" + currentChapter)
	print("Done!")
print("Every chapter available has been downloaded! Enjoy!")
