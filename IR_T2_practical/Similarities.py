import math
import sys

class Similarities:
      frequently_list = {}
      length_Doc = 0
      documentsList = {}
      documents = {}
      idf_list = {}
      query = ""
      distanceDoc = {}
      cosSimList = {}
      
      def initClass(self, listOfDoc):
            for doc in listOfDoc:
                  self.addDocument(doc)
                  
            self.createIdfList()
            self.createTfList()
            
      def addDocument(self , document):
            #create list of words 
            listOfDoc =  document.split(' ')
            listOfFrequency = {}
            
            for word in listOfDoc:
                  listOfFrequency[word] = listOfFrequency.get(word, 0)+1
                  self.frequently_list[word] = self.frequently_list.get(word, 0) + 1

            self.tf_list = listOfDoc
            
            #increase number of document        
            self.length_Doc = self.length_Doc + 1
            # add information to list     
            self.documentsList["d"+str (self.length_Doc)]= listOfFrequency
            self.documents["d"+str(self.length_Doc)] = document
            
      
      def createIdfList(self):
            for word in self.frequently_list:
                  repeat = self.numberRepeatInDocs(word)
                  self.idf_list[word] = math.log2(self.length_Doc/repeat)
      
      def createTfList(self):
            
            for key in self.documentsList:
                  words = self.documentsList[key]
                  for word in words:
                        words[word] = self.idf_list[word] * words[word]
                  
                  self.documentsList[key] = words      
            
            
          
      def numberRepeatInDocs(self ,word):
            number = 0
            for key in self.documentsList:
                  words = self.documentsList[key]
                  if word in words:
                        number = number + 1
            return number

      def setQueryDf(self):
            listOfWords = self.query.split(" ")
            frequentlyQuery = {}
            for word in listOfWords:
                        frequentlyQuery[word] = frequentlyQuery.get(word, 0)+1
            
            tempDic={}
            
            maxRepeat= max(frequentlyQuery.values())
            
            for key in self.frequently_list:
                  if key in frequentlyQuery:
                        if maxRepeat==0:
                              maxRepeat==0
                        tempDic[key] = self.idf_list[key] * (frequentlyQuery[key]/maxRepeat)
                        
            self.documentsList["q"] = tempDic
            
            

      def setDistance(self):
            
            for key in self.documentsList:
                  list_of_tf = self.documentsList[key]
                  sum = 0
                  for key_tf in list_of_tf:
                        sum = sum + float (list_of_tf[key_tf] ** 2)
                  
                  self.distanceDoc[key] = math.sqrt((sum))
            if self.distanceDoc["q"]==0:
                  return 0
            return 1
                  
      def setQuery(self,quey):
            self.query = quey
            self.setQueryDf()
            
            s = self.setDistance()
            if s==0:
                  return 0
            else:
                  self.cosSim()
            
            
            
      def cosSim(self):
            
            qTfList = self.documentsList["q"]

            listOfTf = self.documentsList
            listOfTf.pop("q")
            for key in self.documentsList:
                  sum = 0
                  list_of_tf = self.documentsList[key]
                  for word in list_of_tf:
                        if word in qTfList:
                              sum = sum +(qTfList[word] * list_of_tf[word])

                  sum = sum /(self.distanceDoc[key]*self.distanceDoc["q"])
                  self.cosSimList[key] = sum
                  sum =0
                  
      def MaxArr(self):
            max = 0
            maxIndex = ""
            for i in self.cosSimList:                  
                  valueL = float(self.cosSimList[i])
                  if float(valueL)> float(max):
                        max = valueL
                        maxIndex = i
            return maxIndex
      def result(self):
          maxDoc = self.MaxArr()
          
          return self.documents[maxDoc], float(self.cosSimList[maxDoc])
            
            

