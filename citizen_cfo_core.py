# --- Define Forecast Logic ---
def calculate_forecast():
    print("\n[+] Running Forecast...")
    # Add your specific forecast logic here
    print("[+] Forecast complete.")

# --- Define Dashboard Menu ---
def main_menu():
    while True:
        print("\nCITIZEN CFO SECURED DASHBOARD")
        print("1. Run Forecast")
        print("3. Exit")
        
        choice = input("Select (1-3): ")
        
        if choice == '1':
            calculate_forecast()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

# --- Entry Point ---
if __name__ == "__main__":
    main_menu()