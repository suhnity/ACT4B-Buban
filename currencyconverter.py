import csv
import os
import requests

CSV_URL = "https://raw.githubusercontent.com/suhnity/main/ACT4B-Buban/currency.csv"

def download_csv(filename):
    """Downloads the CSV file if it doesn't exist."""
    print("Downloading currency exchange rates...")
    try:
        response = requests.get(CSV_URL)
        response.raise_for_status()
        with open(filename, "wb") as file:
            file.write(response.content)
        print("Download complete.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")
        exit(1)

def load_currency_rates(filename):
    """Load currency exchange rates from a CSV file into a dictionary."""
    rates = {}
    
    if not os.path.exists(filename):
        download_csv(filename)
    
    with open(filename, newline='', encoding="ISO-8859-1") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if len(row) < 3:
                continue
            currency = row[0].strip().upper()
            try:
                rate = float(row[2].strip())
                rates[currency] = rate
            except ValueError:
                continue
    return rates

def convert_currency(amount, currency, rates):
    """Convert USD to the target currency using exchange rates."""
    return amount * rates.get(currency, 0)

def main():
    filename = "currency.csv"
    rates = load_currency_rates(filename)
    
    try:
        amount = float(input("How much dollar do you have? "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return
    
    currency = input("What currency you want to have? ").strip().upper()
    
    if currency not in rates:
        print(f"Currency '{currency}' not found in the exchange rates.")
        return
    
    converted_amount = convert_currency(amount, currency, rates)
    
    print(f"\nDollar: {amount} USD")
    print(f"{currency}: {converted_amount:.6f}")

if __name__ == "__main__":
    main()
