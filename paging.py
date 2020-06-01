# Yashkir Ramsamy
# Assignment 3
# CSC3002F

import sys
import random
from collections import deque
import queue
from functools import lru_cache


def main():
    size = int(sys.argv[1])
    numPage = int(sys.argv[2])
    pages = processSequence(numPage)
    print("Number of Pages:", numPage)
    print("Page-reference string:", pages)
    print("Frame Size:", size)
    print("==========RESULTS==========")
    print('FIFO', FIFO(size, pages), 'Page Faults.')
    print('LRU', LRU(size, pages), 'Page Faults.')
    print('OPT', OPT(size, pages), 'Page Faults.')


def FIFO(size, pages):
    frameSize = size
    pagesSeq = pages
    memoryQueue = queue.Queue(frameSize)
    fault = 0;
    for page in pagesSeq:
        if page not in deque(memoryQueue.queue) and not memoryQueue.full():
            memoryQueue.put(page)
            fault += 1
        elif page in deque(memoryQueue.queue):
            pass
        elif page not in deque(memoryQueue.queue) and memoryQueue.qsize():
            fault += 1
            memoryQueue.get()
            memoryQueue.put(page)

    return fault


def LRU(size, pages):
    pageSeq = pages

    @lru_cache(size)
    def lruOperations(page):
        return page

    for page in pageSeq:
        lruOperations(page)
        cacheTable = lruOperations.cache_info()
    return cacheTable[1]



def OPT(size, pages):
    frameSize = size
    pagesSeq = pages
    memoryQueue = deque([])
    fault = 0
    i=0
    for page in pagesSeq:
        if page not in memoryQueue and len(memoryQueue)<frameSize: # memory empty or has empty slots
            memoryQueue.append(page)
            fault += 1
        elif page in memoryQueue: # page in memory
            pass
        elif page not in memoryQueue and len(memoryQueue) == frameSize: # memory full and page replacement occurs
            fault += 1
            listMem = list(memoryQueue)
            maxVal = 0
            for item in listMem:
                distance = pagesSeq.find(item,i)
                if distance == -1:
                    distance = len(pagesSeq)*1000
                if maxVal < distance:
                    maxVal = distance
                    itemTR = item
            memoryQueue.remove(itemTR)
            memoryQueue.append(page)
        i+=1

    return fault

def processSequence(numPages):
    #TODO Fix numpages, numpages * c =/= character length
    return str(random.randint(0, numPages * 10000000000000000000000000000000000000000000000000000000000000000))[0:numPages + 1]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python paging.py [Frame Size] [Length of Reference String]")
    else:
        main()
