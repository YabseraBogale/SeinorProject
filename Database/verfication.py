import sqlite3
import random
import string
import time
from datetime import datetime,timedelta

class Verfication():

    def __init__(self) -> None:
        self.connection=sqlite3.Connection("addischereta.db",check_same_thread=False)
        self.pointer=self.connection.cursor()
    
    def InsertVerficationTable(self,Code,Email,DateStored,Status):
        time.sleep(3)
        statment="Insert into Verfication(code,Email,DateStored,status) values(?,?,?,?)"
        self.pointer.execute(statment,(Code,Email,DateStored,Status))
        self.connection.commit()
        return "True"
    
    def UpdateVerficationTable(self,Email):
        time.sleep(3)
        statment="update Verfication set code=(?),DateStored=(?) where email=(?);"
        code=''.join(random.choices(string.digits, k=6))
        futureTime=datetime.now()+timedelta(minutes=10)
        self.pointer.execute(statment,(code,futureTime,Email))
        self.connection.commit()
        return ["code",code]   
     
    def GetEmailForVerfication(self,Email):
        time.sleep(3)
        statment="select * from Verfication where email=(?) order by dateStored DESC "
        self.pointer.execute(statment,(Email,))
        result=self.pointer.fetchone()
        if result is not None:
            return result
        return []