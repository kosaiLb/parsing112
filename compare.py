import os
import json
from termcolor import colored

LIMIT = 0

diff_countries = {
    'Republique de Coree.json': 'Coree du Sud.json',
    'Nouvelle-Zelande.json': 'Nouvelle Zelande.json'
}

in_Monde = [
    'Amerique du Nord et Centrale.json',
    'Amerique du sud.json',
    'Asie.json',
    'Europe.json'
]

def compare_time(tbTime, fwTime):
    tb = tbTime.split(':')
    fw = fwTime.split(':')
    if int(fw[0]) < 23:
        fw[0] = str(int(fw[0])+1)
    else:
        fw[0] = "00"

    if fw[0] == tb[0] and fw[1] == tb[1]:
        return True
    return False

def compare_date(tbDate, fwDate):
    for i in range(3):
        if not tbDate[i] == fwDate[i]:
            return False
    return True

def compare():
    tb_files = set(os.listdir("./tb/"))
    fw_files = set(os.listdir("./fw/"))
    common = list(tb_files.intersection(fw_files))

    diff_file = open('diff.json')
    diff = json.loads(diff_file.read())
    diff_cs = list(diff.keys())

    for c in common:
        tb_file = open('./tb/'+c)
        fw_file = open('./fw/'+c)
        tb = json.loads(tb_file.read())
        fw = json.loads(fw_file.read())
        fw_tours = list(fw.keys())

        print(c)
        for Tbt in tb:
            for Fwt in fw_tours:
                if Tbt in Fwt or Fwt in Tbt:
                    calculate(tb[Tbt], fw[Fwt], Tbt, Fwt, c[0:-5])
                else:
                    if c[0:-5] in diff_cs:
                        for el in diff[c[0:-5]]:
                            if el[0] in Tbt or Tbt in el[0] and el[1] in Fwt or Fwt in el[1]:
                                calculate(tb[Tbt], fw[Fwt], Tbt, Fwt, c[0:-5])

def replace_char(n):
    for k, c in enumerate(n):
        if c in ['-', ',', '.', '\\', '/']:
            list(n)[k] = ' '
    return "".join(n)

def compare_eq_names(n1, n2):
    if n1 in n2 or n2 in n1:
        return True
    n1 = replace_char(n1.strip()).split(' ')
    n2 = replace_char(n2.strip()).split(' ')
    count = 0
    for w1 in n1:
        for w2 in n2:
            if w1 == w2 and not w1 == ' ' and not w2 == ' ':
                count += count
    if count > 1:
        return True
    return False

def F_1x2(_type, x1, x2, x3, tbeq1, tbeq2, fweq1, fweq2, Tbt, Fwt, country):
    total = 100 - (100/x1 + 100/x2 + 100/x3)
    if total > LIMIT:
        print(f"""
{colored("==> "+str(total), 'green')}
            {tbeq1}, {tbeq2}
            {fweq1}, {fweq2}

            {_type}
            {x1} {x2} {x3}
            
            {colored(country, 'red')}
            tour : {Tbt}, 
            tour : {Fwt}
        """)

def F_Double(_type, x1, x2, tbeq1, tbeq2, fweq1, fweq2, Tbt, Fwt, country):
    total = 100 - (100/x1 + 100/x2)
    if total > LIMIT:
        print(f"""
{colored("==> "+str(total), 'green')}
            {tbeq1}, {tbeq2}
            {fweq1}, {fweq2}

            {_type}
            {x1} {x2}

            {colored(country, 'red')}
            tour : {Tbt}, 
            tour : {Fwt}
        """)

