import requests
from bs4 import BeautifulSoup

def get_games(sport):
    nhl_schedule_url = f'https://streameast.top/{sport}/schedule'
    schedule_html = requests.get(nhl_schedule_url).content

    schedule = BeautifulSoup(schedule_html, 'html.parser')
    schedule_links = schedule.find_all('a', class_='competition')

    ret = []
    for l in schedule_links:
        ret.append( (l.get('title'), l.get('href')) )
    return ret

def get_streams(game):
    name = game[0]
    print(f"Looking for streams for : {name}")

    links = []

    try:
        game_html = requests.get(game[1]).content
        game = BeautifulSoup(game_html, 'html.parser')

        buttons = game.find_all('button')

        for b in buttons:
            link = b.get('datatype')
            if link is not None:
                links.append(link)

    except Exception as ex:
        print('    *** Error in get_stream')

    print(f'    Found {len(links)} streams')
    return links

def get_hrefs(sports = None):
    if sports is None:
        sports = ['nhl','nfl','nba','soccer', 'mlb']

    hrefs = []
    for s in sports:
        print(f'**** League {s} ****')
        for game in get_games(s):
            links = get_streams(game)
            if links is not None:
                hrefs.append( (s, game[0], links) )
        print('')

    return hrefs

def get_json_output(sports = None):
    import json
    hrefs = get_hrefs(sports)

    dd = []
    for h in hrefs:
        dd.append({'sport': h[0], 'game': h[1], 'stream': h[2]})

    return json.dumps(dd)


def get_html_output(sports = None):
    hrefs = get_hrefs(sports)
    if len(hrefs) > 0:
        with open('all.html', 'w') as f:
            f.write('<html><body style="font-size: 24px; font-family: sans-serif"><pre>')
            for s,n,ls in hrefs:
                try:
                    f.write(f""" <strong>{s}</strong> {n} """)
                    for i in range(len(ls)):
                        f.write(f"""<a href="{ls[i]}">Stream {i}</a>&#9;""")
                    f.write("""<br/><br/> """)
                except Exception as ex:
                    print(f"""Couldn't write {s} {n} to html output""")
            f.write('</pre></body></html>')