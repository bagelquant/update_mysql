from bageltushare import download, update_by_code, update_by_date
from bageltushare import create_index, create_log_table, get_engine
from time import perf_counter


# configs
HOST = "localhost"
PORT = 3306
USER = "root"
PASSWORD = "Hyz.js180518"
DB = "tushare"

ENGINE = get_engine(HOST, PORT, USER, PASSWORD, DB)
TOKEN = "f7ad1328a17b49b5b7d126cb3ef4ae00565cba3adc28eeeecabbeb78"


def yearly_update() -> None:
    """update once a year"""
    # download and replace table
    download(engine=ENGINE, token=TOKEN, api_name="trade_cal")
    download(engine=ENGINE,
             token=TOKEN,
             api_name="stock_basic",
             params={"list_status": "L, D, P"},
             fields=[
                 "ts_code",
                 "symbol",
                 "name",
                 "area",
                 "industry",
                 "cnspell",
                 "market",
                 "list_date",
                 "act_name",
                 "act_ent_type",
                 "fullname",
                 "enname",
                 "exchange",
                 "curr_type",
                 "list_status",
                 "delist_date",
                 "is_hs"
             ])


def monthly_update() -> None:
    """update once a month"""
    by_code_apis = [
        "balancesheet",
        "cashflow",
        "income",
    ]

    for api in by_code_apis:
        update_by_code(engine=ENGINE, token=TOKEN, api_name=api)
        create_index(engine=ENGINE, table_name=api)


def daily_update() -> None:
    """update once a day"""
    by_date_apis = [
        "daily",
        "adj_factor",
    ]

    for api in by_date_apis:
        update_by_date(engine=ENGINE, token=TOKEN, api_name=api)
        create_index(engine=ENGINE, table_name=api)


def main() -> None:
    """main function"""
    create_log_table(ENGINE)
    # yearly_update()
    # monthly_update()
    daily_update()

if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    print(f"total time: {end - start:.2f}s \n or {(end - start) / 60:.2f}min")
