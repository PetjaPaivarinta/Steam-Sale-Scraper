import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import csv

url = 'https://store.steampowered.com/search/results/?query&start=0&count=100&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&specials=1&infinite=1'

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
            # Write the header row
            writer.writerow(['Title', 'Original Price', 'Discounted Price', 'Release Date', 'Discount Amount'])
            # Write all the game data rows
            writer.writerows(game_data)

        print("Succesfully printed")

data = get_data(url)
parse(data)