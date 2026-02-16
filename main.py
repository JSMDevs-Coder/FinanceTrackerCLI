from commands import *
from database_connection import *
from home_screen import *

create_table()
home()

while True:
    vcommand = input(
    Fore.BLUE + "┌──(" +
    Fore.CYAN + "FinanceTracker" +
    Fore.BLUE + ")\n└─$ " +
    Fore.GREEN
)
    validcommand(vcommand)