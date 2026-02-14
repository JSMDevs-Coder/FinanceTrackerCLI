from commands import *
from database_connection import *

create_table()

while True:
    vcommand = input(">")
    validcommand(vcommand)