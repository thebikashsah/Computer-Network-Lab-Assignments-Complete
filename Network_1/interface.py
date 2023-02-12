from senders import *
from receiver import *
import random
import sys

#function to inject errors in random positions
def injectRandomError(frames):
	for i in range(len(frames)):
		pos = random.randint(0, len(frames[i])-1)
		frames[i] = frames[i][:pos]+'1'+frames[i][pos+1:]
	return frames

def injectSpecificError(frames, zeropos, onepos):
	for i in range(len(zeropos)):
		for j in range(len(zeropos[i])):
			pos = zeropos[i][j]
			frames[i] = frames[i][:pos]+'0'+frames[i][pos+1:]
	for i in range(len(onepos)):
		for j in range(len(onepos[i])):
			pos = onepos[i][j]
			frames[i] = frames[i][:pos]+'1'+frames[i][pos+1:]
	return frames


def case1(filename,size):
    # changing 1 bit in the codeword
    print("CASE 1:")
    print(" VRC ")
    type=1
    s=sender(size)
    s.createCodeword(filename,type)
    s.Display(type)
    s.codeword=injectRandomError(s.codeword)
    r=receiver(s)
    r.checkError(type)
    r.Display(type)
    
    print(" LRC ")
    type=2
    s=sender(size)
    s.createCodeword(filename,type)
    s.Display(type)
    s.codeword=injectRandomError(s.codeword)
    r=receiver(s)
    r.checkError(type)
    r.Display(type)
    
    print("CheckSum")
    type=3
    s=sender(size)
    s.createCodeword(filename,type)
    s.Display(type)
    s.codeword=injectRandomError(s.codeword)
    r=receiver(s)
    r.checkError(type)
    r.Display(type)
    
    print("CRC")
    poly="1001"
    type=4
    s=sender(size)
    s.createCodeword(filename,type,poly)
    s.Display(type)
    s.codeword=injectRandomError(s.codeword)
    r=receiver(s)
    r.checkError(type,poly)
    r.Display(type)
    
def case2(filename,size):
    print("Case 2")
    print("CheckSum")
    type=3
    
    zeropostion=[]
    oneposition=[[5]]
    s=sender(size)
    s.createCodeword(filename,type)
    s.Display(type)
    s.codeword=injectSpecificError(s.codeword,zeropostion,oneposition)
    r=receiver(s)
    r.checkError(type)
    r.Display(type)
    
    print("CRC")
    poly="100"
    type=4
    s=sender(size)
    s.createCodeword(filename,type,poly)
    s.Display(type)
    s.codeword=injectSpecificError(s.codeword,zeropostion,oneposition)
    r=receiver(s)
    r.checkError(type,poly)
    r.Display(type)
    
def case3(filename,size):
	print("Case 3")
	print("VRC")
	type=1
    
	zeropostion=[]
	oneposition=[[5]]
	s=sender(size)
	s.createCodeword(filename,type)
	s.Display(type)
	s.codeword=injectSpecificError(s.codeword,zeropostion,oneposition)
	r=receiver(s)
	r.checkError(type)
	r.Display(type)
    
	print("CRC")
	poly="100"
	type=4
	s=sender(size)
	s.createCodeword(filename,type,poly)
	s.Display(type)
	s.codeword=injectSpecificError(s.codeword,zeropostion,oneposition)
	r=receiver(s)
	r.checkError(type,poly)
	r.Display(type)

if __name__=='__main__':
    print("1. Error is Detected by All Schemes")
    print("2. Error is Detected by Checksum but not CRC ")
    print("3. Error is Detected by VRC but not by CRC")
    case=int(input())
    print("Enter file name ")
    filename=input()
    print("Enter size of frame")
    frameSize=int(input())
    
    if case==1:
        case1(filename,frameSize)
    elif case==2:
        case2(filename,frameSize)
    elif case==3:
        case3(filename,frameSize)
    