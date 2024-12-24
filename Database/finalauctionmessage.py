import sqlite3

class FinalAuctionMessage():
    
    def __init__(self) -> None:
        self.connection=sqlite3.Connection("addischereta.db",check_same_thread=False)
        self.pointer=self.connection.cursor()

    def InsertFinalAuctionMessage(self,UID,StartTime,MessageTalk,Photo):
        statment="Insert into FinaleAcutionMessage(UID,StartTime,MessageTalk,Photo) values(?,?,?,?)"
        self.pointer.execute(statment,(UID,StartTime,MessageTalk,Photo))
        self.connection.commit()
        return "True"