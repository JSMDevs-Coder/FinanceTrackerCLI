from database_connection import *
from colorama import init, Fore, Style
import os
import sys

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
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            SUM(costo * cantidad),
            SUM(precio * cantidad),
            SUM((precio - costo) * cantidad)
        FROM productos
    """)

    result = cursor.fetchone()
    conn.close()

    total_investment = result[0] if result[0] else 0
    total_tax_off = result[1] if result[1] else 0
    total_profit = result[2] if result[2] else 0

    try:
        tax_percentage = float(input("enter the tax percentage: "))
        if tax_percentage < 0:
            print("the tax percentage cant be negative")
            return
    except ValueError:
        print("please enter a valid value")
        return
    
    tax_decimal = tax_percentage / 100
    total_tax = total_tax_off * tax_decimal
    total_tax_on = total_tax_off + total_tax

    print("\n========== FINANCIAL SUMMARY ==========")
    print(f"Total Investment:      ${total_investment:.2f}")
    print(f"Total excluding taxes:      ${total_tax_off:.2f}")
    print(f"Tax ({tax_percentage}%):      ${total_tax:.2f}")
    print(f"Total including taxes:      ${total_tax_on:.2f}")
    print(f"Potential gain:      ${total_profit:.2f}")
    print("========================================")

def create():
    cleanscreen()
    print ("crear archivo exel")

def remove():
    cleanscreen()

    conn = connect()
    cursor = conn.cursor()

    #mostrar los productos disponibles
    cursor.execute("SELECT id, nombre, cantidad FROM productos")
    products = cursor.fetchall()

    if not products:
        print("No products available")
        conn.close()
        return
    
    print("\n--- PRODUCTS AVAILABLE ---")
    for p in products:
        print(f"ID: {p[0]} | {p[1]} | Stock: {p[2]}")

    try:
        product_id = int(input("Enter the ID of the product to delete: "))
    except ValueError:
        print("You must enter a valid number.")
        conn.close()
        return
    
    #verificar si el producto existe
    cursor.execute("SELECT * FROM productos WHERE id = ?", (product_id,))
    product = cursor.fetchone()

    if not product:
        print("Product not found.")
        conn.close()
        return
    
    #confirmacion
    confirmation = input(f"Are you sure you want to delete '{product[1]}'? (y/n): ").lower()

    if confirmation == "y":
        cursor.execute("DELETE FROM productos WHERE id = ?", (product_id,))
        conn.commit()
        print("Product successfully deleted.")
    else:
        print("Operation cancelled.")

    conn.close()


def help():
    cleanscreen()

    print(Fore.CYAN + "========== AVAILABLE COMMANDS ==========")
    print(Style.RESET_ALL)

    print(f"{Fore.GREEN}add{Style.RESET_ALL}           -> Add a new product to inventory")
    print(f"{Fore.GREEN}listproducts{Style.RESET_ALL}  -> Show all products in inventory")
    print(f"{Fore.GREEN}remove{Style.RESET_ALL}        -> Delete a product by ID")
    print(f"{Fore.GREEN}total{Style.RESET_ALL}         -> Show financial summary")
    print(f"{Fore.GREEN}registersale{Style.RESET_ALL}  -> Register a product sale")
    print(f"{Fore.GREEN}create{Style.RESET_ALL}        -> Create Excel file (coming soon)")
    print(f"{Fore.GREEN}help{Style.RESET_ALL}          -> Show this help menu")

    print(Fore.CYAN + "========================================")

def registersale():
    cleanscreen()
    
    conn = connect()
    cursor = conn.cursor()

    #mostrar productos disponibles
    cursor.execute("SELECT id, nombre, precio, costo, cantidad FROM productos")
    products = cursor.fetchall()

    if not products:
        print(Fore.RED + "No products available.")
        conn.close()
        return
    
    print(Fore.CYAN + "\n--- AVAILABLE PRODUCTS ---")
    print("--------------------------------------------")
    for p in products:
        print(f"ID: {p[0]} | {p[1]} | Stock: {p[4]} | Price: ${p[2]}")
    print("--------------------------------------------")

    #pedir la id del producto
    try:
        product_id = int(input("Enter product ID: "))
    except ValueError:
        print(Fore.RED + "Invalid ID.")
        conn.close()
        return
    
    #verificar la existencia del producto
    cursor.execute("SELECT nombre, precio, costo, cantidad FROM productos WHERE id = ?", (product_id,))
    product = cursor.fetchone()

    if not product:
        print(Fore.RED + "Product not found.")
        conn.close()
        return
    
    name, price, cost, stock = product

    #pedir cantidad por vender
    try:
        quantity = float(input("Enter quantity to sell: "))
        if quantity <= 0:
            print(Fore.RED + "Quantity must be greater than 0.")
            conn.close()
            return
    except ValueError:
        print(Fore.RED + "Invalid quantity.")
        conn.close()
        return
    
    #verificar el stock
    if quantity > stock:
        print(Fore.RED + "Not enough stock available.")
        conn.close()
        return
    
    #calcular totales
    total_sale = price * quantity
    profit = (price - cost) * quantity
    new_stock = stock - quantity

    #actualizar la base de datos
    cursor.execute("""
        UPDATE productos
        SET cantidad = ?
        WHERE id = ?
    """, (new_stock, product_id))

    conn.commit()
    conn.close()

    print(Fore.GREEN + "\nSale registered successfully!")
    print("--------------------------------------------")
    print(f"Product: {name}")
    print(f"Quantity sold: {quantity}")
    print(f"Total sale: ${total_sale:.2f}")
    print(f"Profit from this sale: ${profit:.2f}")
    print(f"Remaining stock: {new_stock}")
    print("--------------------------------------------")

def exit():
    print(Fore.YELLOW + "Closing Inventory System...")
    print(Fore.WHITE + "Goodbye 👋")

    sys.exit()

#definir los comandos disponibles
commands = {
    "add" : add,
    "listproducts" : listproducts,
    "total" : total,
    "create" : create,
    "remove" : remove,
    "help" : help,
    "registersale" : registersale,
    "exit" : exit
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