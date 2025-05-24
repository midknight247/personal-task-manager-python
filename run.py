from taskmanager import TaskManager

def main():
    tm = TaskManager()

    while True:
        print("\n --- Task Manager ---")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            tm.view_tasks()
        elif choice == '2':
            title = input("Enter task title: ")
            tm.add_task(title)
        elif choice == '3':
            try:
                index = int(input("Enter task number to mark as done: ")) - 1
                tm.mark_task_done(index)
            except ValueError:
                print(" Please enter a valid number.")
        elif choice == '4':
            try:
                index = int(input("Enter task number to delete: ")) - 1
                tm.delete_task(index)
            except ValueError:
                print(" Please enter a valid number.")
        elif choice == '5':
            print(" Exiting. Goodbye!")
            break
        else:
            print(" Invalid choice. Try again.")

if __name__ == "__main__":
    main()
