import meme_site.module_database.init_db as idb


def push_post(path_to_db, table_name, user, text, meme):
    idb.append_data(path_to_db, table_name, f'{user},{text},{meme},0,0')


def get_db(path_to_db):
    connection = idb.connect_db(path_to_db)
    return idb.get_all_data(connection)


def get_last_row(path_to_db):
    connection = idb.connect_db(path_to_db)
    return idb.get_last_row(connection)
