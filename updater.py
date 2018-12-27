from bs4 import BeautifulSoup as bs
from urllib import request
import os
import time
import wget

URL = 'https://www.umensch.com/downloads/'

def get_version_link():
    sauce = request.urlopen(URL).read()
    soup = bs(sauce, "html.parser")


    for ptag in soup.find_all('p'):
        pt = ptag.text
        if "Latest version:" in pt:
            _, version = pt.split(":")
            version.replace(" ", "")
            #print"version: ", version)
            if version is not None:
                for atag in soup.find_all('a'):
                    at = atag.text
                    title = atag.get('title')
                    #print"title: ", title)
                    href = atag.get('href')
                    try:
                        if version in title and href != None:
                            #print"href: {}, version: {}".format(href, version))
                            return href, version
                    except:
                        pass

    return None, None


def check_for_update(v):
    dwnl, sitev = get_version_link()

    vers1 = list(v)
    vers1.remove(vers1[-2])
    vers1 = float("".join(vers1))

    # print("fv1: ", vers1)

    vers2 = list(sitev)
    vers2.remove(vers2[-2])
    vers2 = float("".join(vers2))

    # print("fv2: ", vers2)
    if vers2 > vers1:
        return True, dwnl, sitev
    else:
        return False, 'bla', 'bla'


def download_new_vers(dwnl, location):
    try:
        filename = wget.download(dwnl, out=location)
        return True 
    except:
        return False

    #subprocess.call(r'wget -r --accept "*.exe,*.dll,*.zip,*.msi,*.rar,*.iso" ftp://ftp.apple.asimov.com/ -P e:\e', shell=True)


if __name__ == '__main__':
    link = 'https://www.umensch.com/downloads/'
    h, pv = get_version_link(link)
    #print"h: {}, pv: {}".format(h, pv))
    #print("soup: ", soop)
