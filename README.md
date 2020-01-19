# RawMangaRipper
A small python script to download mangas from (currently only) rawdevart.com.
The purpose of this was to be able to read raw manga on my phone (ios & android).
While there are many available web readers, they are not really fit for a phone.
This utility turns the web reader manga into a .zip folder, readable by many phone 
(and desktop) apps. Notably, Manga Storm CBR (ios) and Comicat (android).

# Getting started
Simply download the python script, and run. Python3 needed.
The script takes two inputs (not parameters), the URL from rawdevart.com of the
page where all chapters are listed. Example: https://rawdevart.com/comic/tate-no-yuusha-no-nariagari/
The second one is the name of the manga, which is only used for file names (can be anything you want).
It will then create zips for every chapter. The output is located at %user%/Desktop/mangas/output/%file%.zip

# It's python, make it yours!
This wasn't something I intended to publish, so it's not very customizable...yet. If you wish for it to do
something differently, feel free to edit it to make it suit your needs. And of course, push it!

# Future plans

- Allow for more directories than desktop (relative).
- Allow for more than one output format (cbr, cbz...)
- Have more than one input site
