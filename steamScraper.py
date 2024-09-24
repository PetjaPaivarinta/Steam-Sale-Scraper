import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import csv
import tkinter as tk
from tkinter import ttk
import os

url = 'https://store.steampowered.com/search/results/?query&start=0&count=300&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&specials=1&infinite=1'

def get_data(url):
    r = requests.get(url)
    data = dict(r.json())
    return data['results_html']

def parse(data):

    game_data = []
    soup = BeautifulSoup(data, 'html.parser')
    games = soup.find_all('a')
    for game in games:
        title = game.find('span', {'class': 'title'}).text
        price_container = game.find('div', {'class': 'search_price_discount_combined'}).text.strip()
        discount_amount = "No discount"
        discounted_price = None
        original_price = None
        if '%' in price_container:
            discount_amount = price_container.split('%')[0].strip() + "%"

            prices = price_container.split('€')
            if len(prices) >= 2:
                original_price = prices[0].split('%')[-1].strip() + "€"  # After discount percentage
                discounted_price = prices[1].strip() + "€"  # Final discounted price
        else:
            original_price = price_container

        release_date = game.find('div', {'class': 'search_released'}).text.strip()
        game_data.append([title, original_price, discounted_price, release_date, discount_amount])

        with open('games_data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write all the game data rows
            writer.writerows(game_data)

def load_csv_data():
    if os.path.exists('games_data.csv'):
        with open("games_data.csv", "r", newline="", encoding='utf-8') as passfile:
            reader = csv.reader(passfile)
            for row in reader:
                tree.insert("", tk.END, values=row)

passScreen = tk.Tk()
passScreen.geometry("1200x800")
passScreen.title("Games")

# Create a frame for the Treeview widget
frame = tk.Frame(passScreen)
frame.pack(fill=tk.BOTH, expand=True)

# Set up the Treeview widget
tree = ttk.Treeview(frame, columns=("Title", "Original Price", "Discounted Price", "Release Date", "Discount Percentage"), show='headings')
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Define column headings
tree.heading("Title", text="Title")
tree.heading("Original Price", text="Original Price")
tree.heading("Discounted Price", text="Discounted Price")
tree.heading("Release Date", text="Release Date")
tree.heading("Discount Percentage", text="Discount Percentage")

# Set column widths
tree.column("Title", width=300)
tree.column("Original Price", width=150)
tree.column("Discounted Price", width=150)
tree.column("Release Date", width=150)
tree.column("Discount Percentage", width=150)

# Add a scrollbar to the Treeview widget
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

if not os.path.exists("games_data.csv"):
    print("File not found. Fetching data...")
    data = get_data(url)
    parse(data)
else:
    print("File found. Loading data...")

load_csv_data()

passScreen.mainloop()

data = get_data(url)
parse(data)