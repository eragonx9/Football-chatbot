import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from nltk.tokenize import word_tokenize

app = Flask(__name__)
CORS(app) 
API_KEY = 'c3bcc6dfd7ab4abdb93a77855afaf705'

# Function to tokenize and normalize user input
def tokenize(text):
    return word_tokenize(text.lower())

# Function to check if a certain keyword is present in user input
def check_keyword(text, keyword):
    return keyword in tokenize(text)

# Define function to fetch Champions League matches
def fetch_champions_league_matches():
    url = 'https://api.football-data.org/v4/competitions/CL/matches'
    headers = {'X-Auth-Token': API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

# Define function to fetch today's matches
def fetch_todays_matches():
    url = 'https://api.football-data.org/v4/matches'
    headers = {'X-Auth-Token': API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

# Define route for webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    query = data.get('query')
    response = handle_query(query)
    return jsonify(response)

# Function to handle user query
def handle_query(query):
    if check_keyword(query, 'premier league'):
        league_data = fetch_data('competitions/PL')
        return {'text': f"The Premier League has {league_data['numberOfTeams']} teams."}
    elif check_keyword(query, 'la liga'):
        league_data = fetch_data('competitions/PD')
        return {'text': f"La Liga has {league_data['numberOfTeams']} teams."}
    elif check_keyword(query, 'today matches'):
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
    elif check_keyword(query, 'champions league'):
        try:
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
        except Exception as e:
            return {'text': f"Error processing Champions League matches: {str(e)}"}
    else:
        return {'text': "I didn't understand your query. Please ask about a specific league or team."}

if __name__ == '__main__':
    app.run(debug=True)
