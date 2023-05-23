import json
import mysql.connector
from soupsieve import select
import sys
import re

class db:
      mydb = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="", 
                  database="ai"
                        )
      items = ["سیب" , "انار" ,"گلابی","بستنی", "شیر","موز"]       
       
      def getInfo(self,tableName,selector =" ",where=""):
            mycursor = self.mydb.cursor()
            sql = ""
            if where=="":
                  sql += "SELECT "+selector+" FROM "+tableName+" ;"
                 
            else:
                  sql += "SELECT "+selector+" FROM "+tableName+" WHERE "+where +" ;"


            mycursor.execute(str(sql))
            myresult = mycursor.fetchall()
 
            return myresult
      
      def setInfo(self,tableName,columns=[],value=[]):
            col =""
            for v in range(0,len(value)):
                  
                  if len(value)-1 != v:
                        col +=" "+columns[v]+" , "
                  else :
                        col += ""+columns[v]+" "
            
            valStr =""
            for v in range(0,len(value)):
                  
                  if len(value)-1 != v:
                        valStr +=" %s , "
                  else :
                        valStr += " %s "
                  
            sql = "INSERT INTO "+tableName+" ( "+col+ ") VALUES ( "+valStr+" )"
            # print(sql)
            # print(value)

            mycursor = self.mydb.cursor()
            mycursor.execute(sql, value)
            self.mydb.commit()
      
      def edit(self, tableName , data= "", where=""  ):
            
            mycursor = self.mydb.cursor()

            sql = "UPDATE "+tableName+"  SET "+data+" WHERE "+where

            mycursor.execute(sql)

            self.mydb.commit()
      
      def changeFlagUser(self,chatId,number):
            self.edit("user","flag="+str(number),"id="+str(chatId))
      
      def addUserIfNotExist(self,chatId,name,userName):
            user = self.getInfo("user","id","id="+str(chatId))
            if user==[]:
                  self.setInfo("user",["id","name","userName","flag"],[str(chatId),str(name),str(userName),str(0)])

      def getFlag(self,chatId):
            return self.getInfo("user","flag","id="+str(chatId))[0][0]
      
      def checkItem(self , query):
            for i in self.items:
                  item = re.search(str(i), query)
                  if item != None:
                        return i
            return ""
      
      def setTempItem(self,chatid,response):
            # print("res"+response)
            item = self.checkItem(response)
            # print("item -"+item)
            self.edit("user","temp='"+item+"'","id="+str(chatid))
                        
                  
      def setOrder(self,chatid,itemName,value,status):
            self.setInfo("`order`",["id","item","value","status"],[str(chatid),str(itemName),str(value),status])
      
      def getTempIndexFromUser(self,chatid):
           return self.getInfo("user","temp","id="+str(chatid))[0][0]
            
      def getTempOrder(self,chatid):
            items =self.getInfo("`order`"," item , value ", "status=0 and id="+str(chatid))
            
            orders = ""
            for item in items:
                  orders += "کالا : "+item[0]+"-- اندازه : "+item[1]+" کیلو\n"
            if orders != "":
                  return orders+"\n اگر تمایل به اتمام سفارشات دارید لطفا *بله و اگر خیر ، *خیر را تایپ کنید"
            else :
                  orders +"هم اکنون سفارشی ندارید"
      
      def acceptAllOrder(self,chatid):
            self.edit("`order`","status=1"," status=0 and id = "+str(chatid) )
            

      def allOrder(self,chatid):
             items =self.getInfo("`order`"," item , value ", "status=1 and id = "+str(chatid))
             orders = ""
             for item in items:
                  orders += "کالا : "+item[0]+"-- اندازه : "+item[1]+" کیلو\n"
             if orders != "":
                  return orders
             else :
                  orders +"هم اکنون سفارشی ندارید"
       
      # def __del__(self):
            
      #       print('Destructor called, connection closed.')
            

# t =db()
# print(t.getTempOrder("950641524"))
# print(t.setTempItem("23","بستنی میخواهم"))
# t.setOrder("23","holo","2",1)
# t.getTempIndexFromUser("10")
# id =t.getInfo("user",selector="id",where="id=1")
# t.setInfo("user",["id","name","userName","flag"],["2","ali","afds3",1])
# t.edit("user","id=10","id=1")
# t.changeFlagUser("10",0)
# t.addUserIfNotExist("27","java","javadkdf")
# print(t.getFlag("2"))
