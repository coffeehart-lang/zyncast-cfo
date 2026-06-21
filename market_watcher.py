import os
import json
import time

PROJECT_DIR = os.path.expanduser("~/cfo_project")
DB_FILE = os.path.join(PROJECT_DIR, "foreseen_vault.json")
CONFIG_FILE = os.path.join(PROJECT_DIR, "market_config.json")

DEFAULT_MATRIX = {
    "inventory_and_materials": {"predicted_90d_shift": 4.2, "volatility_index": "MEDIUM", "weight": 0.40},
    "logistics_and_shipping": {"predicted_90d_shift": 7.8, "volatility_index": "HIGH", "weight": 0.20},
    "fixed_overhead_buffer": {"predicted_90d_shift": 1.1, "volatility_index": "LOW", "weight": 0.40}
}

MARKET_RISK_MATRIX = {}

def load_market_config():
    global MARKET_RISK_MATRIX
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                MARKET_RISK_MATRIX = json.load(f)
            return
        except Exception:
            pass
    MARKET_RISK_MATRIX = json.loads(json.dumps(DEFAULT_MATRIX))

def save_market_config():
    try:
        if not os.path.exists(PROJECT_DIR):
            os.makedirs(PROJECT_DIR)
        with open(CONFIG_FILE, "w") as f:
            json.dump(MARKET_RISK_MATRIX, f, indent=4)
    except Exception as e:
        print(f"[!] Error saving persistent market config: {e}")

def get_clean_float(prompt_text):
    while True:
        try:
            raw = input(prompt_text).strip().replace('$', '').replace(',', '')
            return float(raw)
        except ValueError:
            print("[!] Error: Please enter a valid number (numbers and decimals only).")

def save_financial_snapshot(payload_type, data):
    if not os.path.exists(PROJECT_DIR):
        os.makedirs(PROJECT_DIR)
        
    vault = []
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                vault = json.load(f)
        except Exception:
            vault = []
            
    snapshot = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "analytics_type": payload_type,
        "metrics": data
    }
    vault.append(snapshot)
    
    with open(DB_FILE, "w") as f:
        json.dump(vault, f, indent=4)
    print("[+] Financial snapshot secured to private hardware ledger vault.")

def run_tax_and_runway_forecast():
    print("\n=========================================")
    print("  MODULE: TAX LIABILITY & RUNWAY ENGINE  ")
    print("=========================================")
    
    gross_revenue = get_clean_float("Enter projected gross business revenue ($): ")
    baseline_opex = get_clean_float("Enter current baseline costs / books ($): ")
    tax_rate = get_clean_float("Enter business tax bracket % (e.g., 15, 21, 25): ") / 100

    weighted_market_inflation = 0.0
    for metrics in MARKET_RISK_MATRIX.values():
        weighted_market_inflation += (metrics["predicted_90d_shift"] / 100) * metrics["weight"]

    adjusted_opex = baseline_opex * (1 + weighted_market_inflation)
    projected_pretax_net = gross_revenue - adjusted_opex

    if projected_pretax_net > 0:
        estimated_tax_provision = projected_pretax_net * tax_rate
        retained_net_profit = projected_pretax_net - estimated_tax_provision
    else:
        estimated_tax_provision = 0.0
        retained_net_profit = projected_pretax_net

    print("\n--- BASELINE FORECAST RESULTS ---")
    print(f"Total Market Inflation Loading Factor: {weighted_market_inflation*100:.2f}%")
    print(f"Market-Adjusted Expenses (Monthly): ${adjusted_opex:,.2f}")
    print(f"Projected Pre-Tax Net: ${projected_pretax_net:,.2f}")
    print(f"Estimated Tax Provision: ${estimated_tax_provision:,.2f}")
    print(f"Retained Net Profit: ${retained_net_profit:,.2f}")
    
    print("\n--- RUNWAY CALCULATOR ENGINE ---")
    current_cash = get_clean_float("Enter current business cash reserves/savings ($): ")
    
    if adjusted_opex > 0:
        runway_months = current_cash / adjusted_opex
    else:
        runway_months = float('inf')
        
    print(f"\n[>] Safe Capital Runway: {runway_months:.1f} Months")
    if runway_months < 3.0:
        print("[!] WARNING: Runway is under the standard 3-month safety threshold.")
    elif runway_months >= 6.0:
        print("[+] STABILITY ALERT: Excellent cash-to-expense runway security.")

    save_choice = input("\nSecure this runway forecast to the private ledger vault? (y/n): ").strip().lower()
    if save_choice == 'y':
        payload = {
            "gross_revenue": gross_revenue,
            "baseline_expenses": baseline_opex,
            "adjusted_expenses": adjusted_opex,
            "tax_liability": estimated_tax_provision,
            "net_retained_profit": retained_net_profit,
            "cash_reserves": current_cash,
            "runway_months": round(runway_months, 2)
        }
        save_financial_snapshot("Tax & Runway Analysis", payload)

