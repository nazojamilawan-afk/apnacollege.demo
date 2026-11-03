
def register():
    username = input("Enter username: ")
    password = input("Enter password: ")

    with open("users.txt", "a") as file:
        file.write(username + "," + password + "\n")

    print("Registration successful!")


def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        with open("users.txt", "r") as file:
            for line in file:
                saved_username, saved_password = line.strip().split(",")

                if username == saved_username and password == saved_password:
                    print("Login successful!")
                    return

        print("Invalid username or password.")

    except FileNotFoundError:
        print("No users registered yet.")


while True:
    print("\n===== LOGIN SYSTEM =====")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        register()

    elif choice == "2":
        login()

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice!")
