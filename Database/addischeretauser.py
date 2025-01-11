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
        try:
            statment="select Email from addisCheretaUser"
            self.pointer.execute(statment)
            result=self.pointer.fetchall()
            lst=[]
            for  i in result:
                lst.append(i[0])
            return lst
        except Exception as e:
            return []
    def GetCheretaUserDataJson(self):
        try:
            statment="select * from addisCheretaUser"
            self.pointer.execute(statment)
            result=self.pointer.fetchall()
            lst={}
            for i in result:
                lst[i[0]]={"email":i[4],"name":i[1]+i[2],"phoneumber":i[5],"location":i[6],"photo":"./uploads/"+i[7]}
            return lst
        except Exception as e:
            return []
    
    def ExistsInAddisCheretaUser(self,Email):
        try:
            statment="select count(email) from addisCheretaUser where Email=(?)"
            self.pointer.execute(statment,(Email,))
            result=self.pointer.fetchone()
            if result[0]==0:
                return False
            return True
        except Exception as e:
            return False
    
    def GetAddisCheretaUserData(self,Email):
        try:
            statment="select * from addisCheretaUser where email=(?)"
            self.pointer.execute(statment,(Email,))
            result=self.pointer.fetchone()
            if result is None:
                return []
            return result
        except Exception as e:
            return []
    
    def ResetPassWordForUser(self,Email,Newpassword):
        try:
            hashpassword=bcrypt.hashpw(str(Newpassword).encode('utf-8'),bcrypt.gensalt())
            statment="update addisCheretaUser set Password=(?) where email=(?);"
            self.pointer.execute(statment,(hashpassword,Email))
            self.connection.commit()
            return "Password Changed"
        except Exception as e:
            return []
        
    def GetAllUserDataUidFirstNameEtc(self):
        try:
            statment="Select UID,Photo,FirstName,MiddleName,LastName,Email,Phonenumber,UserLocation from addischeretauser"
            self.pointer.execute(statment)
            result=self.pointer.fetchall()
            if result is None:
                return []
            return result
        except Exception as e:
            return []
    
    def GetPhonenumberEmailWithUID(self,UID):
        try:
            statment="Select Email,Phonenumber from addischeretauser where UID=?"
            self.pointer.execute(statment,(UID,))
            result=self.pointer.fetchone()
            if result is None:
                return []
            return list(result)
        except Exception as e:
            return []
    
    def GetPhotoWithUID(self,UID):
        try:
            statment="Select Photo from addischeretauser where UID=?"
            self.pointer.execute(statment,(UID,))
            result=self.pointer.fetchone()
            if result is None:
                return False
            return result[0]
        except Exception as e:
            return False