def view_and_adjust_volatility_indexes():
    while True:
        print("\n=========================================")
        print("   MARKET STRESS-TESTING INTERFACE       ")
        print("=========================================")
        keys = list(MARKET_RISK_MATRIX.keys())
        
        for idx, key in enumerate(keys, 1):
            values = MARKET_RISK_MATRIX[key]
            print(f"{idx}. {key.replace('_', ' ').title()}")
            print(f"   Current Expected Shift: {values['predicted_90d_shift']}% | Profile: {values['volatility_index']}")
        print(f"{len(keys) + 1}. Return to Main Dashboard Menu")
        print("=========================================")
        
        choice = input("Select a market sector to adjust (or exit): ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(keys):
            target_key = keys[int(choice) - 1]
            print(f"\n[>] Adjusting Live Shift Profile for {target_key.replace('_', ' ').title()}")
            new_shift = get_clean_float("Enter updated 90-day predicted shift percentage (%): ")
            
            MARKET_RISK_MATRIX[target_key]["predicted_90d_shift"] = new_shift
            if new_shift >= 10.0:
                MARKET_RISK_MATRIX[target_key]["volatility_index"] = "CRITICAL"
            elif new_shift >= 6.0:
                MARKET_RISK_MATRIX[target_key]["volatility_index"] = "HIGH"
            elif new_shift >= 3.0:
                MARKET_RISK_MATRIX[target_key]["volatility_index"] = "MEDIUM"
            else:
                MARKET_RISK_MATRIX[target_key]["volatility_index"] = "LOW"
                
            save_market_config()
            print("[+] Live market configuration scaled and saved to hardware disk.")
        elif choice == str(len(keys) + 1):
            break
        else:
            print("[!] System selection out of bounds.")

def access_vaulted_history():
    print("\n==========================================================================================")
    print("                      CITIZEN CFO™ PRIVATE FINANCIAL LEDGER RECONCILIATION                ")
    print("==========================================================================================")
    if not os.path.exists(DB_FILE):
        print("[!] Secure ledger disk is empty. No records found.")
        return
        
    try:
        with open(DB_FILE, "r") as f:
            vault = json.load(f)
        
        header_format = "{:<20} | {:<12} | {:<12} | {:<12} | {:<12} | {:<8}"
        row_format =    "{:<20} | ${:<11,.2f} | ${:<11,.2f} | ${:<11,.2f} | ${:<11,.2f} | {:<8}"
        
        print(header_format.format("Timestamp", "Revenue", "Adjusted Exp", "Tax Prov.", "Net Profit", "Runway"))
        print("-" * 90)
        
        for record in vault:
            ts = record.get('timestamp', 'N/A')
            m = record.get('metrics', {})
            
            rev = m.get('gross_revenue', 0.0)
            exp = m.get('adjusted_expenses', 0.0)
            tax = m.get('tax_liability', 0.0)
            net = m.get('net_retained_profit', 0.0)
            runway = f"{m.get('runway_months', 'N/A')} Mo" if 'runway_months' in m else "N/A"
            
            print(row_format.format(ts, rev, exp, tax, net, runway))
        print("==========================================================================================")
        
    except Exception as e:
        print(f"[!] Error reading secure ledger disk: {e}")

def main_menu():
    load_market_config()
    while True:
        print("\n=========================================")
        print("     CITIZEN CFO™ FINANCIAL DASHBOARD    ")
        print("=========================================")
        print("1. Run Tax Liability & Net Runway Forecast")
        print("2. Adjust Market Volatility Stress Profiles")
        print("3. Access Vaulted Bookkeeping Ledger History")
        print("4. Exit System")
        print("=========================================")
        
        choice = input("Select operation (1-4): ").strip()
        if choice == '1':
            run_tax_and_runway_forecast()
        elif choice == '2':
            view_and_adjust_volatility_indexes()
        elif choice == '3':
            access_vaulted_history()
        elif choice == '4':
            print("\n[!] Disconnecting from corporate data vault. Safe logout.")
            break
        else:
            print("\n[!] Invalid system option choice.")

if __name__ == "__main__":
    main_menu()
