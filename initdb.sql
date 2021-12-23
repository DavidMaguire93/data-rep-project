use datarepresentation;

create table products(
     ProductID int PRIMARY KEY AUTO_INCREMENT,
     name varchar (250),
     category varchar (250),
     price float
    );


CREATE TABLE orders (
  orderID INT PRIMARY KEY AUTO_INCREMENT,
  customerID INT,
  productID INT,
  quantity INT
     );
  