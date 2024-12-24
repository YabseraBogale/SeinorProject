import sqlite3
import bcrypt

class AddisCheretaUser():
    def __init__(self) -> None:
        self.connection=sqlite3.Connection("addischereta.db",check_same_thread=False)
        self.pointer=self.connection.cursor()

    def InsertAddisCheretaUser(self,FirstName,MiddleName,LastName,Email,Phonenumber,UserLocation,Photo,Password):
        try:
            statment="Insert into addisCheretaUser(FirstName,MiddleName,LastName,Email,Phonenumber,UserLocation,Photo,Password) values(?,?,?,?,?,?,?,?)"
            self.pointer.execute(statment,(FirstName,MiddleName,LastName,Email,Phonenumber,UserLocation,Photo,Password))
            self.connection.commit()
            return "True"
        except Exception as e:
            return str(e)   
     
    def GetAllCheretaUserEmail(self):
        statment="select Email from addisCheretaUser"
        self.pointer.execute(statment)
        result=self.pointer.fetchall()
        lst=[]
        for  i in result:
            lst.append(i[0])
        return lst
    
    def GetCheretaUserDataJson(self):
        statment="select * from addisCheretaUser"
        self.pointer.execute(statment)
        result=self.pointer.fetchall()
        lst={}
        for i in result:
            lst[i[0]]={"email":i[4],"name":i[1]+i[2],"phoneumber":i[5],"location":i[6],"photo":"./uploads/"+i[7]}
        return lst
    
    def ExistsInAddisCheretaUser(self,Email):
        statment="select count(email) from addisCheretaUser where Email=(?)"
        self.pointer.execute(statment,(Email,))
        result=self.pointer.fetchone()
        if result[0]==0:
            return False
        return True
    
    def GetAddisCheretaUserData(self,Email):
        statment="select * from addisCheretaUser where email=(?)"
        self.pointer.execute(statment,(Email,))
        result=self.pointer.fetchone()
        if result is None:
            return []
        return result
    
    def ResetPassWordForUser(self,Email,Newpassword):
        hashpassword=bcrypt.hashpw(str(Newpassword).encode('utf-8'),bcrypt.gensalt())
        statment="update addisCheretaUser set Password=(?) where email=(?);"
        self.pointer.execute(statment,(hashpassword,Email))
        self.connection.commit()
        return "Password Changed"
        