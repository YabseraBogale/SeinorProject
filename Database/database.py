from os import stat
import sqlite3

class Database():
    
    def __init__(self) -> None:
        self.allowedfileextension={"png","jpg","jpeg"}
        self.connection=sqlite3.Connection("addischereta.db",check_same_thread=False)
        self.pointer=self.connection.cursor()
    
    def CreatTables(self):
        print(self.AddisCheretaUserTables())
        print(self.VerficationTable())
        print(self.ItemTable())
        print(self.SellerTable())
        print(self.BuyerTable())
        print(self.AcutionTable())
        print(self.FinaleAcutionTable())
        return "All are made"


    def AddisCheretaUserTables(self):
        try:
            statment=""" create table addisCheretaUser( UID int AUTO_INCREMENT NOT NULL PRIMARY KEY, FirstName varchar(30) not null, MiddleName varchar(30) not null, LastName varchar(30) not null, Email Text not null UNIQUE, Phonenumber varchar(30) not null, UserLocation varchar(30) not null, Photo Text, Password Text not null ); """
            self.pointer.execute(statment)
            self.connection.commit()
            return "addisCheretaUser table made"
        except Exception as e:
            return e
    def VerficationTable(self):
        statment=""" create table Verfication( code  int not null ,Email Text not null references addisCheretaUser, dateStored date not null , status varchar(8) not null ); """
        self.pointer.execute(statment)
        self.connection.commit()
        return "Verfication table made"

    def ItemTable(self):
        try:
            statment=""" Create table Item( IID int AUTO_INCREMENT primary key, Name text not null, Description text not null,status varchar(15) not null, Photo Text not null, Category varchar(30) not null,startingPrice float not null); """
            self.pointer.execute(statment)
            self.connection.commit()
            return "Item table made"
        except Exception as e:
            return e
        
    def SellerTable(self):
        try:
            statment=""" create table Seller( UID int REFERENCES addisCheretaUser, IID int REFERENCES Item, Description Text, Rating int not null); """
            self.pointer.execute(statment)
            self.connection.commit()
            return "Seller table made"
        except Exception as e:
            return e
    
    def BuyerTable(self):
        try:
            statment=""" create Table Buyer( UID int references addisCheretaUser, IID int references Item ); """
            self.pointer.execute(statment)
            self.connection.commit()
            return "Buyer table made"
        except Exception as e:
            return e
        
    def AcutionTable(self):
        try:
            statment=""" create table Auction( AID int AUTO_INCREMENT primary key, IID int REFERENCES Item, UID int REFERENCES addisCheretaUser,Description Text not null, startTime date not null, EndTime date not null, Status varchar(15) not null, ReservePrice float not null );"""
            self.pointer.execute(statment)
            self.connection.commit()
            return "Acution table made"
        except Exception as e:
            return e
        
    def FinaleAcutionTable(self):
        try:
            statment=""" create Table FinalAuctionMessage( UID int REFERENCES addisCheretaUser, startTime date not null, messageTalk Text not null, Photo varchar(30) not null );"""
            self.pointer.execute(statment)
            self.connection.commit()
            return "FinaleAcutionTable table made"
        except Exception as e:
            return e
        
    def RateTable(self):
        try:
            statment="""create table Rating( UID int REFERENCES addisCheretaUser,ratedUserID int not null,rateValue int not null);"""
            self.pointer.execute(statment)
            self.connection.commit()
            return "Rating table made"
        except Exception as e:
            return e
        
    def AllowedFile(self,filename):
        if filename is None:
            return False
        return "." in filename and filename.rsplit('.',1)[1].lower() in self.allowedfileextension

