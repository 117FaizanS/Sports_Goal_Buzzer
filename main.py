from flask import Flask, request
import requests
from datetime import date

app = Flask(__name__)
last_scores = {}

'''
@app.route("/score")
def get_score():
    today = date.today().strftime("%Y-%m-%d")

    team = request.args.get("team", "Florida Panthers")
    url = f"https://api-web.nhle.com/v1/score/{today}"

    r = requests.get(url)
    data = r.json()

    for game in data.get("games", []):
        home_team = game["homeTeam"]["name"]["default"]
        away_team = game["awayTeam"]["name"]["default"]
        home_score = game["homeTeam"]["score"]
        away_score = game["awayTeam"]["score"]

        if team == home_team:
            key = f"{team}-home"
            last = last_scores.get(key, -1)
            last_scores[key] = home_score
            if home_score > last:
                return "HOME_GOAL"
            return "NO_GOAL"

        elif team == away_team:
            key = f"{team}-away"
            last = last_scores.get(key, -1)
            last_scores[key] = away_score
            if away_score > last:
                return "AWAY_GOAL"
            return "NO_GOAL"

    return "NO_GAME"

app.run(host="0.0.0.0", port=5000)'''
































'''
@app.route("/score")
def get_score():
    team = request.args.get("team", "Florida Panthers")
    url = "https://api-web.nhle.com/v1/score/2025-05-30"  # Static date for now

    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        return f"ERROR: {str(e)}"

    for game in data.get("games", []):
        home_team = game["homeTeam"]["name"]["default"]
        away_team = game["awayTeam"]["name"]["default"]
        home_score = game["homeTeam"]["score"]
        away_score = game["awayTeam"]["score"]

        # If your team is the home team
        if team == home_team:
            key = f"{team}-home"
            last = last_scores.get(key, -1)
            last_scores[key] = home_score
            if home_score > last:
                return "HOME_GOAL"
            return "NO_GOAL"

        # If your team is the away team
        elif team == away_team:
            key = f"{team}-away"
            last = last_scores.get(key, -1)
            last_scores[key] = away_score
            if away_score > last:
                return "AWAY_GOAL"
            return "NO_GOAL"

    return "NO_GAME"

if __name__ == "__main__":
    # Run locally at http://127.0.0.1:5000
    app.run(host="127.0.0.1", port=5000, debug=True)'''





























import requests

# Set the team you're tracking
team_to_track = "Panthers"

# Use today's date (or change it manually)
from datetime import date
#today = date.today().strftime("%Y-%m-%d")
today = "2025-05-28"

# NHL API endpoint
url = f"https://api-web.nhle.com/v1/score/{today}"

try:
    response = requests.get(url)
    data = response.json()
except Exception as e:
    print(f"Failed to fetch data: {e}")
    exit()

# Search through the games to find the team
for game in data.get("games", []):
    home_team = game["homeTeam"]["name"]["default"]
    away_team = game["awayTeam"]["name"]["default"]
    home_score = game["homeTeam"]["score"]
    away_score = game["awayTeam"]["score"]

    if team_to_track in [home_team, away_team]:
        print(f"\n🏒 {away_team} @ {home_team}")
        print(f"📊 Score: {away_score} - {home_score}")

        if team_to_track == home_team:
            print(f"✅ {team_to_track} is HOME: {home_score} goals")
        else:
            print(f"✅ {team_to_track} is AWAY: {away_score} goals")
        break
else:
    print(f"No game found for {team_to_track} on {today}")
