import random
import asyncio
import time
from datetime import datetime, timezone
from aiohttp import ClientSession
from redis import Redis
from config import API_URL, MAX_RETRIES, TIMEOUT, PRELOAD_CACHE_SIZE, REDIS_HOST, REDIS_PORT


challenges_cache = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def assign_challenge(key: str) ->  None:
    """
    TODO Docstring
    """
    challenge = challenges_cache.hgetall(key)
    if not challenge:
        print(f"No challenge found for key: {key}")
        return

    challenge_id = key.split(":", 1)[-1]
    new_key = f"assigned_challenge:{challenge_id}"
    challenges_cache.hset(new_key, mapping=challenge)


def increment_tries(key: str) -> None:
    """
    TODO Docstring
    """
    tries = challenges_cache.hget(key, 'tries')
    if tries:
        challenges_cache.hset(key, mapping={'tries': int(tries)+1})


def print_challenges(namespace: str) -> None:
    """
    Imprime el contenido de la caché utilizando pipelining para mejorar la eficiencia.
    """
    print(f'\nNamespace: {namespace}')
    all_keys = challenges_cache.keys(f'{namespace}:*')
    print(f'Cantidad de Keys: {len(all_keys)}')
    
    pipeline = challenges_cache.pipeline()
    for key in all_keys:
        pipeline.hmget(key, "solution", "time_stamp", "tries")
    values = pipeline.execute()
    
    for key, value in zip(all_keys, values):
        print(f'Challenge: {key} Solution: {value[0]} - {value[1]} - Retries: {value[2]}')

   
def get_random_challenge() -> str:
    """
    Devuelve un reto aleatorio de la caché.
    """
    # TODO validar que no tenga > 50 usos antes de asignar
    all_keys = challenges_cache.keys('challenge:*')
    while len(all_keys) == 0:
        asyncio.run(preload_challenges())
        all_keys = challenges_cache.keys('challenge:*')
    key = random.choice(all_keys) # TODO Evaluar si no es conviente aclarar el tipado con key:str=random....
    return key.split(":", 1)[-1]


def get_solution(key: str) -> str:
    """
    Devuelve la solución de un challenge en particular.
    """
    return challenges_cache.hget(key, 'solution')


async def preload_challenges() -> None:
    """
    # TODO Completar
    """
    await remove_old_challenges()

    keys_num = len(challenges_cache.keys('challenge:*'))
    if PRELOAD_CACHE_SIZE > keys_num:
        async with ClientSession() as session:
            tasks = [load_single_challenge(session) for _ in range(PRELOAD_CACHE_SIZE-keys_num)]
            await asyncio.gather(*tasks)
    
    print_challenges(namespace='challenge')
    print_challenges(namespace='assigned_challenge')



async def remove_old_challenges() -> None:
    """
    # TODO Completar
    """
    all_keys = challenges_cache.keys('assigned_challenge:*')
    
    pipeline = challenges_cache.pipeline()
    for key in all_keys:
        pipeline.hmget(key, "tries")
    values = pipeline.execute()
    
    remove_list = [key for key, value in zip(all_keys, values) if int(value[0]) >= MAX_RETRIES]
    
    for key in remove_list:
        challenges_cache.delete(f'challenge:{key.split(":",1)[-1]}')
        challenges_cache.delete(key)



async def load_single_challenge(session: ClientSession) -> None:
    """
    # TODO Completar
    """
    try:
        async with session.get(f"{API_URL}/challenge") as response:
            response.raise_for_status()
            data = await response.json()
            time_stamp = str(datetime.now(timezone.utc))
            time_stamp = time.strftime('%y/%m/%d %H:%M:%S')
            challenge = f"challenge:{data['challenge']}"
            challenges_cache.hset(challenge, mapping={
                'solution': data["solution"],
                'time_stamp': time_stamp,
                'tries': 0,
                })
            challenges_cache.expire(challenge, TIMEOUT)

    except Exception as e:
        print(f"Error fetching challenge: {e}")