# P1060.  Web crawler program.

import urllib.request, csv

'''
Some useful functions:
save_page(data) = saves a web page to a temporary file.  I used this during debugging.
load_page() = loads saved page from temporary file. I used this during debugging.
strip_quotes(str) = assumes that str has at least 2 quote marks in it.  returns whatever is in between the first and second set of quote marks.
get_base_url(str) = for a string such as "http://example.com/home/pages/thispage.htm", it returns "http://example.com".
load_names() = pulls out the targets of the web crawling function for a file names crawl_targets.data.
add_crawl_queue(str) = saves url to the sites to be crawled through.
add_to_hist(str) = saves url into the history file "crawl_hist.data".
add_to_results(str) = Saves URL and what was matched on the page into the results file "crawl_results.data".
get_next_url() = Figures out, based on the queue and history, what is the next url to be crawled.
'''

def save_page(d):
    f = open("temp.dat",mode = "w", encoding = "utf-8")
    f.write(d)
    f.close()

def load_page():
    f = open("temp.dat",mode = "r", encoding = "utf-8")
    d = f.read()
    f.close()
    return d

def strip_quotes(b):
    c = ""
    adding = False
    for x in b:
        if x == "\"":
            if adding:
                break
            else:
                adding = True
        elif adding:
            c = c + x
    return c

def get_base_url(my_url):
    base_url = my_url[0:8]
    for x in range(8,len(my_url)):
        if my_url[x] == "/":
            break
        else:
            base_url = base_url +my_url[x]
    return base_url

def load_names():
    f = open("crawl_targets.data",mode = 'r', encoding = 'utf-8')
    d = f.read()
    f.close()
    data = []
    line = ""
    for x in d:
        if x == "\n":
            data.append(line.upper())
            line = ""
        else:
            line = line +x
    return data

def add_crawl_queue(new_url):
    f = open("crawl_queue.data", mode = "a", encoding = "utf-8")
    f.write(new_url+"\n")
    f.close()

def add_to_hist(my_url):
    f = open("crawl_hist.data", mode = "a", encoding = "utf-8")
    f.write(my_url+"\n")
    f.close()

def add_to_results(name, my_url):
    f = open("crawl_results.data", mode = "a", encoding = "utf-8")
    f.write(my_url+" ,"+name+"\n")
    f.close()

def get_next_url():
    f = open("crawl_hist.data", mode = "r", encoding = "utf-8")
    data = f.read()
    data_list = []
    my_url = ""
    for x in data:
        if x == "\n":
            data_list.append(my_url)
            my_url = ""
        else:
            my_url += x
    f.close()
    f = open("crawl_queue.data", mode = "r", encoding = "utf-8")
    looping = True
    while looping:
        ws = f.readline()
        ws = ws[0:-1]
        if not(ws in data_list):
            looping = False
    f.close()
    return ws
    
'''
PROGRAM STARTS HERE
'''
#determine start URL
my_url = get_next_url()
#load strings to be matched on web pages.
names = load_names()
for x in range(1000):
    #Retrieve the web page
    while True:
        try:
            print("* starting to process:",my_url)
            ws = urllib.request.urlopen(my_url)
            break
        except IOError:
            print("Bad URL:",my_url)
            add_to_hist(my_url)
            my_url = get_next_url()
        except ValueError:
            print("Bad URL:",my_url)
            add_to_hist(my_url)
            my_url = get_next_url()            
    data1 = ws.read()
    data = data1.decode(encoding='utf-8', errors='ignore')

    # strip all tags from document and save each tag into list a
    a = []
    adding = False
    count = 0
    for x in data:
        if x == ">":
            adding = False
        if adding:
            a[count] = a[count] + x
        if x == "<":
            adding = True
            a.append("")
            count = len(a)-1
    # look at each tag in list a and save those which are href's into list b
    b = []
    for x in a:
        if x[0:6] == "a href":
            b.append(strip_quotes(x))

    base_url = get_base_url(my_url)
    stop_domains = ['google','facebook','pinterest','twitter','amazon',
                    'cyndislist','cialis','mailto','cafepress'] # I may want to create a file for these.

    # some checking on the urls here.
    for x in b:
        f_url = ""
        if x != "":
            if x[0] == '/':
                f_url = base_url+x #expand relative links
            elif x[0] != '#':
                f_url = x
            for y in stop_domains:
                if y in f_url:
                    f_url = ""
            if f_url != "":
                add_crawl_queue(f_url)
    
    # now go back through the web page which was retrieved and create bag of words.
    words = set() # we will store these into a set.
    adding = False
    word_add = ""
    in_tag = False
    for x in data:
        if in_tag:
            if x == ">":
                adding = True
                in_tag = False
        else:
            if x == "<":
                if word_add != "":
                    words.add(word_add.upper())
                in_tag = True
                word_add = ""
                adding = False
            elif x == " " or x == "\n":
                if word_add != "":
                    words.add(word_add.upper())
                word_add = ""
            elif x in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-":
                word_add = word_add + x


    # Any matches between target list and bag of words?
    for x in names:
        y = x.split()
        full_name = True
        hit = False
        for z in y:
            if z in words:
                hit = True
            else:
                full_name = False
        if full_name:
            print("!!!!",x," was found on page:", my_url)
            add_to_results(x,my_url)
        # elif hit:
        #    print(x," had a partial match on page:", my_url)

    # All done with page, save it to history and get the next page and loop.
    add_to_hist(my_url)
    my_url = get_next_url()
