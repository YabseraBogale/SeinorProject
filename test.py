from datetime import datetime
from Database.database import Database
from Database.addischeretauser import AddisCheretaUser
from Database.verfication import Verfication
from Database.item import Item
from Database.rating import Rating
from Database.buyer import Buyer
import bcrypt

print(Database().AllowedFile("filename.png"))
print(Database().AllowedFile("filename.jpg"))
print(Database().AllowedFile("filename.jpeg"))
print(Database().AllowedFile("filename.txt"))
print(AddisCheretaUser().ResetPassWordForUser('getahunababu@gmail.com','654321'))
print(type(Verfication().GetEmailForVerfication('getahunababu@gmail.com')[0]))
pas=AddisCheretaUser().GetAddisCheretaUserData('getahunababu@gmail.com')
result=bcrypt.checkpw("1234567890".encode('utf-8'),pas)
print(pas)
print(type(pas)==type([]))
print(result!=[])
print(AddisCheretaUser().GetAllCheretaUserEmail()!=False)
print(AddisCheretaUser().GetCheretaUserDataJson()!=False)
print(Item().InsertItemTable(2,"Yabsera","Yabsera","Yabsera","Yabsera",1,"2024-12-25")==True)
print(type(list(Item().GetItemWithIID((str(758424)))))==type([]))
print(Item().GetAllItemLimit()!=False)
print(Item().Search(Price="",Name="",Category="Art"))
print(Buyer().InsertBuyerTable(1,'758424','2024-12-20',600))
print(Item().GetItemWithIID('758424'))
print(Buyer().HighestBid(316197))
print(Item().ListOfAuction()[0])
print(Buyer().GetUserBidWithUserId("2"))
lst=[]
for i in Item().UserItemDashboardWithUID("1"):
    if Buyer().HighestBid(i[5])==None:
        print(list(i)+[0])
    else:
        print(list(i)+[Buyer().HighestBid(i[5])])
print(Buyer().HighestBidWinnerWithId('758424'))
print(AddisCheretaUser().GetPhonenumberEmailWithUID(Item().GetItemWithIID('381383')[1]))
print(AddisCheretaUser().GetPhonenumberEmailWithUID(Buyer().HighestBidWinnerWithId('758424')[1]))
print("Rating Count Of Rating Of User",Rating().CountOfRatingOfUser(2))
print("Rating Sum Rating Of User",Rating().SumRatingOfUser(2))
print("Rating Min Rating Of User",Rating().MinRatingOfUser(2))
print("Rating Average Rating Of User",Rating().AverageRatingOfUser(2))
print("Rating Bayesian Rating Of User",Rating().BayesianRatingOfUser(2))
print(AddisCheretaUser().GetPhotoWithUID(1))