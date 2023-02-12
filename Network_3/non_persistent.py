import threading
import random
import time

frameTime = 3
interFrameTime = 1
numFrames = 2
totalFrames = 0


def metrics(lock, total):
    global totalFrames
    tot = 0
    used = 0
    while totalFrames < total:
        if lock.locked():
            used += 1
        tot += 1
    print("---------------------------------------------------")
    # Channel Utilization to 4 decimal places
    print("Channel Utilization: " + str(round(used / tot, 4)))



class CSMA(threading.Thread):
    def __init__(self, lock, index):
        super().__init__()
        self.lock = lock
        self.index = index

    def run(self):
        global numFrames
        global totalFrames

        cnt = 1
        while cnt <= numFrames:
            print("---------------------------------------------------")
            print(f"Attempting to send frame {cnt} of node {self.index}")
            print("---------------------------------------------------")
            # print()

            while self.lock.locked():
                backOffTime = random.randint(2, 5)
                print("---------------------------------------------------")
                print(f"Node {self.index} waiting for time : {backOffTime}")
                print("---------------------------------------------------")
                # print()
                time.sleep(backOffTime)

            self.lock.acquire()
            time.sleep(frameTime)
            print("---------------------------------------------------")
            print(f"Successfully sent frame {cnt} of node {self.index}")
            print("---------------------------------------------------")
            # print()
            self.lock.release()
            totalFrames += 1
            time.sleep(interFrameTime)

            cnt += 1
        return


if __name__ == '__main__':
    numberNodes = int(input("Enter number of nodes: "))
    lock = threading.Lock()
    met = threading.Thread(target=metrics, args=[lock, numberNodes * numFrames])

    Nodes = [CSMA(lock, i + 1) for i in range(0, numberNodes)]
    met.start()
    for node in Nodes:
        node.start()

    for node in Nodes:
        node.join()
    met.join()