import sqlite3

class Buyer():

    def __init__(self) -> None:
            self.connection=sqlite3.Connection("addischereta.db",check_same_thread=False)
            self.pointer=self.connection.cursor()

    def InsertBuyerTable(self,UID,IID,BidDate,Price):
        try:
            statment="insert into Buyer(UID,IID,BidDate,Price) values(?,?,?,?)"
            self.pointer.execute(statment,(UID,IID,BidDate,Price))
            self.connection.commit()
            return True
        except Exception as e:
            return False
        
    def HighestBid(self,IID):
        try:
          statment="Select Max(Price) from Buyer where IID=?"
          self.pointer.execute(statment,(IID,))
          result=self.pointer.fetchone()
          if result==None:
              return 0
          return list(result)[0]
        except Exception as e:
           return 0
    
    def GetUserBidWithUserId(self,UID):
        try:
            statment="Select DISTINCT Buyer.BidDate,Buyer.Price,Item.Name,Item.Category,Buyer.IID from Buyer,Item where Item.IID=Buyer.IID and Buyer.UID=?"
            self.pointer.execute(statment,(UID))
            result=self.pointer.fetchall()
            if result is None:
                return []
            return result
        except Exception as e:
            return []

    def HighestBidWinnerWithId(self,IID):
        try:
            statment="Select Max(Price),* from Buyer where IID=?"
            self.pointer.execute(statment,(IID,))
            result=self.pointer.fetchone()
            if result is None:
                return []
            return list(result)
        except Exception as e:
            return []
        
    def DeleteWithBuyerIdAndPrice(self,Price,UID,IID):
        try:
            statment="Delete from Buyer Where Price=? and UID=? and IID=?"
            self.pointer.execute(statment,(Price,UID,IID))
            self.connection.commit()
            return True
        except Exception as e:
            return False
