# Yashkir Ramsamy
# Assignment 3
# CSC3002F
# FIFO, LRU, OPT Page Replacement Algorithms
# Usage: python paging.py [Number of Frames] [Number of Pages]
# Usage example: python3 paging.py 5 64

import queue
import random
import sys
from collections import deque
from functools import lru_cache


def main():
    '''Runs page replacement algorithms'''
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
    ''' FIFO Page Replacement algorithm'''
    frameSize = size
    pagesSeq = pages
    memoryQueue = queue.Queue(frameSize)
    fault = 0;
    for page in pagesSeq:  # Iterate through pages in sequence
        if page not in deque(memoryQueue.queue) and not memoryQueue.full():  # memory empty or has empty slots
            memoryQueue.put(page)
            fault += 1
        elif page in deque(memoryQueue.queue):  # page exists in memory
            pass
        elif page not in deque(memoryQueue.queue) and memoryQueue.qsize():  # memory full and page replacement occurs
            fault += 1
            memoryQueue.get()  # pop page from queue
            memoryQueue.put(page)  # insert page into queue

    return fault


def LRU(size, pages):
    ''' LRU Page Replacement algorithm'''
    pageSeq = pages

    @lru_cache(size)  # Set the size of the LRU cache structure
    def lruOperations(page):  # Insert page into LRU Cache
        return page

    for page in pageSeq:  # For every page in sequence, insert into cache structure
        lruOperations(page)
        cacheTable = lruOperations.cache_info()  # Calculate and display information about cache structure
    return cacheTable[1]  # Select faults from cache structure


def OPT(size, pages):
    '''OPT Page Replacement algorithm'''
    frameSize = size
    pagesSeq = pages
    memoryQueue = deque([])
    fault = 0
    i = 0
    for page in pagesSeq:  # Iterate through pages in sequence
        if page not in memoryQueue and len(memoryQueue) < frameSize:  # memory empty or has empty slots
            memoryQueue.append(page)
            fault += 1
        elif page in memoryQueue:  # page in memory
            pass
        elif page not in memoryQueue and len(memoryQueue) == frameSize:  # memory full and page replacement occurs
            fault += 1
            listMem = list(memoryQueue)  # Converts queue into workable list
            maxVal = 0
            for item in listMem:  # Iterate through options for replacement
                distance = pagesSeq.find(item, i)
                if distance == -1:
                    distance = len(pagesSeq) * 1000
                if maxVal < distance:
                    maxVal = distance
                    itemTR = item
            memoryQueue.remove(itemTR)
            memoryQueue.append(page)
        i += 1

    return fault


def processSequence(numPages):
    ''' Generates random page sequence reference string'''
    return str(random.randint(10 ** (numPages - 1), (10 ** numPages) - 1))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python paging.py [Number of Frames] [Number of Pages]")  # Usage example python paging.py 5 64
    else:
        main()
