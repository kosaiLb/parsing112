import requests
import json
from unidecode import unidecode

url = "https://sport.africawin365.com/Prematch"
startDate = "2023-06-10T23:00:00.000Z"
endDate = "3000-06-10T23:00:00.000Z"
dates = f"startDate={startDate}&endDate={endDate}&period=0"
other = "&isTournament=false&langId=16&partnerId=3000013&countryCode=TN"
match_other = "&isTournament=false&stakeTypes=1&stakeTypes=3&stakeTypes=37&stakeTypes=702&langId=16&partnerId=3000013&countryCode=TN"

false_tour = ["Gagnant", "Outrights", "Qualification", "Results", "Resultats"]

def get_cs():
    foot_url = f"{url}/Championships?{dates}&sportId=1{other}"
    foot_res = requests.get(foot_url).text
    foot_data = json.loads(foot_res)

    for c in foot_data:
        tours = {}
        tours_url = f"{url}/Tournaments?{dates}&championshipId={c['Id']}{other}"
        tours_res = requests.get(tours_url).text
        tours_data = json.loads(tours_res)
        
        for t in tours_data:
            tour_name = unidecode(t['N'])

            contains = False
            for el in false_tour:
                if el in tour_name:
                    contains = True

            if not contains:
                match_data = {}
                matchs_url = f"{url}/Matches?{dates}&tournamentId={t['Id']}{match_other}"
                matchs_res = requests.get(matchs_url).text
                matchs_data = json.loads(matchs_res)
                proto_data = matchs_data['CNT'][0]['CL'][0]['E']

                matches = {}
                for data in proto_data:
                    match_data = {
                        "comp1": unidecode(data["HT"]),
                        "comp2": unidecode(data["AT"]),
                        "date": data["D"],
                    }

                    for s in data["StakeTypes"]:
                        Stakes = {}
                        for stk in s["Stakes"]:
                            if (s["N"] == "Total O/U"):
                                Stakes[stk["N"] +" "+ str( stk["A"])] = stk["F"]                    
                            elif (s["N"] == "Double Chance"):
                                Stakes[stk["N"].strip()] = stk["F"]                    
                            else:
                                Stakes[stk["N"]] = stk["F"]                    
                            
                        match_data[s["N"]] = Stakes

                    matches["match"] = match_data

                tours[unidecode(t['N'])] = matches
            
        f = open(f"./fw/{unidecode(c['N'])}.json", "w")
        json_data = json.dumps(
            tours,
            indent=4
        )
        f.write(json_data)
        print(unidecode(c['N']))
        f.close()

get_cs()
