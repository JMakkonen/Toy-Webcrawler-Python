# Toy-Webcrawler-Python
A toy Web Crawler written in Python

This is not intended to be used as such, since it is buggy, slow, has bad heuristics, does not consider robot.txt files, etc.
But!  it does actually work and provided me with some insight into what kinds of things you have to deal with for creating an 
industrial grade web-crawler.

The program seems to read and process about 1 site per second.  As the history files get bigger, that starts to slow down
finding the next site to crawl.

The crawl queue explodes pretty quick.  Not through too many websites in history, and the queue file was 10-12 MB.
