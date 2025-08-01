from datetime import datetime
import json, os, pathlib
from flask import render_template
from HelloFlask import app

@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    return render_template(
        "index.html",
        title = "Team Friends Fantasy Football",
        message = "Hello, Flask!",
        content = " on " + formatted_now)

@app.route('/2025')
def home2025():
    return render_template(
        "2025home.html",
        title = "Team Friends 2025")

@app.route('/docs/rules')
def get_rules():
    return app.send_static_file('TeamFriendsRules.pdf')


@app.route('/history')
def history():
    ##########################
    # Regular Season History #
    ##########################
    #get Regular Season History from file
    regSeason = 'regSeasonHistory.json'
    currDir = pathlib.Path(__file__).parent.resolve()
    with open(os.path.join(currDir,"data",regSeason), 'r') as f:
        dictRegSeason = json.load(f)
        
    
    
    for team in dictRegSeason['teams']:
        #calculate win pct
        total = team['wins'] + team['losses']
        team['winPct'] = round(team['wins'] / total,3)

        #caluclate number of seasons
        currYr = 2025
        team['numSeasons'] = currYr - team['startYear']
        
        team['pngWins'] = f"/static/{team['owner']}_wins.png"

    return render_template(
        "history.html",
        teams = dictRegSeason['teams'])