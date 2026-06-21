# -*- coding: utf-8 -*-
# ==============================================================================
# PROPRIETARY AND CONFIDENTIAL - CITIZEN CFO™
# COPYRIGHT © 2026 CHRISTOPHER. ALL RIGHTS RESERVED.
# ==============================================================================
import os
import json
import time
import shutil
import csv
import logging

PROJECT_DIR = os.path.expanduser("~/cfo_project")
BACKUP_DIR = os.path.join(PROJECT_DIR, "vault_backups")
DB_FILE = os.path.join(PROJECT_DIR, "foreseen_vault.json")
CONFIG_FILE = os.path.join(PROJECT_DIR, "market_config.json")
EXPORT_FILE = os.path.join(PROJECT_DIR, "citizen_cfo_ledger_export.csv")
LOG_FILE = os.path.join(PROJECT_DIR, "cfo_system.log")

# Setup logging for background operational monitoring
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DEFAULT_MATRIX = {
    "inventory_and_materials": {"predicted_90d_shift": 4.2, "volatility_index": "MEDIUM", "weight": 0.40},
    "logistics_and_shipping": {"predicted_90d_shift": 7.8, "volatility_index": "HIGH", "weight": 0.20},
    "fixed_overhead_buffer": {"predicted_90d_shift": 1.1, "volatility_index": "LOW", "weight": 0.40}
}

MARKET_RISK_MATRIX = {}

def verify_secure_environment():
    for path in [PROJECT_DIR, BACKUP_DIR]:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            os.chmod(path, 0o700)

def load_market_config():
    global MARKET_RISK_MATRIX
    verify_secure_environment()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                MARKET_RISK_MATRIX = json.load(f)
                return
        except Exception: pass
    MARKET_RISK_MATRIX = DEFAULT_MATRIX.copy()

def get_clean_float(prompt_text):
    while True:
        raw = input(prompt_text).strip().replace('$', '').replace(',', '')
        try:
            return float(raw)
        except ValueError:
            print("[!] Invalid input. Please enter a valid number.")

def save_financial_snapshot(payload_type, data, tactical_insights):
    vault = []
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                vault = json.load(f)
        except Exception: pass
    
    vault.append({
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "type": payload_type,
        "metrics": data,
        "audited_strategic_moves": tactical_insights
    })
    
    with open(DB_FILE, "w") as f:
        json.dump(vault, f, indent=4)
    os.chmod(DB_FILE, 0o600)
    logging.info(f"Financial record vaulted: {payload_type}")

def calculate_forecast():
    print("\n--- RUNWAY FORECAST ENGINE ---")
    revenue = get_clean_float("Enter projected gross revenue ($): ")
    reserves = get_clean_float("Enter liquid reserves ($): ")
    
    total_shift = sum(d['predicted_90d_shift'] * d['weight'] for d in MARKET_RISK_MATRIX.values())
    adjusted_opex = (revenue * 0.36) * (1 + (total_shift / 100))
    net_profit = revenue - adjusted_opex - (revenue * 0.15)
    runway = reserves / adjusted_opex if adjusted_opex > 0 else 99.9
    
    print(f"\n[+] Runway: {runway:.2f} Months | Net Profit: ${net_profit:,.2f}")
    save_financial_snapshot("Tax & Runway Analysis", {"revenue": revenue, "runway": runway}, ["Analysis complete."])

def main_menu():
    load_market_config()
    while True:
        print("\n=== CITIZEN CFO™ SECURED DASHBOARD ===")
        print("1. Run Forecast\n2. View Ledger\n3. Exit")
        choice = input("Select (1-3): ").strip()
        if choice == "1": calculate_forecast()
        elif choice == "2": print("Accessing vault records...")
        elif choice == "3": break
        else: print("[!] Invalid selection.")

if __name__ == "__main__":
    main_menu()