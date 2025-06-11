import requests
import time
from datetime import date
import pyfirmata2

# Python Configuration
board = pyfirmata2.Arduino('COM7')
LED_pin = board.get_pin('a:8:o')

# 🧾 Configuration
team_to_track = "Edmonton Oilers"
check_interval = 5  # seconds
today = date.today().strftime("%Y-%m-%d")

# Step 1: Get today's scheduled games
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

# Step 2: Find your team's game
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

# Step 3: Real-time loop
box_url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/boxscore"

print("\n🔁 Starting live score tracking...\n")

last_home_score = -1
last_away_score = -1

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

            # 👉 Trigger event (e.g., light/LED) when your team scores here
            for i in range(10): # Loop to blink the micro-led
                LED_pin.write(255) # Turn on the led
                time.sleep(1) # Delay
                LED_pin.write(0) # Turn off the led
                time.sleep(1) # Delay

            last_home_score = home_score
            last_away_score = away_score

        time.sleep(check_interval)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(check_interval)