#!/usr/bin/env python

import urllib2
import sys, os

try:
    from bs4 import BeautifulSoup
except ImportError as e:
    print 'You must have beautifulsoup pkg, install by pip install beautifulsoup4'.upper()
    sys.exit(1)

HEADERS={
    'User-Agent': 'Mozilla/5.0'
}

def get_good_html(file_like_object):
    # original html have 2 body tags, it's suck.
    # this function gonna wipe that out.
    flag=False
    done=[]
    for line in file_like_object.readlines():
        if "<html" in line:flag=True
        flag and done.append(line)
    return ''.join(done)

def get_pics_list(soup):
    #[ (referrer, url), ...]
    # We can implement handle for each image server
    find_ahref_in_soup = soup.find('div',{'class':'post'}).find_all('a')
    if find_ahref_in_soup:
        print 'Found ahref in soup.[oozha.com]'
        return [(a.attrs['href'], a.findChild('img').attrs['src']) for a in find_ahref_in_soup if a.findChild('img')]

    find_img_in_soup = soup.find_all('img',{'class':'bbc_img'})
    if find_img_in_soup:
        print 'Found img in soup.[impur.com]'
        return [('', i.attrs['src']) for i in find_img_in_soup]

    return []

def down(fname, url, folder_name):
    real_url = url[1]
    d = {
        'Accept':'image/png,image/*;q=0.8,*/*;q=0.5',
        'Accept-Encoding':'gzip, deflate',
    }
    if url[0] != '': d['Referer'] = url[0]
    HEADERS.update(d)
    try:
        img = urllib2.urlopen(urllib2.Request(real_url, None, HEADERS))
    except Exception as e:
        print 'Cannot proces url %s' % real_url
        return
    fullname = '%s-%s' % (fname, real_url.split('/')[-1])
    with open('./%s/%s' % (folder_name, fullname), 'wb') as f:
        while True:
            t = img.read(16*1024)
            if not t:break
            f.write(t)
    print 'Writed %s' % fullname

def center_ops(url):
    good_html_string = get_good_html(urllib2.urlopen(url))
    soup = BeautifulSoup(good_html_string)
    for index, dat in enumerate(get_pics_list(soup)):
        down(index, dat, folder_name)

if __name__ == '__main__':
    assert len(sys.argv) == 3, 'Hey, let\'s params like this -> <url> <folder_name>'
    url = sys.argv[1]
    folder_name = sys.argv[2]

    if not os.path.isdir(folder_name):
        os.mkdir('./%s' % folder_name)
    center_ops(url)
