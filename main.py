import requests
import json
from secrets import API_TOKEN

OUTPUT_DIR = 'data'
HEADERS = {"User-Agent": "htbapi"}
BASE = "http://hackthebox.eu/api"

def getRequest(url: str) -> str:
    s = f"{BASE}{url}?api_token={API_TOKEN}"
    return requests.get(s, headers=HEADERS)

def getAllMachines():
    return getRequest("/machines/get/all/").json()

def get_matrix(machine_id: int):
    return getRequest(f'/machines/get/matrix/{machine_id}').json()

def write_data_all_machines():
    with open(f"{OUTPUT_DIR}/all_machines.json", 'w') as f:
        json.dump(getAllMachines(), f)

def read_data_all_machines():
    j = None
    with open(f"{OUTPUT_DIR}/all_machines.json", 'r') as f:
        j = json.load(f)
    return j

def write_data_all_matrices():
    all_matrices = []
    machines = read_data_all_machines()

    for machine in machines:
        print(f"{machine['id']}: {machine['name']}")
        matrix = get_matrix(machine['id'])
        all_matrices.append({"id": machine['id'], "matrix": matrix})

    with open(f"{OUTPUT_DIR}/all_matrices.json", 'w') as f:
        json.dump(all_matrices, f)

def read_data_all_matrices():
    matrices = None
    with open(f"{OUTPUT_DIR}/all_matrices.json", 'r') as f:
        matrices = json.load(f)
    return matrices

def get_name_from_id(id: int):
    machines = read_data_all_machines()
    for machine in machines:
        if machine["id"] == id:
            return machine["name"]

def get_difficulty(id: int):
    values = {'20':'Easy', '30':'Medium', '40':'Hard', '50': 'Insane'}
    machines = read_data_all_machines()
    for machine in machines:
        if machine["id"] == id:
            points = machine["points"]
            return values[f"{points}"]
            

def write_matrices_data_to_csv(maker_or_aggregate="aggregate"):
    if not maker_or_aggregate in ('maker', 'aggregate'):
        import sys
        sys.exit(1)

    import csv
    
    with open(f"{OUTPUT_DIR}/all_matrices_{maker_or_aggregate}.csv", 'w') as f:
        fieldnames = ["Id", "Machine name", "Difficulty", "Enumeration", "Real-life", "CVE", "Custom Exploitation", "CTF-like"]
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        matrices_data = read_data_all_matrices()
        matrices = ((o["id"], o["matrix"]) for o in matrices_data)
        writer.writerow(fieldnames)

        for id, matrix in matrices:
            name = get_name_from_id(id)
            difficulty = get_difficulty(id)
            writer.writerow([id, name, difficulty] + matrix[maker_or_aggregate])


if __name__ == "__main__":
    # write_data_all_machines()
    # write_data_all_matrices()
    write_matrices_data_to_csv()
    write_matrices_data_to_csv(maker_or_aggregate='maker')