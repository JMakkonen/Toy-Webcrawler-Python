#P1062:  Clean up crawl_queue file.
'''
To reduce the size of the crawl_queue, you can run this program which
deletes redundant links as well as anything that is in history already.
It does not overwrite the current queue.  User has to rename the outputted
file "cleaned_list.data".
'''
f = open("crawl_queue.data",mode = 'r', encoding = "utf-8")
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
f = open("crawl_hist.data",mode = 'r', encoding = "utf-8")
data_read = f.read()
data_list_read = []
my_url = ""
for x in data_read:
    if x == "\n":
        data_list_read.append(my_url)
        my_url = ""
    else:
        my_url += x
f.close()

stop_domains = ['google','facebook','pinterest','twitter','amazon',
                   'cialis','mailto','cafepress']

f = open("cleaned_list.data",mode = "w", encoding = "utf-8")

clean_list = []
for x in data_list:
    add_it = True
    for y in stop_domains:
        if (y in x):
            add_it = False
    if x in data_list_read:
        add_it = False
    if add_it:
        f.write(x+"\n")
f.close()
