#Project: Downloading all XKCD Comics- Chapter 11 Automate the Boring Stuff
#Loads the XKCD homepage
#Saves the comic on that page and goes to the previous page and downloads that comic
#Repeats until it reaches the first page

import requests, os, bs4

url = 'http://xkcd.com' #initial url
os.makedirs('xkcd', exist_ok=True) #store comics in ./xkcd
while not url.endswith('#'):
    print('downloading page %s...' % url)
    #download the page
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text)
    #find the URL of the comic image
    comicElem = soup.select('comic img')
    if comicElem == []:
        print('Could not find that image')
    else:
        comicURL = 'http://' + comicElem[0].get('src')
        #download the image
        print('Downloading image %s...' % (comicURL))
        res = requests.get(comicURL)
        res.raise_for_status()

        #save file to ./xkcd
        imagefile = open(os.path.join('xkcd', os.path.basename(comicURL)), 'wb')
        for chunk in res.iter_content(100000):
            imagefile.write(chunk)
        imagefile.close()
    #get the previous link
    prev_link = soup.select('a[rel = "prev"]')[0]
    url = 'http://xkcd.com' + prev_link.get('href')

print('done')
