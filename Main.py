from __future__ import annotations

import os
from project_manager import ProjectManager
from task_manager import TaskManager
from utils import (
    prompt,
    print_menu,
    print_projects,
    print_project_detail,
    show_error,
    show_ok,
)

print("DEBUG RUNNING:", os.path.abspath(__file__))


def main() -> None:
    pm = ProjectManager()
    tm = TaskManager()

    while True:
        print_menu()
        choice = prompt("Kies een optie: ")

        # Debug: laat EXACT zien wat je keuze is
        print("DEBUG choice =", repr(choice))

        try:
            if choice == "1":
                name = prompt("Projectnaam: ")
                desc = prompt("Omschrijving (optioneel): ")
                pm.create_project(name, desc)
                show_ok("Project aangemaakt.")

            elif choice == "2":
                projects = pm.list_projects()
                print("DEBUG projects count =", len(projects))
                print_projects(projects)

            elif choice == "3":
                name = prompt("Welke projectnaam? ")
                p = pm.get_project(name)
                if not p:
                    show_error("Project niet gevonden.")
                else:
                    print_project_detail(p)

            elif choice == "4":
                proj_name = prompt("In welk project? ")
                p = pm.get_project(proj_name)
                if not p:
                    show_error("Project niet gevonden.")
                    continue

                title = prompt("Taaktitel: ")
                desc = prompt("Beschrijving (optioneel): ")
                prio = prompt("Prioriteit (laag/normaal/hoog, leeg=normaal): ") or "normaal"
                tm.add_task(p, title, desc, prio)
                pm.save()
                show_ok("Taak aangemaakt.")

            elif choice == "5":
                proj_name = prompt("In welk project? ")
                p = pm.get_project(proj_name)
                if not p:
                    show_error("Project niet gevonden.")
                    continue

                title = prompt("Welke taak? ")
                new_status = prompt("Nieuwe status (bezig/afgerond): ")
                tm.change_status(p, title, new_status)
                pm.save()
                show_ok("Status aangepast.")

            elif choice == "6":
                name = prompt("Welke projectnaam sluiten? ")
                pm.close_project(name)
                show_ok("Project gesloten.")

            elif choice == "7":
                proj_name = prompt("In welk project? ")
                p = pm.get_project(proj_name)
                if not p:
                    show_error("Project niet gevonden.")
                    continue

                title = prompt("Welke taak verwijderen? ")
                tm.delete_task(p, title)
                pm.save()
                show_ok("Taak verwijderd.")

            elif choice == "0":
                print("Bye 👋")
                break

            else:
                show_error("Onbekende optie. Kies 0 t/m 7.")

        except ValueError as e:
            show_error(str(e))


if __name__ == "__main__":
    main()
