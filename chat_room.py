import getpass

def chat_room():
    """Simulates a general chat room."""
    print("\n--- Welcome to the General Chat Room ---")
    print("Type 'menu' to return to the main menu.")
    while True:
        message = input("Chat > ")
        if message.lower() == 'menu':
            break
        print(f"   -> {message}")

def counselor_section():
    """Simulates a private counselor section."""
    print("\n--- Welcome to the Counselor Section ---")
    print("This is a private and secure space. Type 'menu' to return.")
    while True:
        message = input("Counselor > ")
        if message.lower() == 'menu':
            break
        print(f"   -> {message}")

def desk_help():
    """Simulates a desk help section."""
    print("\n--- Welcome to Desk Help ---")
    print("How can we assist you? Type 'menu' to return.")
    while True:
        message = input("Help > ")
        if message.lower() == 'menu':
            break
        print(f"   -> {message}")

def main():
    """Main function to run the chat application."""
    correct_password = "dido7return"
    
    # Using getpass to hide the password input
    password = getpass.getpass("Enter password to access the chat service: ")

    if password != correct_password:
        print("Incorrect password. Access denied.")
        return

    print("\nPassword accepted. Welcome!")

    while True:
        print("\n--- Main Menu ---")
        print("1. General Chat Room")
        print("2. Counselor Section")
        print("3. Desk Help")
        print("4. Exit")

        choice = input("Select an option (1-4): ")

        if choice == '1':
            chat_room()
        elif choice == '2':
            counselor_section()
        elif choice == '3':
            desk_help()
        elif choice == '4':
            print("Thank you for using the chat service. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number between 1 and 4.")

if __name__ == "__main__":
    main()

