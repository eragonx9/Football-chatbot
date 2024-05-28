import requests

API_KEY = 'c3bcc6dfd7ab4abdb93a77855afaf705'

def fetch_data(endpoint):
    url = f'https://api.football-data.org/v4/{endpoint}'
    headers = {'X-Auth-Token': API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def fetch_todays_matches():
    return fetch_data('matches')

def fetch_champions_league_matches():
    return fetch_data('competitions/CL/matches')

def fetch_all_teams():
    return fetch_data('teams')

def fetch_leagues():
    competitions_data = fetch_data('competitions')
    competitions = competitions_data.get('competitions', [])
    competitions_text = "Available football competitions:\n"
    for competition in competitions:
        competition_name = competition.get('name', 'Unknown')
        area_name = competition.get('area', {}).get('name', 'Unknown')
        competition_code = competition.get('code', 'Unknown')
        competition_type = competition.get('type', 'Unknown')
       
        competitions_text += (
            f"- Name: {competition_name}\n"
            f"  Area: {area_name}\n"
            f"  Code: {competition_code}\n"
            f"  Type: {competition_type}\n"
        )
    return {'text': competitions_text}

def fetch_premier_league_winners():
    return fetch_data('competitions/PL')
