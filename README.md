# Distributed Systems Project

A project by Zack McKevitt and Md. Rezwanur Rahman

## Database Configuration

There is a table called ```products``` in the ```product``` database running on ```localhost```. This table has 6 columns: name VARCHAR(32), category INT, id INT, keywords VARCHAR(40), item_condition BOOL, price DOUBLE.

To get set up with the database, first install mysql. In the mysql console, execute the following commands to create a new user. I will use the credentials given in the server files:

```CREATE USER 'prod'@'localhost' IDENTIFIED BY 'prodpassword';```
```GRANT ALL PRIVILEGES ON *.* TO 'prod'@'localhost' WITH GRANT OPTION;```
```FLUSH PRIVILEGES;```

To create a new databse, use the ```init_db.py``` file. If you used a different username/password combination than above, you will need to modify the DB configuration in the ```init_db.py``` and server files. Then, to create the products table, enter the following command in your MySQL instance:

```CREATE TABLE product.products (name VARCHAR(32), category INT, id INT, keywords VARCHAR(40), item_condition BOOL, price DOUBLE);```

This will create a table called ```products``` in the ```product``` database with all of the correct columns.