
class receiver:
    def __init__ (self,s):
        self.codeword=s.codeword
        self.frame_size=s.frame_size
        
        
    def checkError(self,schemeType,poly=""):
        if schemeType ==1:
            self.OneDParityCheck()
        elif schemeType ==2:
            self.TwoDParityCheck()
        elif schemeType ==3:
            self.checksumCheck()
        elif schemeType ==4:
            self.checkCRCError(poly)
        else:
            print("Invalid Scheme")
    
    def checkCRCError(self,poly):
        for i in range(len(self.codeword)):
            remainder = self.divideBinary(self.codeword[i], poly)
            error = False
            for j in range(len(remainder)):
                if remainder[j] == '1':
                    error = True
            print("Remainder:",remainder,end=' ')
            if error:
                print("ERROR DETECTED")
            else:
                print("NO ERROR DETECTED")
            # exit the loop if error is detected
        
        
        
    def OneDParityCheck(self):
        
        flag=True
        for i in range(len(self.codeword)):
            countOnes=0
            for j in range(len(self.codeword[i])):
                if(self.codeword[i][j]=='1'):
                    countOnes+=1
            if(countOnes%2!=0):
                print("ERROR is detected by VRC")
                flag=False
                break
        if flag==True:
            print("No Error is detected by VRC")
        
        
            
    def TwoDParityCheck(self):
        parity=""
        index=0
        while index<self.frame_size:
            countOnes=0
            codeWordIndex=0;
            while codeWordIndex<len(self.codeword)-1:
                if(self.codeword[codeWordIndex][index]=='1'):
                    countOnes+=1
                codeWordIndex+=1
            if(countOnes%2==0):
                parity+='0'
            else:
                parity+='1'
            index+=1
        if(parity==self.codeword[len(self.codeword)-1]):
            print("No Error is detected by LRC")
        else:
            print("ERROR is detected by LRC")
        return parity
            
    def checksumCheck(self):
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
        #convert the finalCheckSum to int 
        val=int(finalCheckSum,2)
        if(val==0):
            print("No Error is detected by Checksum")
        else:
            print("ERROR is detected by Checksum")
    def addBinary(self,a,b):
        result=""
        a=a[::-1]
        b=b[::-1]
        carry=0
        
        for i in range(max(len(a),len(b))):
            DigitA=ord(a[i])-ord('0') if i<len(a) else 0
            DigitB=ord(b[i])-ord('0') if i<len(b) else 0
            total=DigitA+DigitB+carry
            
            char=str(total%2)
            result=char+result
            carry=total//2
        
        if carry==1:
            result='1'+result
        return result
    def Display(self,schemeType):
        # display the codeword
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
            parity=""
            index=0
            while index<self.frame_size:
                countOnes=0
                codeWordIndex=0;
                while codeWordIndex<len(self.codeword)-1:
                    if(self.codeword[codeWordIndex][index]=='1'):
                        countOnes+=1
                    codeWordIndex+=1
                if(countOnes%2==0):
                    parity+='0'
                else:
                    parity+='1'
                index+=1
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
    def xor(self, a, b):
        result = ""
        for i in range(1, len(b)):
            if a[i]==b[i]:
                result += '0'
            else:
                result += '1'
        return result

        

            



        