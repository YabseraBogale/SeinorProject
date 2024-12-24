from datetime import datetime
from Database.database import Database
from Database.addischeretauser import AddisCheretaUser
from Database.verfication import Verfication
from Database.item import Item
from Database.buyer import Buyer
import bcrypt

# print(Database().AllowedFile("filename.png"))
# print(Database().AllowedFile("filename.jpg"))
# print(Database().AllowedFile("filename.jpeg"))
# print(Database().AllowedFile("filename.txt"))
# print(AddisCheretaUser().ResetPassWordForUser('getahunababu@gmail.com','654321'))
# print(type(Verfication().GetEmailForVerfication('getahunababu@gmail.com')[0]))

# pas=AddisCheretaUser().GetAddisCheretaUserData('getahunababu@gmail.com')
# result=bcrypt.checkpw("1234567890".encode('utf-8'),pas)
# print(pas)
# print(type(pas)==type([]))
# print(result!=[])
# print(AddisCheretaUser().GetAllCheretaUserEmail()!=False)

# print(AddisCheretaUser().GetCheretaUserDataJson()!=False)

# print(Item().InsertItemTable(2,"Yabsera","Yabsera","Yabsera","Yabsera",1,"2024-12-25")==True)
# print(type(list(Item().GetItemWithIID((str(758424)))))==type([]))

# print(Item().GetAllItemLimit()!=False)

# print(Item().Search(Price="Low",Category="Art",Name="")!=False)

# print(Buyer().InsertBuyerTable(1,'758424','2024-12-20',600))
# print(Item().GetItemWithIID('758424'))

# print(Buyer().HighestBid(316197))