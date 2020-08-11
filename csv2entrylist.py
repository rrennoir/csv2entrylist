import csv
import pprint
import json
import sys


def add_driver(driver_id: int, row: list, header: dict):

    driver = {}

    steamid = row[header[f"steam id driver {driver_id}"]]
    if steamid != "":

        driver.update({"playerID": f"S{steamid}"})

        if f"first name driver {driver_id}" in header:

            firstName = row[header[f"first name driver {driver_id}"]]
            if firstName != "":
                driver.update({"firstName": firstName})

        if f"last name driver {driver_id}" in header:

            lastName = row[header[f"last name driver {driver_id}"]]
            if lastName != "":
                driver.update({"lastName": lastName})

        if f"short name driver {driver_id}" in header:

            shortName = row[header[f"short name driver {driver_id}"]]
            if shortName != "":
                driver.update({"shortName": shortName.upper()})

    return driver


def generate_entry_json(header: dict, entry_csv: list,
                        car_model: dict, max_driver: int):

    entry_list = {
        "entries": [],
        "forceEntryList": 1
        }

    for team_row in entry_csv:

        # pprint.pprint(team_row)
        team = {
            "drivers": [],
            "raceNumber": int(team_row[header["car number"]]),
            "forcedCarModel": car_model[team_row[header["car model"]].lower()],
            "overrideDriverInfo": 1,
            # "defaultGridPosition": -1,
            # "ballastKg": 0,
            # "restrictor": 0,
            # "customCar": "",
            # "overrideCarModelForCustomCar": 0,
            "isServerAdmin": 0
        }

        for i in range(1, max_driver + 1):
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
        max_driver = 0
        for column_id, column_name in enumerate(csv_header):

            header.update({column_name.lower(): column_id})
            if column_name.lower().startswith("steam"):
                max_driver += 1

        # pprint.pprint(header)

        generate_entry_json(header, entry_csv, car_model, max_driver)


if __name__ == "__main__":

    if len(sys.argv) == 2:
        csv2entrylist(sys.argv[1])

    elif len(sys.argv) == 3:
        csv2entrylist(sys.argv[1], sys.argv[2])

    else:
        print("Usage: csv2entrylist.py pathToCsvFile")
