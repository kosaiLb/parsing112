import os
import json

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

def get_files():
    tb_files = set(os.listdir("./tb/"))
    fw_files = set(os.listdir("./fw/"))
    diffs = list(tb_files.symmetric_difference(fw_files))

    for c in diffs:
        if c in in_Monde:
            diffs.remove(c)
    
    for c in diffs:
        if c in diff_countries.keys():
            diffs.remove(c)

    common = list(tb_files.intersection(fw_files))
    monde_ex = []
    if "Monde.json" in common:
        monde_ex = in_Monde

    tb_diff = list(tb_files - fw_files)
    fw_diff = list(fw_files - tb_files)

    print(tb_diff)
    print(fw_diff)
    
    return [diffs, common, monde_ex, fw_files]

def get_diff_file():
    old_diff_file = open('diff.json')
    old_diff = json.loads(old_diff_file.read())
    old_diff_cs = list(old_diff.keys())
    old_diff_file.close()
    return [old_diff_cs, old_diff]

def diff_like(tours, existed):
    for t in tours:
        new_tb_diff = []
        exist = False
        for x in existed:
            if x in t:
                exist = True
        if not exist:
            new_tb_diff.append(t)
    return new_tb_diff

def differentiate(n, countries, old_diff_cs, old_diff):
    print("=> "+n)
    first = n
    if n in in_Monde:
        first = 'Monde.json'
    tb_file = open('./tb/'+first)
    fw_file = open('./fw/'+n)
    
    tb = json.loads(tb_file.read())
    fw = json.loads(fw_file.read())
    tb_tours = list(tb.keys())
    fw_tours = list(fw.keys())

    exist_tb = []
    exist_fw = []
    if n[0:-5] in old_diff_cs:
        for tour in old_diff[n[0:-5]]:
            exist_tb.append(tour[0])
            exist_fw.append(tour[1])

        new_tb_diff = diff_like(tb_tours, exist_tb)
        new_fw_diff = diff_like(fw_tours, exist_fw)
        countries[n[0:-5]] = [new_tb_diff, new_fw_diff]

    else:
        countries[n[0:-5]] = [tb_tours, fw_tours]
        
    tb_file.close()
    fw_file.close()
    return countries

def compare_common():
    diffs, common, monde_ex, fw_files = get_files()
    old_diff_cs, old_diff = get_diff_file()

    countries = {}

    for n in common:
        countries = differentiate(n, countries, old_diff_cs, old_diff)

    for n in monde_ex:
        if n in fw_files:
            countries = differentiate(n, countries, old_diff_cs, old_diff)
        
    f = open("new_diff.json", "w")
    json_data = json.dumps(
        countries, 
        indent=4
    )
    f.write(json_data)
    print("new_diff.json ok")
    f.close()

compare_common()
