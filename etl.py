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

def transform(data):
    # Transform weekly salary -> convert to int
    for i in data["Weekly Salary"]:
        amount_string = i.split("£")[1]
        amount_string = amount_string.split(",")
        amount = int(amount_string[0] + amount_string[1])

        data["Weekly Salary"] = data["Weekly Salary"].replace([i], amount)

    data.rename(columns = {"Weekly Salary": "Weekly Salary (GBP)"}, inplace = True)

    return data

def load(data):
    data.to_csv("top_players_salary.csv", index=False)

def log(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second
    now = datetime.now() # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open("logfile.txt","a") as f:
        f.write(timestamp + ',' + message + '\n')

log("ETL Job Started")
log("Extract phase Started")
extracted_data = extract()
log("Extract phase Ended")
log("Transform phase Started")
transformed_data = transform(extracted_data)
log("Transform phase Ended")
log("Load phase Started")
load(transformed_data)
log("Load phase Ended")
log("ETL Job Ended")