def calc_1x2_Double(tb_1x2, fw_1x2, tb_D, fw_D, tbeq1, tbeq2, fweq1, fweq2, Tbt, Fwt, country):
    if tb_1x2 and fw_1x2:
        tb = {}
        fw = fw_1x2
        for el in tb_1x2:
            tb[el] = float(".".join(tb_1x2[el].split(',')))

        F_1x2("tb_1 fw_X fw_2", tb['1'], fw['X'], fw['2'], tbeq1, tbeq2, fweq1, fweq2, Tbt, Fwt, country)
        F_1x2("tb_X fw_1 fw_2", tb['X'], fw['1'], fw['2'], tbeq1, tbeq2, fweq1, fweq2, Tbt, Fwt, country)
        F_1x2("tb_2 fw_1 fw_X", tb['2'], fw['1'], fw['X'], tbeq1, tbeq2, fweq1, fweq2, Tbt, Fwt, country)
        F_1x2("fw_1 tb_X tb_2", fw['1'], tb['X'], tb['2'], tbeq1, tbeq2, fweq1, fweq2, Tbt, Fwt, country)
        F_1x2("fw_X tb_1 tb_2", fw['X'], tb['1'], tb['2'], tbeq1, tbeq2, fweq1, fweq2, Tbt, Fwt, country)
        F_1x2("fw_2 tb_1 tb_X", fw['2'], tb['1'], tb['X'], tbeq1, tbeq2, fweq1, fweq2, Tbt, Fwt, country)

        if tb_D and fw_D:
            tbD = {}
            for el in tb_D:
                tbD[el] = float(".".join(tb_D[el].split(',')))

            F_Double("tb_1 fw_X2", tb['1'], fw_D['X2'], tbeq1, tbeq2, fweq1, fweq2, Tbt, Fwt, country)
            F_Double("tb_X fw_12", tb['X'], fw_D['12'], tbeq1, tbeq2, fweq1, fweq2, Tbt, Fwt, country)
            F_Double("tb_2 fw_1X", tb['2'], fw_D['1X'], tbeq1, tbeq2, fweq1, fweq2, Tbt, Fwt, country)
            F_Double("fw_1 tb_X2", fw['1'], tbD['X2'], tbeq1, tbeq2, fweq1, fweq2, Tbt, Fwt, country)
            F_Double("fw_X tb_12", fw['X'], tbD['12'], tbeq1, tbeq2, fweq1, fweq2, Tbt, Fwt, country)
            F_Double("fw_2 tb_1X", fw['2'], tbD['1X'], tbeq1, tbeq2, fweq1, fweq2, Tbt, Fwt, country)

def calc_UO_2_5(tb_Under, tb_Over, w_Plus, fw_Minus, tbeq1, tbeq2, fweq1, fweq2, Tbt, Fwt, country):
    tb_Under = float(".".join(tb_Under.split(',')))
    tb_Over = float(".".join(tb_Over.split(',')))

    F_Double("tb_Under, w_Plus", tb_Under, w_Plus, tbeq1, tbeq2, fweq1, fweq2, Tbt, Fwt, country)
    F_Double("tb_Over, fw_Minus", tb_Over, fw_Minus, tbeq1, tbeq2, fweq1, fweq2, Tbt, Fwt, country)

def calculate(Tbt, Fwt, Tbt_tour, Fwt_tour, country):
    for date in Tbt:
        tb_date = list(reversed(date.split('/')))
        for match_id in Tbt[date]:
            tb_match = Tbt[date][match_id]

            for match_id in Fwt:
                fw_date = Fwt[match_id]['date'].split('-')
                fw_match = Fwt[match_id]
                if compare_time(tb_match["time"], fw_match["Time"]) and compare_date(tb_date, fw_date):
                    eq1 = compare_eq_names(tb_match["comp1"], fw_match["comp1"]) 
                    eq2 = compare_eq_names(tb_match["comp2"], tb_match["comp2"]) 
                    rev_eq1 = compare_eq_names(tb_match["comp1"], fw_match["comp2"]) 
                    rev_eq2 = compare_eq_names(tb_match["comp2"], fw_match["comp1"]) 

                    if eq1 and eq2 or rev_eq1 and rev_eq2:

                        tb_1x2 = []
                        fw_1x2 = []
                        if "1X2" in fw_match and "1X2" in tb_match["odds"]:
                            tb_1x2 = tb_match["odds"]["1X2"]
                            fw_1x2 = fw_match["1X2"]

                        tb_D = []
                        fw_D = []
                        if "Double Chance" in fw_match and "1X12X2" in tb_match["odds"]:
                            if len(fw_match["Double Chance"]) > 3:
                                tb_D = tb_match["odds"]["1X12X2"]
                                fw_D = fw_match["Double Chance"]

                        calc_1x2_Double(
                            tb_1x2, fw_1x2,
                            tb_D, fw_D,
                            tb_match["comp1"],
                            tb_match["comp2"],
                            fw_match["comp1"],
                            fw_match["comp2"],
                            Tbt_tour, Fwt_tour, country
                        )

                        if "Total O/U" in fw_match and "UnderOver2.5" in tb_match["odds"]:
                            if "+ de 2.5" in fw_match["Total O/U"]:
                                tb_Under = tb_match["odds"]["UnderOver2.5"]["Under"]
                                tb_Over = tb_match["odds"]["UnderOver2.5"]["Over"]
                                fw_Plus = fw_match["Total O/U"]["+ de 2.5"]
                                fw_Minus = fw_match["Total O/U"]["- de  2.5"]

                                calc_UO_2_5(
                                    tb_Under, tb_Over,
                                    fw_Plus, fw_Minus,
                                    tb_match["comp1"],
                                    tb_match["comp2"],
                                    fw_match["comp1"],
                                    fw_match["comp2"],
                                    Tbt_tour, Fwt_tour, country
                                )

compare()
