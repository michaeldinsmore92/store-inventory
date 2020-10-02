# store-inventory
Unit 4 (A Store Inventory)

This is an inventory application.

'app.py' imports data from 'csvfile' and exports into a database called 'inventory.db'

User has 3 options:
1) "View a single product's inventory"
2) "Add a new product to the database"
3) "Make a backup of the entire inventory"
    *Enter 'q' to quit at any given time.

1) User is prompted to enter a product ID number, and a print of the correct product's information will be displayed.
    *If a product ID doesn't exist, an error message will be displayed.

2) User is prompted to enter a product name, then quantity, then price. This product will be entered into the database.
    *If a duplicate is found, the app will check the existing product entry, and only save User data.
    
3) Creates a csv file called 'backup.csv' that contains the current contents of the database.
