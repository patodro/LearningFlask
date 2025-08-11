from datetime import datetime
import json, os, pathlib
from flask import render_template
from HelloFlask import app

def calc_win_pct(wins,losses):
    total = wins + losses
    if total==0: return 0
    return round(wins / total, 3)

def calc_num_seasons(startYear,status):
    currYr = 2025
    if status == "active":
        return currYr - startYear
    elif status.startswith(("inactive-")):
        deadYr = int(status.split('-')[-1])
        return deadYr - startYear

def calc_champ_score(firsts,seconds,thirds,numSeasons):
    frScore = firsts * 3
    scScore = seconds * 2
    thScore = thirds * 1
    total = frScore+scScore+thScore
    if numSeasons != 0:
        return round(total / numSeasons,2)
    else:
        return 0

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
        team['winPct'] = calc_win_pct(team['wins'],team['losses'])

        #caluclate number of seasons
        team['numSeasons'] = calc_num_seasons(team['startYear'],team['status'])
        
        team['pngWins'] = f"/static/{team['owner']}_wins.png"
        
    ###########################
    ##### Playoff History #####
    ###########################
    playoffHist = 'playoffResults.json'
    with open(os.path.join(currDir,"data",playoffHist), 'r') as f:
        dictPlayoff = json.load(f)

    #######################
    ##### Champ Score #####
    #######################
    champHist = 'champHistory.json'
    with open(os.path.join(currDir,"data",champHist), 'r') as f:
        dictChamp = json.load(f)

    for team in dictChamp['teams']:
        #calculate number of seasons
        team['numSeasons'] = calc_num_seasons(team['startYear'],team['status'])

        #calculate champ score
        team['score'] = calc_champ_score(team['firsts'],team['seconds'],team['thirds'],team['numSeasons'])
    #sort dict by Champ Score
    dictChamp['teams'] = sorted(dictChamp['teams'], key=lambda x: float(x['score']), reverse=True)

    return render_template(
        "history.html",
        teams = dictRegSeason['teams'],
        results = dictPlayoff['results'],
        champs = dictChamp['teams'])