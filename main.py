"""
Update Tushare data to MySQL database.
"""
import json
from bageltushare import download, update_by_code, update_by_date
from bageltushare import create_index, create_all_tables, get_engine
from time import perf_counter


# configs
HOST = "localhost"
PORT = 3306
USER = "root"
PASSWORD = "Hyz.js180518"
DB = "tushare"

ENGINE = get_engine(HOST, PORT, USER, PASSWORD, DB)
TOKEN = "f7ad1328a17b49b5b7d126cb3ef4ae00565cba3adc28eeeecabbeb78"


def yearly_update(apis: dict) -> None:
    """
    update yearly apis
    :param apis: dict, the apis to update
    :return: None
    """
    for api in apis["yearly"]:
        print(f"====== Download {api} ======")
        # check if the api have params or fields
        if "params" in apis["yearly"][api]:
            params = apis["yearly"][api]["params"]
        else:
            params = None
        if "fields" in apis["yearly"][api]:
            fields = apis["yearly"][api]["fields"]
        else:
            fields = None
        download(engine=ENGINE, token=TOKEN, api_name=api, params=params, fields=fields)


def monthly_update(apis: dict) -> None:
    """
    update monthly apis
    :param apis: dict, the apis to update
    :return: None
    """
    for api in apis["monthly"]:
        print(f"====== Update {api} by code ======")
        # check if the api have params or fields
        if "params" in apis["monthly"][api]:
            params = apis["monthly"][api]["params"]
        else:
            params = None
        if "fields" in apis["monthly"][api]:
            fields = apis["monthly"][api]["fields"]
        else:
            fields = None
        update_by_code(engine=ENGINE, token=TOKEN, api_name=api, params=params, fields=fields)


def daily_update(apis: dict) -> None:
    """
    update daily apis
    :param apis: dict, the apis to update
    :return: None
    """
    for api in apis["daily"]:
        print(f"====== Update {api} by date ======")
        # check if the api have params or fields
        if "params" in apis["daily"][api]:
            params = apis["daily"][api]["params"]
        else:
            params = None
        if "fields" in apis["daily"][api]:
            fields = apis["daily"][api]["fields"]
        else:
            fields = None
        update_by_date(engine=ENGINE, token=TOKEN, api_name=api, params=params, fields=fields)


def create_indexes(apis: dict) -> None:
    """create indexes for the given apis"""
    all_apis = []
    for api in apis["yearly"]:
        all_apis.append(api)
    for api in apis["monthly"]:
        all_apis.append(api)
    for api in apis["daily"]:
        all_apis.append(api)

    for api in all_apis:
        print(f"Index created for {api}")
        create_index(engine=ENGINE, table_name=api)


def main() -> None:
    """main function"""
    create_all_tables(ENGINE)
    with open("update_apis.json", encoding="utf-8") as f:
        apis = json.load(f)

    # User input to choose update type: 1 for daily, 2 for monthly, 3 for yearly, 0 for create indexes
    update_type = input("Choose update type:\n1. Daily\n2. Monthly\n3. Yearly\n0. Create Indexes\nEnter your choice: ")
    if update_type == "1":
        print("Updating daily data...")
        daily_update(apis)
    elif update_type == "2":
        print("Updating monthly data...")
        monthly_update(apis)
    elif update_type == "3":
        print("Updating yearly data...")
        yearly_update(apis)
    elif update_type == "0":
        print("Creating indexes...")
        create_indexes(apis)
    else:
        print("Invalid choice. Exiting.")
        return


if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    print(f"total time: {end - start:.2f}s \n or {(end - start) / 60:.2f}min")
