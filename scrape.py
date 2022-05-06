import json
import statsapi
import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparse

def schedule():
    """Scrape schedules from Baseball Reference."""
    # Get the page
    url = "https://www.baseball-reference.com/teams/TOR/2022-schedule-scores.shtml"
    r = requests.get(url)

    # Parse it
    soup = BeautifulSoup(r.text, "html5lib")

    # Grab the table
    table = soup.find("table", class_="stats_table")

    # Loop through each row
    row_list = []
    for row in table.find_all("tr")[1:-1]:
        d = {}
        # Get the cells
        cell_list = row.find_all(['td', 'th'])

        # Skip the cruft rows
        if cell_list[0].text == "Gm#":
            continue

        # Pull the data
        for cell in cell_list:
            d[cell.attrs['data-stat']] = cell.text

        # Parse the dates
        d['date'] = dateparse.parse(d['date_game'] + " 2022")

        # Add them to the list
        row_list.append(d)

    # Write it out
    with open("./data/schedule.json", "w") as fp:
        json.dump(row_list, fp, indent=2, sort_keys=True, default=str)

schedule()


		