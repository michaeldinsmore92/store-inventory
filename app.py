# Import libraries
from collections import OrderedDict
import csv
import datetime
import os

# Import Peewee
from peewee import *

db = SqliteDatabase('inventory.db')           

class Product(Model):
    product_id = AutoField(unique=True, primary_key=True)
    product_name = TextField()
    product_quantity = IntegerField()
    product_price = IntegerField(unique=True)
    date_updated = DateTimeField(formats='%m/%d/%Y')
    
    class Meta:
        database = db
        
def create_products():
    with open('inventory.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        products = Product.select()
        
        for row in reader:
            try:
                Product.create(product_name = row['product_name'],
                               product_quantity = row['product_quantity'],
                               product_price = row['product_price'].replace('$', '').replace('.', ''),
                               date_updated = row['date_updated']
                               )
            except IntegrityError:
                products.product_name = row['product_name']
                products.product_quantity = row['product_quantity']
                products.product_price = row['product_price']
                products.date_updated = row['date_updated']

def initialize():
    """Create database and tables"""
    db.connect()
    db.create_tables([Product], safe=True)
    
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def show_menu():
    """Show the menu"""
    choice = None
    valid_choices = ['v', 'a', 'b', 'q']
    
    while choice != 'q':
        clear()
        print("Enter 'q' to quit")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()
        if choice not in valid_choices:
            print("Sorry! That's not a valid option! ")
            input("Press 'enter' and try again... ")
        elif choice in menu:
            clear()
            menu[choice]()
    
def view_product():
    """View a single product's inventory"""
    products = Product.select()   
    search = input("Please enter Product ID: ").strip()
    
    try:
        if int(search) < len(products):
            product_name = Product.get(Product.product_id == search).product_name
            product_price = Product.get(Product.product_id == search).product_price
            product_quantity = Product.get(Product.product_id == search).product_quantity
            date_updated = Product.get(Product.product_id == search).date_updated
            print(f"Name: {product_name}")
            print(f"Price: {product_price}")
            print(f"Quantity: {product_quantity}")
            print(f"Date Updated: {date_updated}")
        else:
            print("Sorry that's not a valid value... ")
    except ValueError:
        print("Sorry that's not a valid value... ")
        
    input("Press 'enter' to continue... ")

def add_product():
    """Add a new product to the database"""
    
    choice_name = input("Please enter Product Name: ").title().strip()
    choice_quantity = input("Please enter Quantity: ").strip()
    choice_price = input("Please enter Product Price: ").strip()
    
    try:
        Product.create(product_name = choice_name,
                       product_quantity = choice_quantity,
                       product_price = choice_price,
                       date_updated = datetime.datetime.now().strftime('%m/%d/%Y')
                       )
        print("Added successfully!")
    except IntegrityError:
        product = Product.get(product_name=choice_name)
        product.product_quantity = choice_quantity
        product.product_price = choice_price
        product.date_updated = datetime.datetime.now().strftime('%m/%d/%Y')
        product.save()
        
        print("That item already exists... ")
        print("Product info has been updated! ")
        
    input("Press 'enter' to continue... ")

def backup():
    """Make a backup of the entire inventory"""
    choice = input('Would you like to make a backup? [Y/N] ').lower().strip()
    
    while choice != 'n':
        with open('backup.csv', 'a', newline='') as csvfile:
            fieldnames = ['product_id',
                          'product_name',
                          'product_quantity',
                          'product_price',
                          'date_updated'
                          ]
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
            writer.writeheader()
            
            products = Product.select().dicts()
            for product in products:
                writer.writerow(product)
                
        print("Backup saved! ")            
        break
               
    input("Press 'enter' to continue... ")
    
menu = OrderedDict([
    ('v', view_product),
    ('a', add_product),
    ('b', backup)
])

if __name__ == '__main__':
    initialize()
    create_products()
    show_menu()
