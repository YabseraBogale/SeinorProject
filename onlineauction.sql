create table User(
    UserId int not null primary key,
    firstName varchar(20) not null,
    MiddleName varchar(20) not null,
    LastName varchar(20) not null,
    password Text not null,
    Dateofregsistartion date not null,
    Dateofbirth date not null
);