from sqlalchemy import create_engine, text
from config import DATABASE_URL


engine = create_engine(DATABASE_URL) #echo=True


def get_apikeys():
    with engine.connect() as conn:
        results = conn.execute(text("SELECT * FROM api_keys;"))
        keys = [result[1] for result in results]
        return keys
    

def check_apikey(api_key: str) -> int:
    with engine.connect() as conn:
        query = text(f"SELECT * FROM api_keys WHERE api_key = '{api_key}';")
        result = conn.execute(query)
        result_as_dict = result.mappings().all()
        # print(result_as_dict)
        user_id = result_as_dict[0]["user_id"]
        return user_id


def log_challenge_event(user_id, challenge, time_stamp, event) -> None:
    with engine.begin() as conn:
        query = text(f"""
            INSERT INTO challenges_log(user_id, challenge, time_stamp, event_desc)
            VALUES ({user_id},'{challenge}','{time_stamp}', '{event}');""")
        conn.execute(query)
        return None
    

if __name__ == '__main__':
    print('se ejecuta get_apikeys()')
    apikeys = get_apikeys()
    print(apikeys)