#!/usr/bin/python3

import urllib.request
import re
import requests

f = open("links.txt") # Generated with: pdftk Springer\ Ebooks.pdf cat output out.pdf uncompress; strings out.pdf | grep -i http > links.txt
urls = []
for line in f:
    if( line[:4]==r"/URI" ):
        url = line[6:-2]
        urls.append(url)
f.close()

for url in urls:
    
    idx = urls.index(url)
    print("\tAt index: {}".format(idx))
    
    u = urllib.request.urlopen(url)
    # Check box to include error_radius
    
    data = u.read()
    
    lines = data.splitlines(True)
    for i, line in enumerate(lines):
        lines[i] = str(line.decode("UTF-8"))
        
    for line in lines:
        
        if( r"<title>" in line ):
            try:
                title = re.search(r"<title>(.*)\s\|.*\<\/title\>", line).group(1)
                title = title.replace("/", "-")
            except:
                print("No title found for {}".format(url))
                break
            print( "\tDownloading: {}".format(title) )
        
        
        if( 'data-track-action="Book download - pdf"' in line ):
            
            try:
                pdf_url = re.search(r"/content/pdf/.*\.pdf", line).group(0)
            except:
                print("No url found for {}".format(url))
            else:
                pdf_url = "https://link.springer.com" + pdf_url

                pdf_file = requests.get(pdf_url, allow_redirects=True)

                open('Books/{}.pdf'.format(title), 'wb').write(pdf_file.content)
            break
