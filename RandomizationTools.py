

# https://stackoverflow.com/questions/2140787/select-k-random-elements-from-a-list-whose-elements-have-weights
# testing out roulette wheel algorithm

from random import randint, choice, shuffle
import numpy as np

def TestRouletteWheeel():

    # generate elements
    NUM_ELEMENTS = 100
    ELEMENTS = [
        "STEVE-%d",
        "BOB-%d",
        "TED-%d",
        "MARY-%d"
    ]
    heap = []
    weight_sum = 0
    for index in xrange(NUM_ELEMENTS):
        heap.append(
            (randint(1,4), choice(ELEMENTS) % index)
        )
        weight_sum += heap[-1][0]

    # print heap
    def EmptyHeap(heap, initial_weight):
        weight = initial_weight
        index = -1
        while len(heap) > 0:
            interval = randint(0, weight)
            index = -1
            while interval > 0  and index < len(heap)-1:
                index += 1
                interval -= heap[index][0]
            value = heap.pop(index)
            weight -= value[0]
            print value
    EmptyHeap(heap, weight_sum)

    # now generate a bunch of random numbers without popping the heap (so just test the number of times a value gets pulled
    heap = [
        (4, "bob"),
        (2, "steve"),
        (1, "mary"),
        (1, "tom"),
    ]

    # generate a bunch of values
    results = np.zeros(4)
    weight = 8
    index = -1
    for index in xrange(10000):
        index, value = ValueFromHeap(heap, weight, pop=False)
        results[index] += 1

    print "results", results
    print "percentage", results / np.sum(results)


    # sort
    shuffle(heap)
    heap.sort(key=lambda x: x[0])
    heap.reverse()

    # print heap

def ValueFromHeap(heap, weight=None, pop=True):
    #roulette wheel algorithm
    if weight is None:
        weight = 0
        for item in heap:
            weight += item[0]

    # prepare the wheel
    shuffle(heap)
    heap.sort(key=lambda x: x[0])
    heap.reverse()

    interval = randint(0, weight -1)
    index = -1
    while interval > 0  and index < len(heap)-1:
        index += 1
        interval -= heap[index][0]

    value = heap[index]
    if pop:
        heap.pop(index)
        weight -= value[0]
    return index, value


if __name__ == "__main__":
    TestRouletteWheeel()
