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
          if result is None:
              return 0
          return list(result)[0]
        except Exception as e:
           return 0
    
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
        