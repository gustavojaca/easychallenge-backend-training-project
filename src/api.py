import asyncio
from fastapi import FastAPI, Request
from datetime import datetime, timezone
from starlette.responses import JSONResponse
from contextlib import asynccontextmanager

from redis_cache import get_random_challenge, get_solution, assign_challenge, increment_tries, preload_challenges, print_challenges
from db import check_apikey, log_challenge_event
from model import Challenge
from config import REFRESH_CACHE_TIME


async def periodic_task():
    while True:
        print("Loading/updating caché...")
        await preload_challenges()
        await asyncio.sleep(REFRESH_CACHE_TIME)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicia la tarea de refresh de caché en background
    task = asyncio.create_task(periodic_task())
    try:
        # Devuelva el control a FastAPI para que pueda iniciar la aplicación
        yield
    finally:
        # Cancela la task cuando la aplicación se detiene
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


app = FastAPI(debug=False, lifespan=lifespan)


@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    api_key = request.headers.get('x-api-key')
    if not api_key:
        return JSONResponse(status_code=401, content={"detail": "API key missing"})
    user_id = check_apikey(api_key)
    if not user_id:
        return JSONResponse(status_code=403, content={"detail": "Invalid API key"})
    # TODO loguear en la base
    # Si pasa la validación, continúa con el request
    request.state.user_id = user_id
    response = await call_next(request)
    return response


@app.get("/challenge")
def get_challenge(request: Request) -> dict:
    challenge = get_random_challenge()
    assign_challenge(f'challenge:{challenge}')
        
    user_id = get_current_user(request)
    time_stamp = datetime.now(timezone.utc)
    log_challenge_event(user_id, challenge, time_stamp, 'challenge_assigned')
    # print_challenges(namespace='challenge')
    # print_challenges(namespace='assigned_challenge')
    
    return {"challenge": challenge}


@app.post("/challenge")
def post_challenge(submission: Challenge, request: Request) -> dict:
    challenge = submission.challenge
    solution = get_solution(f'assigned_challenge:{challenge}')
    if not solution:
        return JSONResponse(status_code=404, content={"detail": "Challenge not found"})
    
    user_id = get_current_user(request)
    time_stamp = datetime.now(timezone.utc)
    
    increment_tries(f'challenge:{challenge}')
    increment_tries(f'assigned_challenge:{challenge}')

    if  submission.solution == solution:
        log_challenge_event(user_id, challenge, time_stamp, 'challenge_solved')
        # print_challenges(namespace='challenge')
        # print_challenges(namespace='assigned_challenge')
        return {"correct": True, "message": "Challenge resolved successfully."}

    
    else:
        log_challenge_event(user_id, challenge, time_stamp, 'challenge_not_solved')
        # print_challenges(namespace='challenge')
        # print_challenges(namespace='assigned_challenge')
        return {"correct": False, "message": "Challenge incorrect."}
    

def get_current_user(request: Request):
    return request.state.user_id