import os
import json
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

requests.packages.urllib3.disable_warnings()

headers = {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://tounesbet.com",
    "Connection": "keep-alive",
    "Referer": "https://tounesbet.com/?d=1",
    "Cookie": 
    "_culture=fr-fr; _ga_PGQGW1WPHH=GS1.1.1686663687.6.0.1686663687.0.0.0; _ga=GA1.2.947079087.1686555229; TimeZone=-60; _gid=GA1.2.313063078.1686555237; comm100_visitorguid_5000334=bc900b9e-21d4-472e-b41b-e85f2f2136c1; DDoS_Protection=4c172812a4f478a31d78eeb5c5fd940b; ASP.NET_SessionId=tn10olzpx3el5pusuaylbkwh; __RequestVerificationToken=ky1lc0Lxy5VIRY2UGye7_YTfxuu1Vsm_6xb0RfVzNG54Sqo38s0rQEla2LLOAbCchyHa-qjzjOYDh7wFEaBwOyril9J3B2Bm58Z-JCdLSYk1; _gat_gtag_UA_160317988_1=1",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Content-Length": "0",
    "TE": "trailers",
}

def start_foot(foot_id):
    sports_url = f'https://tounesbet.com/SportCategory?SportId={foot_id}&BetRangeFilter=0&DateDay=all_days'
    html_text = requests.post(sports_url, headers=headers, verify = False).text
    soup = BeautifulSoup(html_text, 'html.parser')
    
    countries = {}
    for country_div in soup.find_all('div', {"class": "divSportCategory"}):
        data_sportid = country_div.find('a')["data-sportid"]
        data_sportcategoryid = country_div.find('a')["data-sportcategoryid"]
        menu_sport_name = unidecode(country_div.find('span', {"class": "menu-sport-name"}).text)

        f = open(f"./tb/{menu_sport_name}.json", "w")
        json_data = json.dumps(
            get_tours(data_sportid, data_sportcategoryid), 
            indent=4
        )
        f.write(json_data)
        print(menu_sport_name)
        f.close()

def get_tours(SportId, SportCategoryId):
    country_id = SportCategoryId
    tournaments_url = f"https://tounesbet.com/Tournaments?SportId={SportId}&SportCategoryId={country_id}&BetRangeFilter=0&DateDay=all_days"
    html_text = requests.post(tournaments_url, headers=headers, verify = False).text
    soup = BeautifulSoup(html_text, 'html.parser')

    tours = {}
    for tour_div in soup.find_all('div', {"class": "divTournament"}):
        data_tournamentid = tour_div.find('a')["data-tournamentid"]
        menu_sport_name = unidecode(tour_div.find('span', {"class": "menu-sport-name"}).text)

        tours[menu_sport_name] = get_dates(SportId, country_id, data_tournamentid)

    return tours

def get_dates(SportId, country_id, tournamentid):
    tournaments_url = f"https://tounesbet.com/Sport/{SportId}/Category/{country_id}/Tournament/{tournamentid}?DateDay=all_days&BetRangeFilter=0&Page_number=1"
    html_text = requests.post(tournaments_url, headers=headers, verify = False).text
    soup = BeautifulSoup(html_text, 'html.parser')
    # print(html_text)
    m_dates = {}
    m_date = ""
    matches = {}
    x = 0
    for tr in soup.find_all('tr'):
        if (m_date == "" and tr["class"][0] == "header_row"):
            m_date = tr.find('span').text
            matches = {}
            
        if (m_date and tr["class"][0] == "trMatch"):
            matches[tr["data-matchid"]] = get_match(tr)
            m_dates[m_date] = matches
            
    return m_dates

def get_match(tr_match):
    tdMatch = tr_match.find('td', {"class": "tdMatch"})
    time = tdMatch.select('div:first-of-type')[0].text.strip()
    competitor1 = unidecode(tdMatch.select('div.competitor-wrapper div.competitor1-name')[0].text)
    competitor2 = unidecode(tdMatch.select('div.competitor-wrapper div.competitor2-name')[0].text)
    tdbetColumns = tr_match.find_all('td', {"class": "betColumn"})
    odds = {}
    for tdbetCol in tdbetColumns:
        spans = tdbetCol.find_all('span', {"class": "match_odd"})
        oddy = {}
        odd_title = ""
        for sp in spans:
            oddspecial = ""
            if sp.has_attr("data-outcomeid") and sp.has_attr("data-matchoddspecialbetvalue") and sp.has_attr("data-oddvaluedecimal"):
                oddname = sp["data-outcomeid"]
                oddspecial = sp["data-matchoddspecialbetvalue"]
                oddvalue = sp["data-oddvaluedecimal"]
                oddy[oddname] = oddvalue
                odd_title += oddname
            else:
                continue

        odd_title += oddspecial
        odds[odd_title] = oddy
    
    return {"time": time, "comp1": competitor1, "comp2": competitor2, "odds": odds}

def rm_files():
    tb_files = os.listdir("./tb/")
    for f in tb_files:
        os.remove("./tb/"+f)
        
rm_files()
start_foot("1181")
