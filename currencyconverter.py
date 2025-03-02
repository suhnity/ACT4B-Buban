import csv
import os

CSV_URL = "https://raw.githubusercontent.com/valeriecmcho/IT0011-Activity/main/currency.csv"

def download_csv(filename):
    """Downloads the CSV file if it doesn't exist."""
    print("Downloading currency exchange rates...")
    try:
        response = requests.get(CSV_URL)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        with open(filename, "wb") as file:
            file.write(response.content)
        print("Download complete.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")
        exit(1)

def load_exchange_rates(filename):
    """Load currency exchange rates from a CSV file into a dictionary."""
    rates = {}

    # If the file doesn't exist, download it
    if not os.path.exists(filename):
        download_csv(filename)

    with open(filename, newline='', encoding="ISO-8859-1") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) < 3:
                continue  # Skip invalid rows
            currency = row[0].strip().upper()  # Extract currency code (first column)
            try:
                rate = float(row[2].strip())  # Extract exchange rate (third column)
                rates[currency] = rate
            except ValueError:
                continue  # Skip invalid data
    return rates

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script directory
    filename = os.path.join(script_dir, "currency.csv")  # Full path to CSV
    rates = load_exchange_rates(filename)

    try:
        dollars = float(input("How much dollar do you have? "))
    except ValueError:
        print("Please enter a valid number for dollars.")
        return

    target_currency = input("What currency you want to have? ").strip().upper()

    if target_currency not in rates:
        print(f"Currency '{target_currency}' not found in the exchange rate file.")
        return

    converted_amount = dollars * rates[target_currency]

    print(f"\nDollar: {dollars} USD")
    print(f"{target_currency}: {converted_amount}")

if __name__ == '__main__':
    main()