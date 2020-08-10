import csv
import pprint
import json
import sys


def add_driver(driver_number: int, row: list, header: dict):

    driver = {}
    try:
        steamid = header[f"steam id {driver_number}"]

    except IndexError:
        steamid = None

    if steamid:
        try:
            driver.update({"playerID": row[steamid]})

            try:
                firstName = header[f"first name {driver_number}"]
                if row[firstName] != " ":
                    driver.update({"firstName": row[firstName]})

                lastName = header[f"last name {driver_number}"]
                if row[lastName] != " ":
                    driver.update({"lastName": row[lastName]})

                shortName = header[f"short name {driver_number}"]
                if row[shortName] != " ":
                    driver.update({"shortName": row[shortName][:3].upper()})

            except IndexError:
                pass

        except IndexError:
            pass

    return driver


def generate_entry_json(entry_list: dict, header: dict,
                        entry_csv: list, car_model: dict):

    for team_row in entry_csv:
        team = {
            "drivers": [],
            "raceNumber": int(team_row[header["car number"]]),
            "forcedCarModel": car_model[team_row[header["car model"]].lower()],
            "overrideDriverInfo": 1,
            "defaultGridPosition": -1,
            # "ballastKg": 0,
            # "restrictor": 0,
            # "customCar": "",
            # "overrideCarModelForCustomCar": 0,
            "isServerAdmin": 0
        }

        # pprint.pprint(header)
        for i in range(1, 5):
            driver = add_driver(i, team_row, header)
            if driver != {}:
                team["drivers"].append(driver)

        # pprint.pprint(team)
        entry_list["entries"].append(team)

    # Save entry list to json file
    with open("entrylist.json", "w", encoding="utf-16") as entry_json_fp:
        json.dump(entry_list, entry_json_fp, indent=4)


def csv2entrylist(csv_path: str, car_ids_path: str = "car_model_list.json"):

    with open(car_ids_path) as car_model_fp:
        car_model = json.load(car_model_fp)

    with open(csv_path) as entry_fp:
        entry_csv = csv.reader(entry_fp)
        csv_header = next(entry_csv)

        header = {}
        for i in csv_header:
            header.update({i.lower(): csv_header.index(i)})

        entry_list = {
                "entries": [],
                "forceEntryList": 1
                }

        generate_entry_json(entry_list, header, entry_csv, car_model)


if __name__ == "__main__":

    if len(sys.argv) == 2:
        csv2entrylist(sys.argv[1])

    elif len(sys.argv) == 3:
        csv2entrylist(sys.argv[1], sys.argv[2])

    else:
        print("Usage: csv2entrylist.py pathToCsvFile")
