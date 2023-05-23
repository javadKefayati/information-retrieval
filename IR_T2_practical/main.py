import telebot 
import logging
import json
import re
import sys
from db import db
from Response import Response

def logFile():
    logging.basicConfig(filename='./info.log', encoding='utf-8', level=logging.INFO)

logFile()


def listener(messages):
    
    """
    When new messages arrive TeleBot will call this function.
    This func give query from telegram bot and response them.
    """
    for m in messages:
        chatid = m.chat.id #give user id for resend message 

        if m.content_type == 'text' and m.text!="/help" and m.text !="/start" and m.text !="/items" and m.text!="/allOrder": #check format message has text and doesn'dataBase has /help or /start 
            
            text = m.text
            username = str(m.chat.username)
            first_name = str(m.chat.first_name)
            last_name = str(m.chat.last_name)
            dataBase= db()
            dataBase.addUserIfNotExist(chatid,first_name,username)
            r = Response()
            print(text)            
            logging.info('ci='+str(chatid)+"-un ="+username+"-fn:"+first_name+"-ln:"+last_name+"-dataBase="+text)
            response, group, nearQ, err = r.getResponse(str(text.strip()))
            
            if text=="فاکتور":
                      tempOrder= dataBase.getTempOrder(chatid)
                      
                      if tempOrder != None:
                                bot.send_message(chatid, tempOrder)
                      else:
                                bot.send_message(chatid, "سفارشی ندارید" )
                                
            elif text=="سفارش ها" or text=="سفارشها":
                    allOrder=dataBase.allOrder(chatid)
                    
                    if allOrder != None:
                              bot.send_message(chatid, allOrder)
                    else:
                              bot.send_message(chatid, "سفارشی ندارید" )
                    
            elif text =="*بله":
                      dataBase.acceptAllOrder(chatid)
                      bot.send_message(chatid, "عملیات با موفقیت انجام شد" )
            elif text =="*خیر":
                      bot.send_message(chatid, "ادامه بدهید به سفارش" )
            else :
                if err ==1 and dataBase.getFlag(chatid)==0:
                          bot.send_message(chatid, "توان فهم ورودی شما را ندارم\nلطفا واضح تر بیان کنید")

                #normal status
                if group != "Shop" and err == 0 and dataBase.getFlag(chatid) == 0:
                          bot.send_message(chatid, response)

                if group == "Shop" and err == 0 and dataBase.getFlag(chatid) == 0 :
                          dataBase.changeFlagUser(chatid,1)
                          dataBase.setTempItem(chatid ,nearQ)
                          bot.send_message(chatid, response)

                elif   dataBase.getFlag(chatid) == 1:
                          isNumber = re.search("\d+", text)

                          if isNumber==None:
                                    bot.send_message(chatid, " لطفا مقدار را با واحد کیلو وارد کنید ")
                          else :
                            dataBase.changeFlagUser(chatid,0)
                            number = isNumber   
                            tempIndex = dataBase.getTempIndexFromUser(str(chatid))
                            dataBase.setOrder(chatid, tempIndex, number.group(), 0)
                            
                            bot.send_message(chatid, "بسیار خب سفارشتان ثبت شد ، برای نمایش لیست خرید فاکتور را تایپ کنید")


#api key for connect to telegram bot
TOKEN = "5331090152:AAHfzMVzZuiJQq9ChEsQ9ttc0pkkRfH9zXU"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands =["start"])
def start(message):
      bot.send_message(message.chat.id,"سلام  \n اگه میخوای بدونی چه میکنم \items را تایپ کنید")

@bot.message_handler(commands =["help"])
def help(message):
      bot.reply_to(message,"شما میتوانید با بات صحبت کنید\n اگر سفارشی دارید از /items یک محصول را انتخاب و\n به بات اطلاع بدهید\nبعد از آن مقدار را اطلاع دهید\n برای دیدن سفارش های در سبد، 'فاکتور' را تایپ کنید\n برای دیدن تاریخچه تمامی سفارشات ، 'سفارش ها' را تایپ کنید")
      
@bot.message_handler(commands =["items"])
def items(message):
      bot.reply_to(message,"سیب - انار -گلابی- بستنی- شیر - موز")
      

bot.set_update_listener(listener) #register listener
#Use none_stop flag let polling will not stop when get new message occur error.
# Interval setup. Sleep 3 secs between request new message.
bot.polling(interval=3)

while True: # Don'dataBase let the main Thread end.
    pass