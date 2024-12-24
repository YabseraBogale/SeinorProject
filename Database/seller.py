import sqlite3

class Seller():

    def __init__(self) -> None:
        self.connection=sqlite3.Connection("addischereta.db",check_same_thread=False)
        self.pointer=self.connection.cursor()
    
    def InsertSellerTable(self,UID,IID,Description,Rating):
        statment="Insert into Seller(UID,IID,Description,Rating) values(?,?,?,?)"
        self.pointer.execute(statment,(UID,IID,Description,Rating))
        self.connection.commit()
        return "True"