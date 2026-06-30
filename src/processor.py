import pandas as pd

def load_financial_data(file_path):
    return pd.read_csv(file_path)

def main_menu():
    while True:
        print("\n--- CITIZEN CFO DASHBOARD ---")
        print("1. View Dashboard Summary")
        print("2. Show High-Risk Actions")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ")
        
        try:
            df = load_financial_data('citizen_cfo_ledger_export.csv')
            
            if choice == '1':
                print(f"\nTotal Entries in Ledger: {len(df)}")
            elif choice == '2':
                high_risk = df[df['Audited Strategic Actions'].str.contains('HIGH RISK', na=False)]
                print("\n--- HIGH RISK ACTIONS ---")
                print(high_risk)
            elif choice == '3':
                print("Exiting Dashboard.")
                break
            else:
                print("Invalid choice, please try again.")
        except Exception as e:
            print(f"Error reading data: {e}")

if __name__ == "__main__":
    main_menu()
