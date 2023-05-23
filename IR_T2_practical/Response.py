from Similarities import Similarities
import random
import json
import  sys


class Response:
      questionData = {}
      answerData = {}
      listOfData = []
      
      def __init__(self):
            
            with open("question.json", "r") as file:
                dataQ = json.load(file)

            with open("answer.json", "r") as file:
                dataA = json.load(file)
                
            self.questionData = dataQ
            self.answerData = dataA
            self.createListOfDataWithoutKey()
            
            
      def createListOfDataWithoutKey(self):
            for d in self.questionData:
                  self.listOfData+=self.questionData[d]
            return self.listOfData
      
      def checkGroup(self, query):
            
            sim = Similarities()
            sim.initClass(self.listOfData)
            if sim.setQuery(query) == 0:
                  return "","", 1
            else:
                  namSimilarities , valueSimilarities = sim.result()
                  
                  
                  for d in self.questionData:
                        nL = self.questionData[d]
                        for n in nL:
                            if n == namSimilarities:

                              
                                return d, n,0

      def getResponse(self,query):
            group,nearQ ,error = self.checkGroup(query)
 
            if error==1:
                  return "","","", 1  
            else :
                  for a in self.answerData:
                        
                        if a == group:
                              nList = self.answerData[a]
                              randIndex = random.randint(0, len(nList)-1)
                              # print("nl="+nList[randIndex]+"---"+group+"--"+nearQ)
                              return nList[randIndex], group,nearQ, 0

                  
            
      
                  
                  





