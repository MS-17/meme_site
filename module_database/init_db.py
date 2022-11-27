import sqlite3


def table_exists(connection, table_name):
    res = connection.execute(f"select name from sqlite_master where type='table' and name='{table_name}'")
    return res.fetchone() is not None


def connect_db(path):
    connection = sqlite3.connect(path)
    return connection


# call it only 1 time if you don't have the db created
def create_table(connection, path_to_scheme, table_name):
    if not table_exists(connection, table_name):
        with open(path_to_scheme) as file1:
            connection.executescript(file1.read())


def add_row(connection, content):
    # cur.execute("insert into posts (title, content) values (?, ?)",
    #             ('first post', 'first post content'))
    #
    # cur.execute("insert into posts (title, content) values (?, ?)",
    #             ('second aa', 'second post content'))

    """Content is author, text, image, likes, dislikes"""
    curs = connection.cursor()

    cont_lst = content.split(',')

    if len(cont_lst) != 5:
        raise ValueError("The content string should contain 4 arguments")

    curs.execute("insert into posts (author, text, image, likes, dislikes) values (?, ?, ?, ?, ?)",
                 (cont_lst[0], cont_lst[1], cont_lst[2], cont_lst[3], cont_lst[4]))

    connection.commit()


def close_connection(connection):
    connection.close()


def append_data(path, table_name, content):
    """Content is author, text, image, likes, dislikes"""
    connection = connect_db(path)
    create_table(connection, 'scheme.sql', table_name)
    add_row(connection, content)
    close_connection(connection)


def get_all_data(connection):
    """None if the table is empty"""
    table = connection.execute('select * from posts').fetchall()
    # res = []
    dict1 = {}

    if table is None:
        return None
    for row in table:
        dict1[row[0]] = list(row[1:])
        # print(dict1)

    # for row in table:
    #     res += [list(row)]

    return dict1


def get_last_row(connection):
    """None if the table is empty"""
    # table = connection.execute('select * from posts order by id desc limit 1').fetchone() #return tuple
    # print(table)
    data = get_all_data(connection)
    last_idx = list(data.keys())[-1]
    return {last_idx: data[last_idx]}

# conn = connect_db('database.db')
# create_table(conn, 'scheme.sql', 'posts')
# get_all_data(conn)
# print(get_last_row(conn))

# print(start.messages)
# import json as js
# dict1 = {1: 'a', 2: 'b'}
# print(js.dumps(dict1))


# append_data('database.db', 'posts', 'hi,image here,4,1')
# append_data('database.db', 'posts', 'hey,image here,17,2')
# conn = connect_db('database.db')
# cur = conn.cursor()
# add_data(conn, 'text,image here,10,10')
# dict1 = get_all_data(conn)
# print(dict1)
# i = list(dict1.items())
# print(type(i[0][0]))


# print(table_exists(conn, 'posts'))

# cur.execute('select * from posts')
# print(cur.fetchall())   # works only if we made at least 1 query
# print(cur.lastrowid)
# res = cur.execute("select name from sqlite_master where type='table' and name='posts'")
# print(res.fetchone())
# for row in cur.execute('select * from posts'):
#     print(row)

# for row in cur.execute('select * from posts'):
#     print(row)

# print(conn.execute('select * from posts'))
# print(cur.execute('select * from posts'))

# conn.close()
