create table addisCheretaUser(
	UID int AUTO_INCREMENT NOT NULL PRIMARY KEY,
	FirstName varchar(30) not null,
	MiddleName varchar(30) not null,
	LastName varchar(30) not null,
	Email Text not null UNIQUE,
	Phonenumber varchar(30) not null,
	UserLocation varchar(30) not null,
  	Photo Text,
	Password Text not null
);

create table Verfication(
	code  int not null  primary key,
	Email Text references addisCheretaUser,
  	dateStored date not null,
	status varchar(8) not null 
);

Create table Item(
	IID int AUTO_INCREMENT not null primary key,
	UID int references addisCheretaUser,
	Name text not null,
	Description text not null,
	status varchar(15) not null,
	dateStored date not null,
	Photo varchar(30) not null,
	Category varchar(30) not null,
	startingPrice float not null
);

create table Seller(
	UID int REFERENCES addisCheretaUser,
	IID int REFERENCES Item,
	Description Text,
	Rating int not null
);

create Table Buyer(
	UID int references addisCheretaUser,
	IID int references Item,
	BidDate date not null,
	Price float not null
);

create table Auction(
	AID int AUTO_INCREMENT primary key,
	IID int REFERENCES Item,
	UID int REFERENCES addisCheretaUser,
  	Description Text not null,
	startTime date not null,
	EndTime date not null,
	Status varchar(15) not null,
	ReservePrice float not null
);

create Table FinalAuctionMessage(
	UID int REFERENCES addisCheretaUser,
	startTime date not null,
	messageTalk Text not null,
	Photo varchar(30) not null
);


create table Rating(
	UID int REFERENCES addisCheretaUser,
	ratedUserID int not null,
	rateValue int not null
);

create table Admin(
	username varchar(12) not null primary key,
	Password text not null
);
