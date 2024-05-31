create table User(
    UserId int not null primary key,
    firstName varchar(20) not null,
    MiddleName varchar(20) not null,
    LastName varchar(20) not null,
    Password Text not null,
    Phonenumber varchar(20) not null,
    Email varchar(40) not null,
    location varchar(20) not null,
    Dateofregsistartion date not null,
    Dateofbirth date not null
);

create table product(
    productId int not null primary key,
    productName varchar(30) not null,
    productImage varchar(30) not null,
    category varchar(30) not null,
    startingPrice float not null
);

create table Admin(
    UserId int not null primary key,
    FOREIGN  key UserId references User(UserId)
);

create table Seller(
    UserId int not null primary key,
    productId int not null,
    startingtime date not null,
    closingtime date not null,
    risingrate float not null,
    rating int not null,
    roomId int not null,
    FOREIGN  key UserId references User(UserId),
    FOREIGN  key productId references product(productId)
);

create table Bidder(
    UserId int not null primary key,
    productId int not null,
    roomId int not null,
    increaingprice float not null,
    rating int not null,
    FOREIGN  key UserId references User(UserId),
    FOREIGN  key productId references product(productId)
    FOREIGN  key roomId references Seller(roomId)
);

create table winner(
    UserId int not null primary key,
    productId int not null,
    servicecost float not null,
    FOREIGN  key UserId references User(UserId),
    FOREIGN  key productId references product(productId)
    
);
