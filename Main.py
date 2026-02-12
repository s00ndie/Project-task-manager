from __future__ import annotations

from utils import (
    search_tasks_across_projects,   # ← додаємо
)

import os
from utils import print_project_statistics
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
        choice = prompt("Kies een optie: ").strip()

        try:
            if choice == "1":
                name = prompt("Projectnaam: ")
                desc = prompt("Omschrijving (optioneel): ")
                pm.create_project(name, desc)
                show_ok("Project aangemaakt.")

            elif choice == "2":
                print_projects(pm.list_projects())

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
                prio = prompt("Prioriteit (laag/normaal/hoog, leeg=normaal): ").strip() or "normaal"
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
                new_status = prompt("Nieuwe status (bezig/afgerond): ").strip()
                tm.change_status(p, title, new_status)
                pm.save()
                show_ok("Status aangepast.")

            elif choice == "6":
                name = prompt("Welke projectnaam sluiten? ")
                pm.close_project(name)
                show_ok("Project gesloten.")
                pm.save()

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

            elif choice == "8":  # ← NIEUW: statistiek
                name = prompt("Van welk project wil je de statistiek zien? ")
                p = pm.get_project(name)
                if not p:
                    show_error("Project niet gevonden.")
                else:
                    print_project_statistics(p)
            
            elif choice == "9":
                name = prompt("Welk project? ")
                p = pm.get_project(name)
                if not p:
                    show_error("Project niet gevonden.")
                else:
                    filt = prompt("Filter op status (nieuw/bezig/afgerond/alle): ").strip().lower()
                    print_filtered_tasks(p, filt)

            elif choice == "0":
                print("Tot ziens! 👋")
                break

            else:
                show_error("Ongeldige keuze. Probeer opnieuw (0–8).")

        except ValueError as e:
            show_error(str(e))


if __name__ == "__main__":
    main()
