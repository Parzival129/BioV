"""
The main function that allows the user to interact with all the other functions
"""

from rich.console import Console
import register
import authorize
import sys
import DB.VaxDB as VaxDB
import DB.hashDB as hashDB
console = Console()

def titleCard():
    '''
    displays the titlecard and menu options
    Ival: None
    Rval: None
    '''
    print("")
    console.print("[bold green]    ____  _       __ __              ___         __  __  [bold green]")
    console.print("[bold green]   / __ )(_)___  / //_/__  __  __   /   | __  __/ /_/ /_ [bold green]")
    console.print("[bold green]  / __  / / __ \/ ,< / _ \/ / / /  / /| |/ / / / __/ __ |[bold green]")
    console.print("[bold green] / /_/ / / /_/ / /| /  __/ /_/ /  / ___ / /_/ / /_/ / / /[bold green]")
    console.print("[bold green]/_____/_/\____/_/ |_\___/\__, /  /_/  |_\__,_/\__/_/ /_/ [bold green]")
    console.print("[bold green]                        /____/                           [bold green]")
    console.print("Developed By: Russell Tabata & Thomas Lauder", style="bold cyan")
    print("")
    console.print("[bold cyan]1.[/bold cyan] REGISTER User BioKey")
    console.print("[bold cyan]2.[/bold cyan] AUTHENTICATE User BioKey")
    console.print("[bold cyan]3.[/bold cyan] DELETE User Biokey")
    console.print("[bold cyan]4.[/bold cyan] UPDATE User Vaccinations")
    console.print("[bold cyan]5.[/bold cyan] DISPLAY these options")
    console.print("[bold cyan]6.[/bold cyan] EXIT")

titleCard()

while True:
    print("")
    job = input("?> ")

    if job == "1" or job.lower() == "register":
        register.main()

    if job == "2" or job.lower() == "authenticate" or job.lower() == "authorize":
        authorize.main()

    if job == "3" or job.lower() == "delete":
        resp = authorize.checkbiometrics()
        if resp != False and register.deleteFace(resp) and hashDB.deleteItem(resp) == 200 and VaxDB.deleteItem(resp) == 200:
                    console.print("[bold green]Completed deleting your biokey data!")
        else:
            console.print('[bold red]Failed to delete from hashDB')

    if job == "4" or job.lower() == "update":
        resp = authorize.checkbiometrics()
        if resp != False:
            vaxs = input("Vaccinations (split up by spaces) >> ")
            vacsset = []
            for i in vaxs.strip().split(" "):
                vacsset.append(i)
            VaxDB.registerVaccinations(resp, vacsset)
            console.print("[bold green]Completed updating your vaccinations!")

    if job == "5" or job.lower() == "display":
        titleCard()

    if job == "6" or job.lower() == "exit":
        sys.exit()
