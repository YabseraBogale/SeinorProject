
create table AcutionUser(
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

create table Product(
    productId int not null primary key,
    productName varchar(30) not null,
    productImage varchar(30) not null,
    category varchar(30) not null,
    startingPrice float not null
);

create table AcutionAdmin(
    UserId int references AcutionUser
);

create table Seller(
    UserId int references AcutionUser,
    productId int references Product,
    startingtime date not null,
    closingtime date not null,
    risingrate float not null,
    rating int not null,
    roomId int not null
);

create table Bidder(
    UserId int references AcutionUser,
    productId int references Product,
    increaingprice float not null,
    lastbid float not null,
    rating int not null
);


create table winner(
    UserId int references AcutionUser,
    productId int references Product,
    servicecost float not null  
);

