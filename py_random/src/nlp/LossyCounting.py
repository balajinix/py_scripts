'''
Created on Nov 18, 2014

@author: gbalaji
'''

#!/usr/bin/python

import csv
import heapq

# http://www.americanscientist.org/issues/pub/the-britney-spears-problem

# global values
container_hash = {}
m = 500
debug = False

# load current values
def load_containers(filename):
    global container_hash
    try:        
        # open file
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter='|')
            for term, count in reader:
                if term in container_hash:
                    print "Error: container already has term: ", term
                else:
                    container_hash[term] = int(count)
    except:
        print "file ERROR: " + filename

# takes a term, checks if its in hash, else finds a place for it
def update(term, count):
    global m
    global container_hash
    global debug
    # if term is already in hash, we are done
    if term in container_hash:
        if debug:
            print term, " present in hash"
        container_hash[term] += 1
        return

    # if hash is not yet full, then insert the new term and done
    if len(container_hash) < m:
        if debug:
            print "hash has space for ", term
        container_hash[term] = 1
        return

    # see if there is any replacable term in the hash
    for k, v in container_hash.items():
        if v <= 0:
            if debug:
                print "replacing ", k, " with ", term
            del container_hash[k]
            container_hash[term] = 1
            return

    if debug:
        print "decrementing count for all entries"
    # decrement every item
    for k, v in container_hash.items():
        container_hash[k] -= 1

    return

# returns top k items as a list
def get_trends(k):
    global container_hash
    global m
    if k > m:
        k = m
    h = []
    for key, value in container_hash.items():
        heapq.heappush(h, (value, key))
    # trends will get an array
    trends = heapq.nlargest(k,h)
    return trends

def store(filename):
    global container_hash
    f = open(filename, 'w')
    for term, count in container_hash.items():
        line = term + '|' + str(count) + '\n'
        f.write(line)
    f.close()
        
def init_test(_m):
    global m
    m = _m

import sys

def main():
    print "Enter m"
    line = sys.stdin.readline()
    m = int(line.strip())
    init_test(m)
    for line in iter(sys.stdin.readline, ""): 
        line = line.strip()
        if (line == "exit"):
            break
        if (line == "print"):
            get_trends(5)
            continue
        update(line, 1)
    store('hotspots.txt')

if __name__ == '__main__':
        main()
