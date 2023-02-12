import threading
import time

frameTime = 3
interFrameTime = 1

numFrames = 2
totalFrames = 0


# function to determine channel utilization of 1p CSMA
# Channel utilization is the percentage of time that the channel is busy (i.e. the percentage of time that the channel is not idle)
def utility(lock, total): # It is the fraction of time used to transmit data packets.
    global totalFrames
    tot = 0
    used = 0
    while totalFrames < total:
        if lock.locked():
            used += 1
        tot += 1
    channelUtil = used / tot
    # Channel Utilization to 2 decimal places
    print("---------------------------------------------------")
    print("Channel Utilization: " + str(round(channelUtil, 4)))
    print("---------------------------------------------------")

    print()


# CSMA class using threading
class CSMA(threading.Thread):
    def __init__(self, lock, k, index): # initialize class with lock, k, and index values
        super().__init__()
        self.lock = lock
        self.k = k
        self.index = index

    def run(self):
        cnt = 1
        global numFrames
        global totalFrames
        while cnt <= numFrames:
            print("---------------------------------------------------")
            print("Thread " + str(self.index) + " is trying to acquire lock")
            print(f"Attempting to send frame {cnt} of node {self.index}")
            print()

            while self.lock.locked():
                pass

            self.lock.acquire()
            time.sleep(frameTime)
            print(f"Successfully sent frame {cnt} of node {self.index}")
            print()
            self.lock.release()
            totalFrames += 1
            time.sleep(interFrameTime)
            cnt += 1
        return


if __name__ == '__main__':
    numberNodes = int(input("Enter number of nodes: ")) # Take number of nodes as input
    
    lock = threading.Lock() # Create lock object which will be used by all threads
    met = threading.Thread(target=utility, args=[lock, numberNodes * numFrames]) # Create thread to calculate channel utilization

    Nodes = [CSMA(lock, 4, i + 1) for i in range(0, numberNodes)] # Create list of threads for each node in the network
    met.start() # Start thread to calculate channel utilization
    for node in Nodes: # Start all threads
        node.start()

    for node in Nodes: # Wait for all threads to finish
        node.join()
    met.join() # Wait for channel utilization thread to finish