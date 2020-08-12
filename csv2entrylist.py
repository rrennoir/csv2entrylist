import csv
import json
import argparse


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
                        car_model: dict, max_driver: int, admins=[]):

    entry_list = {
        "entries": [],
        "forceEntryList": 1
        }

    for team_row in entry_csv:

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

        # Generate drivers.
        for i in range(1, max_driver + 1):

            driver = add_driver(i, team_row, header)
            if driver != {}:
                if driver["playerID"][1:] in admins:
                    team["isServerAdmin"] = 1

                team["drivers"].append(driver)

        entry_list["entries"].append(team)

    # Save entry list to json file
    with open("entrylist.json", "w", encoding="utf-16") as entry_json_fp:
        json.dump(entry_list, entry_json_fp, indent=4)


def read_csv(csv_path: str):

    with open(csv_path) as entry_fp:
        entry_csv = csv.reader(entry_fp)
        csv_header = next(entry_csv)

        header_list = []
        for column in csv_header:
            header_list.append(column)

        registration = []
        for entry in entry_csv:
            registration.append(entry)

    return registration, header_list


def get_args():

    desc = "Convert csv file to an entry list for ACC"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("path_to_csv")

    help_admin = "steam id of the admin(s)"
    parser.add_argument("-admin", nargs="+", help=help_admin)

    help_carid = "path to car_model.json"
    parser.add_argument("-carid", default="./car_model.json", help=help_carid)

    # parser.add_argument("-DEBUG", action="store_true")

    return parser.parse_args()


if __name__ == "__main__":

    args = get_args()

    with open(args.carid) as car_model_fp:
        car_model = json.load(car_model_fp)

    registration, header_list = read_csv(args.path_to_csv)

    header = {}
    max_driver = 0
    for column_id, column_name in enumerate(header_list):

        header.update({column_name.lower(): column_id})
        if column_name.lower().startswith("steam id"):
            max_driver += 1

    if not args.admin:
        admin = []

    else:
        admin = args.admin

    print(admin)
    generate_entry_json(header, registration, car_model, max_driver, admin)
