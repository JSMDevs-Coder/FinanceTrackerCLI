from commands import *
from database_connection import *

def home():
    cleanscreen()

    print(Fore.CYAN + Style.BRIGHT + """
╔══════════════════════════════════════════════╗
║              FINANCE TRACKER CLI            ║
║                                              ║
║        Inventory & Profit Management        ║
╚══════════════════════════════════════════════╝
""")

    print(Fore.YELLOW + "Available Commands:\n")

    print(Fore.GREEN + " /add            " + Fore.WHITE + "→ Add new product")
    print(Fore.GREEN + " /listproducts   " + Fore.WHITE + "→ Show inventory")
    print(Fore.GREEN + " /registersale   " + Fore.WHITE + "→ Register a sale")
    print(Fore.GREEN + " /total          " + Fore.WHITE + "→ Financial summary")
    print(Fore.GREEN + " /remove         " + Fore.WHITE + "→ Delete a product")
    print(Fore.GREEN + " /create         " + Fore.WHITE + "→ Export to Excel (coming soon)")
    print(Fore.GREEN + " /help           " + Fore.WHITE + "→ Show commands again")
    print(Fore.GREEN + " /exit           " + Fore.WHITE + "→ Close the program")


    print(Fore.MAGENTA + "\n──────────────────────────────────────────────")
    print(Fore.BLUE + "Developed by: JS")
    print(Fore.MAGENTA + "──────────────────────────────────────────────\n")