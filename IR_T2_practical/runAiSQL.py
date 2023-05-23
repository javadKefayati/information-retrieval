
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

mycursor = mydb.cursor()

# delete messenger database
mycursor.execute("show databases")
myresult = mycursor.fetchall()
for i in range(0, len(myresult)):
    if (myresult[i][0] == "messenger"):
        mycursor.execute("drop DATABASE ai")
        break

# create messenger database
mycursor.execute("create DATABASE ai")
mycursor.execute("use ai")
mycursor.execute("CREATE TABLE `order` (`id` varchar(100) NOT NULL,`item` varchar(200) NOT NULL,`value` varchar(200) NOT NULL,`status` int(11) NOT NULL)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
mycursor.execute("CREATE TABLE `user` (`id_order` int(20) NOT NULL,`id` varchar(200) NOT NULL,`name` varchar(200) NOT NULL,`userName` varchar(200) NOT NULL,`flag` int(10) NOT NULL,`temp` varchar(100) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")