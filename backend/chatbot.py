from flask import Flask, request, jsonify
from flask_cors import CORS
from api_calls import fetch_todays_matches, fetch_champions_league_matches, fetch_leagues, fetch_premier_league_winners

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

@app.route('/handle_webhook', methods=['POST'])
def handle_webhook():
    data = request.get_json()
    query = data.get('query')
    response = handle_query(query)
    return jsonify(response)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    query = data.get('query')
    response = handle_query(query)
    return jsonify(response)

def handle_query(query):
    if "today's matches" in query.lower():
        matches_data = fetch_todays_matches()
        matches = matches_data.get('matches', [])
        if not matches:
            return {'text': "There are no matches scheduled for today."}
        
        matches_text = "Today's matches:\n"
        for match in matches:
            competition = match['competition']['name']
            home_team = match['homeTeam']['name']
            away_team = match['awayTeam']['name']
            matches_text += f"{competition}: {home_team} vs {away_team}\n"
        return {'text': matches_text}
    elif 'Champions League' in query:
        matches_data = fetch_champions_league_matches()
        matches = matches_data.get('matches', [])
        if not matches:
            return {'text': "There are no Champions League matches scheduled."}
        
        matches_text = "Champions League matches:\n"
        for match in matches:
            home_team = match['homeTeam']['name']
            away_team = match['awayTeam']['name']
            utc_date = match['utcDate']
            matches_text += f"{home_team} vs {away_team} on {utc_date}\n"
        return {'text': matches_text}
    elif 'premier league winners' in query.lower():
        winners_data = fetch_premier_league_winners()
        seasons = winners_data.get('seasons', [])
        if not seasons:
            return {'text': "No data available for Premier League winners."}

        winners_text = "Premier League winners in recent seasons:\n"
        for season in seasons:
            if 'winner' in season and season['winner']:
                winner = season['winner']['name']
                start_date = season['startDate']
                end_date = season['endDate']
                winners_text += f"Season {start_date} to {end_date}: {winner}\n"
        return {'text': winners_text}
    elif 'different leagues' in query.lower():
        return fetch_leagues()
        
    else:
        return {'text': "I didn't understand your query. Please ask about a specific league or team."}

if __name__ == '__main__':
    app.run(debug=True)
