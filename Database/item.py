import sqlite3
import random
import string
from datetime import datetime

class Item():
    def __init__(self) -> None:
        self.connection=sqlite3.Connection("addischereta.db",check_same_thread=False)
        self.pointer=self.connection.cursor()

    def InsertItemTable(self,UID,Name,Description,Photo,Category,StartingPrice,EndDate):
        try:
            Status="selling"
            statment="Insert into Item(IID,UID,Name,Description,DateStored,status,Photo,Category,StartingPrice) values(?,?,?,?,?,?,?,?,?)"
            IID=int(''.join(random.choices(string.digits, k=6)))
            dateStored=EndDate
            self.pointer.execute(statment,(IID,int(UID),Name,Description,dateStored,Status,Photo,Category,StartingPrice))
            self.connection.commit()
            return True
        except Exception as e:
            return False
        
    def GetAllItemLimit(self):
        statment="Select * from Item Limit 15"
        self.pointer.execute(statment)
        result=self.pointer.fetchall()
        return result
        
    def GetItemWithIID(self,IID):
        statment="Select * from Item where IID=?;"
        self.pointer.execute(statment,(IID,))
        result=self.pointer.fetchone()
        if result is None:
            return []
        return list(result)

    def Search(self,Name=None,Price=None,Category=None):
        try:
            statment=""
            if Price=="" and Name == "":
                statment="Select * from Item where Category=?"
                self.pointer.execute(statment,(Category,))
                result=self.pointer.fetchall()
                if result is None:
                    return []
                return result    
            elif Price!="" and Name=="":
                statment="Select * from Item where Category=? and startingPrice < ?"
                self.pointer.execute(statment,(Category,Price))
                result=self.pointer.fetchall()
                if result is None:
                    return []
                return result
            elif Price=="" and Name!="":
                statment="Select * from Item where Category=? and name=?"
                self.pointer.execute(statment,(Category,Name))
                result=self.pointer.fetchall()
                if result is None:
                    return []
                return result
            else:
                statment="Select * from Item where Category=? and name=? and startingPrice < ?"
                self.pointer.execute(statment,(Category,Name,Price))
                result=self.pointer.fetchall()
                if result is None:
                    return []
                return result
                
        except Exception as e:
            return []
    def ListOfAuction(self):
        try:
            statment="Select DISTINCT Item.IID,Item.Name,Buyer.UID,Buyer.Price,Buyer.BidDate,Item.startingPrice,Item.Photo,Item.dateStored from Item,Buyer"
            self.pointer.execute(statment)
            result=self.pointer.fetchall()
            if result is None:
                return []
            return result
        except Exception as e:
            return []