import psycopg2
import os



def add_chat_id_to_postgres(chat_id):

    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
    except Exception as e:
        return "The subscription feature is currently unavailable please try again later."

    cur = conn.cursor()

    try:
        cur.execute("CREATE TABLE IF NOT EXISTS ACCOUNT( chat_id bigint not null, PRIMARY KEY(chat_id));")
        insert = f'INSERT INTO account (chat_id) VALUES({chat_id});'
        cur.execute(insert)
        conn.commit()
    except Exception as e:
        return "The subscription feature is currently unavailable please try again later."

    cur.close()
    conn.close()
    return "You are subscribed successfully! Use command /unsubscribe to stop daily updates. "

def get_chat_ids():
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
    except Exception as e:
        print(str(e))
        return None

    cur = conn.cursor()

    try:
        cur.execute("CREATE TABLE IF NOT EXISTS ACCOUNT( chat_id integer not null, PRIMARY KEY(chat_id))")
        select_statement = "SELECT * FROM ACCOUNT"
        cur.execute(select_statement)
        result = cur.fetchall()
    except Exception as e:
        print(str(e))
        return None

    cur.close()
    conn.close()
    return result

