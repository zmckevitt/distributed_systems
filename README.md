# Distributed Systems Project

A project by Zack McKevitt and Md. Rezwanur Rahman

## Database Configuration

There is a table called ```products``` in the ```product``` database running on ```localhost```. This table has 6 columns: name VARCHAR(32), category INT, id INT, keywords VARCHAR(40), item_condition BOOL, price DOUBLE.

To create a new databse, use the ```init_db.py``` file. Then, to create the products table, enter the following command in your MySQL instance:

```CREATE TABLE product.products (name VARCHAR(32), category INT, id INT, keywords VARCHAR(40), item_condition BOOL, price DOUBLE);```

This will create a table called ```products``` in the ```product``` database with all of the correct columns.