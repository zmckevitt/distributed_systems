# Distributed Systems Project

A project by Zack McKevitt and Md. Rezwanur Rahman. This repository consists of five files: a database initializer, buyer/seller servers, and buyer/seller clients. Each server connects to a MySQL instance that is running on the same machine as the servers, allowing the servers to quickly interact with the local database. Clients can call a number of select API calls to interface with the product database. The clients communicate with the servers by means of TCP sockets. 

The seller server interfaces with the products table in the product database while the buyer interfaces with the cart table in the product database. More database information is provided below.

## API Functions

### Seller API functions

- ```sell``` - List an item for sale. Provide an item name, category, ID, keywords, condition, and sale price. This will call an INSERT command into the database to add a new entry.

- ```modify``` - Modify the price of a current item. Provide an item ID and new price. This will call an UPDATE query on the database.

- ```remove``` - Remove an entry from the database. Provide an item ID and quantity. This will invoke a DELETE query and remove the quantity of items specified from the database.

- ```list``` - Lists all items in the database. Invokes a SELECT query.

- ```clear``` - Clear the current cart. This will issue a DELETE command to delete everything from cart.

- ```create``` - Creates a user with username and password in the Users table of Customer database. 

- ```login``` - Takes username and password as input. Returns successful if username password mache, otherwise fails.

- ```logout``` - Logs out the current logged-in user.

- ```rating``` - Fetches all the ratings from feedback table for a seller .

### Buyer API functions

- ```search``` - Search items by category. Provide an item category and keywords. This will use a SELECT query that passes the keywords to the LIKE command, which will match the provided keywords to similar ones in the database.

- ```display``` - Displays the current user's cart with a SELECT query.

- ```remove``` - Remove an item from the cart. Provide item id and quantity, which will issue an UPDATE database query to decrement the item's count. NOTE: removed items will remain in the cart with a quantity of zero. This was intended to keep items in a user's cart in case they intend to re-add them later on.

- ```clear``` - Clear the current cart. This will issue a DELETE command to delete everything from cart.

- ```add``` - Add item to cart. Provide item ID and quantity, which will issue an INSERT query to the database. NOTE: it is possible to add more items than there are available to your cart. This will be addressed when transactions are added to the application.

- ```create``` - Creates a user with username and password in the Users table of Customer database. 

- ```login``` - Takes username and password as input. Returns successful if username password mache, otherwise fails.

- ```logout``` - Logs out the current logged-in user.

- ```purchase``` - Purchases item(s) with card information: name, card number and expiration 

- ```feedback``` - User can give feedback for a seller as good or bad

- ```rating``` - Fetches all the ratings from feedback table for a seller.

- ```history``` - Fetches all purchases of a customer from the 'purchased' table


## Assumptions

For the database, we are assuming that there is only one user and one seller. This is because we did not need to implement any sort of login or registration features, and thus have no way to track users across sessions. Instead, any calls to ```list``` or ```display``` will list the entirety of the products or cart tables, respectively.

Additionally, the products table adds duplicate entries as new rows, while the cart database increments an already added item's quantity field. This was chosen so that removed items can stay in the cart even upon removal.

Lastly, we assume that the MySQL database will always be hosted on the same machine as each of the servers, and is the same database across both. 

## State of the project

The current state of the project is functional but not yet polished, mainly due to the nature of the assignment. As we add more to this project, it will become increasingly polished. In its current state, each of the API calls we were asked to implement are completely functional, but the current state of the project is less polished on the client sides. For example, we are returning raw database query information directly back to the user. As we are only implementing an API, we decided to focus our attention on implementing our API and ensuring that it works correctly.

We currently do not have support for account creation, seller feedback/rating, buyer history, or transactions. We expect to implement these features in the coming weeks.

## Database Configuration

There is a table called ```products``` in the ```product``` database running on ```localhost```. This table has 6 columns: name VARCHAR(32), category INT, id INT, keywords VARCHAR(40), item_condition BOOL, price DOUBLE.

To get set up with the database, first install mysql. In the mysql console, execute the following commands to create a new user. I will use the credentials given in the server files:

```CREATE USER 'prod'@'localhost' IDENTIFIED BY 'prodpassword';```

```GRANT ALL PRIVILEGES ON *.* TO 'prod'@'localhost' WITH GRANT OPTION;```

```FLUSH PRIVILEGES;```

To create a new databse, use the ```init_db.py``` file. If you used a different username/password combination than above, you will need to modify the DB configuration in the ```init_db.py``` and server files. This will create the product database with the following table commands:

```CREATE TABLE product.products (name VARCHAR(32), category INT, id INT, keywords VARCHAR(40), item_condition BOOL, price DOUBLE, s_id INT);```

This will create a table called ```products``` in the ```product``` database with all of the correct columns.

```CREATE TABLE product.cart (id INT, b_id INT, quantity INT);```

This will create a table called ```cart``` with columns id and quantity

To create the customers database, use the following command in MySQL:

```CREATE DATABASE customer;```

To create a table for user information (both buyer and seller), issue the following create table command:

```CREATE TABLE customer.users (name VARCHAR(32), id INT, nitems INT);```

Next, we need to add a ratings table for feedback:

```CREATE TABLE customer.feedback (id INT, pos INT, neg INT);```

A passwords table:

```CREATE TABLE customer.passwords (id INT, password VARCHAR(32));```

A buyer history table:

```CREATE TABLE customer.purchased(id INT, b_id INT, quantity INT);```

Lastly, we need a table to keep track of users currently logged in:

```CREATE TABLE customer.logged (id INT, logged BOOL);```


## Timing Benchmarks

We determined timing benchmarks entirely client-side, measuring the timing difference between the sending of the command and the receiving of the response. We tested these benchmarks in two scenarios: communications between two processes on the same machine and communications between two different machines on the same LAN.

### Configuration: Server and DB on Google Cloud and Client on PC

Seller benchmarks: 

- ```sell``` - 0.12314s

- ```modify``` - 0.43276s

- ```remove``` - 0.11799s

- ```list``` - 0.17842s

- ```create``` - 0.54668s

- ```login``` - 0.11099s

- ```logout``` - 0.19256s

- ```rating``` - 0.39720s


Seller benchmark average: 0.2624675s = 262.46ms

Buyer benchmarks:

- ```search``` - 0.42031s

- ```display``` - 0.40018s

- ```remove``` - 0.42287s

- ```clear``` - 0.13140s

- ```add``` - 0.56263s

-```create```- 0.91323s

-```login```- 0.23005s

-```logout```- 0.34269s

-```purchase```- 0.60980s

-```feedback```- 0.39177

-```rating```- 0.16186s

-```history```- 1.00593s

Buyer benchmark Average: 0.46606 = 466.06ms

Overal Average: 386.22ms


### Congiguration: LAN Machines (For previous socket config)

Seller benchmarks:

- ```sell``` - 0.01580s

- ```modify``` - 0.02410s

- ```remove``` - 0.03597s

- ```list``` - 0.02128s

-```create```- 0.64591

-```login```- 1.22935

-```login```- 0.23005

-```logout```- 0.87905

-```rating```- 0.16428

Seller benchmark average: 0.02429s = 24.29 ms

Buyer benchmarks:

- ```search``` - 0.01017s

- ```display``` - 0.01416s

- ```remove``` - 0.01793s

- ```clear``` - 0.04088s

- ```add``` - 0.01632s

Buyer benchmark average: 0.01989s = 19.89ms

LAN Machine average: 22.09ms
