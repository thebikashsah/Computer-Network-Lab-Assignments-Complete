# sender.py – The following are the tasks performed in this Sender program :
# 1. The input file is read, which contains a sequence of 0 and 1(From input.txt)
# 2. The message sequence is divided into datawords on the basis of frame size(k) taken as
#    the input from the user.
# 3. According to the four schemes namely VRC, LRC, Checksum and CRC, redundant
#    bits/dataword are added along with the datawords to form codewords.
#    datawords + redundant bits = codewords
# 4. The datawords and codewords which are to be sent are displayed.
# 5. These encoded codewords are then sent to the receiver.

class sender:
    # Initialize the sender class
    def __init__(self,size):
        self.codeword = []
        self.frame_size = size
    
    # Generate the codeword from the dataword according to the scheme
    def createCodeword(self,filename,schemeType,poly=""):
        fileinput=open(filename,"r")
        dataword=fileinput.readline()
        fileinput.close()
        tempword=""
        if schemeType ==1:
            for i in range(len(dataword)):
                if(i!=0 and i%self.frame_size==0):
                    self.codeword.append(tempword)
                    tempword=""
                tempword+=dataword[i]
            self.codeword.append(tempword)
            self.OneDParityGenerator()
        elif schemeType ==2:
            for i in range(len(dataword)):
                if(i!=0 and i%self.frame_size==0):
                    self.codeword.append(tempword)
                    tempword=""
                tempword+=dataword[i]
            self.codeword.append(tempword)
            self.TwoDParityGenerator()
        elif schemeType ==3:
            # Checksum
            for i in range(len(dataword)):
                if(i!=0 and i%self.frame_size==0):
                    self.codeword.append(tempword)
                    tempword=""
                tempword+=dataword[i]
            self.codeword.append(tempword)
            
            checkSum=self.codeword[0]
            for i in range(1,len(self.codeword)):
                checkSum=self.addBinary(checkSum,self.codeword[i])
                while(len(checkSum)>self.frame_size):
                    a=checkSum[:len(checkSum)-self.frame_size]
                    b=checkSum[len(checkSum)-self.frame_size:]
                    checkSum=self.addBinary(a,b)
            # Compliment of the checksum
            finalCheckSum=""
            for j in range(len(checkSum)):
                if(checkSum[j]=='0'):
                    finalCheckSum+='1'
                else:
                    finalCheckSum+='0'
            self.codeword.append(finalCheckSum)
        elif schemeType ==4:
            
            for i in range(len(dataword)):
                if i>0 and i%self.frame_size==0:
                    tempword+='0'*(len(poly)-1)
                    remainder=self.divideBinary(tempword,poly)
                    remainder=remainder[len(remainder)-(len(poly)-1):]
                    tempword=tempword[:self.frame_size]
                    tempword+=remainder
                    self.codeword.append(tempword)
                    tempword=""
                tempword+=dataword[i]
            tempword+='0'*(len(poly)-1)
            remainder=self.divideBinary(tempword,poly)
            remainder=remainder[len(remainder)-(len(poly)-1):]
            tempword=tempword[:self.frame_size]
            tempword+=remainder
            self.codeword.append(tempword)
            
            
            
            
    def OneDParityGenerator(self):
        for i in range(len(self.codeword)):
            countOnes=0
            for j in range(len(self.codeword[i])):
                if(self.codeword[i][j]=='1'):
                    countOnes+=1
            if(countOnes%2==0):
                self.codeword[i]+='0'
            else:
               self.codeword[i]+='1'

                
                
    def TwoDParityGenerator(self):
        
        parity=""
        index=0
        while index<self.frame_size:
            countOnes=0
            codeWordIndex=0;
            while codeWordIndex<len(self.codeword):
                if(self.codeword[codeWordIndex][index]=='1'):
                    countOnes+=1
                codeWordIndex+=1
            if(countOnes%2==0):
                parity+='0'
            else:
                parity+='1'
            index+=1
        self.codeword.append(parity)
    # Add the two binary numbers of the same length
    def addBinary(self,a,b):
        result=""
        a=a[::-1]
        b=b[::-1]
        carry=0
        
        for i in range(len(a)):
            DigitA=ord(a[i])-ord('0')
            DigitB=ord(b[i])-ord('0')
            total=DigitA+DigitB+carry
            
            char=str(total%2)
            result=char+result
            carry=total//2
        
        if carry==1:
            result='1'+result
        return result
    
    def xor(self, a, b):
        result = ""
        for i in range(1, len(b)):
            if a[i]==b[i]:
                result += '0'
            else:
                result += '1'
        return result

	#Helper function to divide two binary sequence
    def divideBinary(self, dividend, divisor):
        xorlen = len(divisor)
        temp = dividend[:xorlen]
        while len(dividend) > xorlen:
            if temp[0]=='1':
                temp=self.xor(divisor,temp)+dividend[xorlen]
            else:
                temp=self.xor('0'*xorlen,temp)+dividend[xorlen]
            xorlen += 1
        if temp[0]=='1':
            temp=self.xor(divisor,temp)
        else:
            temp=self.xor('0'*xorlen,temp)
        return temp
        
    def Display(self,schemeType):
        dataword=[]
        if schemeType ==1:
            print("VRC Scheme")
            print("Dataword : ",end="")
            for i in self.codeword:
                dataword.append(i[:self.frame_size])
            
            
            print(dataword)
            print("Codeword : ",end="")
            print(self.codeword)
        elif schemeType ==2:
            parity=self.codeword[len(self.codeword)-1]
            print("LRC Scheme")
            print("Dataword : ",end="")
            for i in range(len(self.codeword)-1):
                dataword.append(self.codeword[i])
            print(dataword)
            print("Codeword : ",end="")
            print(self.codeword)
            print("Parity : ",end="")
            print(parity)
        elif schemeType ==3:
            checkSum=self.codeword[len(self.codeword)-1]
            # push all elements except the checksum
            for i in range(len(self.codeword)-1):
                dataword.append(self.codeword[i])
            print("Checksum Scheme")
            print("Dataword : ",end="")
            print(dataword)
            print("Codeword : ",end="")
            print(self.codeword)
            print("Checksum : ",end="")
            print(checkSum)
        elif schemeType ==4:
            print("CRC Scheme")
            print("Dataword : ",end="")
            for i in range(len(self.codeword)):
                dataword.append(self.codeword[i])
            print(dataword)
            print("Codeword : ",end="")
            print(self.codeword)

            
            

            
            
        
            
