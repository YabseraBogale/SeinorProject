import sqlite3
import bcrypt


salt=bcrypt.gensalt()

class Admin():
    def __init__(self) -> None:
        self.connection=sqlite3.Connection("addischereta.db",check_same_thread=False)
        self.pointer=self.connection.cursor()
    
    def InsertNewAdmin(self,username,password):
        try:
            password=bcrypt.hashpw(password.encode('utf-8'), salt)
            statment="Insert into Admin(username,password) values(?,?);"
            self.pointer.execute(statment,(username,password))
            self.connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False 

    def GetAdminWithUsername(self,username):
        statment="select * from Admin where username=(?)"
        self.pointer.execute(statment,(username,))
        result=self.pointer.fetchall()
        if result is None:
            return []
        return result


