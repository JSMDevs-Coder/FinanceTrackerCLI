from database_connection import *
from colorama import init, Fore, Style
import os

init(autoreset=True)

def cleanscreen():
    os.system('cls' if os.name == 'nt' else 'clear')

#comandos disponible
def add():
    cleanscreen()
    productname = input ("Product Name:")

    try:
        cost = float(input("cost of product by unit: "))
        price = float(input("price of sale by unit: "))
        amount = float(input("amount of the product on stock: "))

        if cost < 0 or price < 0 or amount < 0:
            print(Fore.RED + "no negative numbers are allowed")
            return
        
    except ValueError:
        print (Fore.RED + "Error: Enter Valid Values.")
        return
    
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO productos (nombre, costo, precio, cantidad)
        VALUES (?, ?, ?, ?)
    """, (productname, cost, price, amount))

    conn.commit()
    conn.close()

    print(f"Product '{productname}' added correctly")

def listproducts():
    cleanscreen()
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos")
    products = cursor.fetchall()

    conn.close

    print("\n--- Products ---")
    for p in products:
        print(f"ID: {p[0]} | {p[1]} | Stock: {p[4]} | Precio: {p[3]}")

def total():
    cleanscreen()
    print("total ganancia")

def create():
    cleanscreen()
    print ("crear archivo exel")

def remove():
    cleanscreen()
    print ("eliminar producto")

#definir los comandos disponibles
commands = {
    "add" : add,
    "listproducts" : listproducts,
    "total" : total,
    "create" : create,
    "remove" : remove
}

def validcommand(text):

    if text.startswith("/"):

        name = text[1:]
        
        if name in commands:

            commands[name]()

        else:

            print(Fore.RED + "Invalid Command")

    else:
        print("add a '/' to use a command")
