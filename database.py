import pymssql
from env import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, QUERY_LOG_FILE
from logger import logger
from utils import clean

conn = pymssql.connect(f"{DB_HOST}:{DB_PORT}", DB_USER, DB_PASS, DB_NAME)


def execute_query(conn, query):
    cursor = conn.cursor(as_dict=True)
    cursor.execute(query)

    data = list(cursor)
    conn.commit()

    if not data:
        return data

    return data if len(data) > 1 or query.startswith("select") else data[0]


def gen_values_str(values):
    value_str = ", ".join(f"'{clean(value)}'" for value in values)
    return value_str


def gen_assignments(dict_value):
    assigment_list = [f"{key}='{clean(value)}'" for key, value in dict_value.items()]
    assigment_str = ", ".join(assigment_list)

    return assigment_str


def log_query(query):
    with open(QUERY_LOG_FILE, "a") as file:
        file.write("\n")
        file.write(query)


def insert_data(conn, table, data, echo=True):
    query = f"INSERT INTO {table} ({', '.join(data.keys())}) OUTPUT INSERTED.* VALUES ({gen_values_str(data.values())});"

    logger.debug(f"Executing: {data}")

    log_query(query)

    data = execute_query(conn, query)
    return data


def update_data(conn, table, update_data, filter_data, echo=True):
    query = f"UPDATE {table} SET {gen_assignments(update_data)} where {gen_assignments(filter_data)};"

    logger.debug(f"Executing: {query}")
    log_query(query)

    data = execute_query(conn, query)
    return data
