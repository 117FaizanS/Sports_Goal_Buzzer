import requests
import time
from datetime import date
import pyfirmata2

# Python Config
# TODO add speaker config for goal horns
board = pyfirmata2.Arduino('COM7')
LED_pin = board.get_pin('a:8:o')

# Team selection
team_to_track = "Edmonton Oilers"
check_interval = 5  # seconds
today = date.today().strftime("%Y-%m-%d")

# Get today's scheduled games
schedule_url = f"https://api-web.nhle.com/v1/schedule/{today}"
resp = requests.get(schedule_url)

if resp.status_code != 200:
    print("Error fetching schedule.")
    exit()

# Find today's games
games = []
for day in resp.json().get("gameWeek", []):
    if day["date"] == today:
        games = day["games"]
        break

# Find selected team's game
game_id = None
for game in games:
    home = game["homeTeam"]["placeName"]["default"] + " " + game["homeTeam"]["commonName"]["default"]
    away = game["awayTeam"]["placeName"]["default"] + " " + game["awayTeam"]["commonName"]["default"]

    print(f"{away} @ {home}")

    if team_to_track in [home, away]:
        game_id = game["id"]
        print(f"✅ Found game ID: {game_id}")
        break

if not game_id:
    print("❌ No game found for your team today.")
    exit()

# Loop continuously to update scores
box_url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/boxscore"

print("\n🔁 Starting live score tracking...\n")

last_home_score = -1
last_away_score = -1

# Loop continuously to check scores and trigger buzzer
while True:
    try:
        box_resp = requests.get(box_url)
        if box_resp.status_code != 200:
            print("Failed to fetch game data. Retrying...")
            time.sleep(check_interval)
            continue

        box = box_resp.json()

        game_state = box.get("gameState", "UNKNOWN")
        home_team = box["homeTeam"]["commonName"]["default"]
        away_team = box["awayTeam"]["commonName"]["default"]
        home_score = box["homeTeam"]["score"]
        away_score = box["awayTeam"]["score"]
        

        print(f"🕒 {time.strftime('%H:%M:%S')} | {away_team} @ {home_team} ({game_state})")
        print(f"📢 {away_team} @ {home_team} | {game_state}")
        print(f"📊 Score: {away_score} - {home_score}\n")

        if home_score != last_home_score or away_score != last_away_score:
            print(f"📢 {away_team} @ {home_team} | {game_state}")
            print(f"📊 Score: {away_score} - {home_score}\n")

            # Arduino triggers for goal
            # TODO make a function?
            for i in range(6):
                LED_pin.write(255)
                time.sleep(0.5)
                LED_pin.write(0)
                time.sleep(0.5)

            # Update Scores
            last_home_score = home_score
            last_away_score = away_score

        time.sleep(check_interval)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(check_interval)