import sqlite3

class Auctioin():
    def __init__(self) -> None:
        self.connection=sqlite3.Connection("addischereta.db",check_same_thread=False)
        self.pointer=self.connection.cursor()
    
    def InsertAuctionTable(self,IID,UID,Description,StartTime,EndTime,Status,ReservePrice):
        statment="Insert into Auction(IID,UID,Description,StartTime,EndTime,Status,ReservePrice) values(?,?,?,?,?,?,?)"
        self.pointer.execute(statment,(IID,UID,Description,StartTime,EndTime,Status,ReservePrice))
        self.connection.commit()
        return "True"