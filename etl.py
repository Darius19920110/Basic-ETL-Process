from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime

def extract():
    players = []

    page = requests.get("https://www.spotrac.com/epl/rankings/weekly/")
    html = page.text # Get the content of the webpage
    soup = BeautifulSoup(html, "html.parser") # Convert that into a BeautifulSoup object that contains methods to make the tag search easier

    table = soup.find_all("tr")

    for i,row in enumerate(table):
        if i == 0:
            continue

        column = row.find_all("td")
        player_container = column[1]
        player = player_container.find(name="h3").text
        team = column[2].text
        salary = column[3].text

        players.append({"Rank": i, "Player": player, "Team": team, "Weekly Salary": salary})

    extracted_data = pd.DataFrame(players)

    return extracted_data 

extracted_data = extract()