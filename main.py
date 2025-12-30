# Main CLI Orchestration for Todo CLI
import sys
from agents.manager import add_task, toggle_task, update_task, delete_task
from agents.viewer import format_list
from agents.analytics import get_summary

def main():
    print("Welcome to In-Memory Todo CLI")
    print("Warning: All data is lost upon exit.")

    while True:
        print("\nMain Menu:")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Toggle Complete")
        print("4. Update Task")
        print("5. Delete Task")
        print("6. Show Stats")
        print("7. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            title = input("Enter Task Title: ").strip()
            description = input("Enter Description (optional): ").strip()
            resp = add_task(title, description)
            print(f"\n{resp.message}")

        elif choice == "2":
            resp = format_list()
            print(f"\n{resp.data}")

        elif choice == "3":
            try:
                task_id = int(input("Enter Task ID to toggle: ").strip())
                resp = toggle_task(task_id)
                print(f"\n{resp.message}")
            except ValueError:
                print("\nError: ID must be a number")

        elif choice == "4":
            try:
                task_id = int(input("Enter Task ID to update: ").strip())
                print("Leave blank to keep existing value")
                title = input("New Title: ").strip() or None
                description = input("New Description: ").strip() or None
                resp = update_task(task_id, title, description)
                print(f"\n{resp.message}")
            except ValueError:
                print("\nError: ID must be a number")

        elif choice == "5":
            try:
                task_id = int(input("Enter Task ID to delete: ").strip())
                resp = delete_task(task_id)
                print(f"\n{resp.message}")
            except ValueError:
                print("\nError: ID must be a number")

        elif choice == "6":
            resp = get_summary()
            d = resp.data
            print(f"\nStats: Total: {d['total']}, Completed: {d['completed']}, Pending: {d['pending']} ({d['percentage']}%)")

        elif choice == "7":
            print("Exiting. Goodbye!")
            sys.exit(0)

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
