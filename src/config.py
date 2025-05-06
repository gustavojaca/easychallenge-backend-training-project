#### REDIS CACHÉ ####
# REDIS_HOST = 'localhost' 
# REDIS_HOST = 'redis'
REDIS_HOST = 'easy-challenge-redis'
REDIS_PORT = 6379
PRELOAD_CACHE_SIZE = 200
# PRELOAD_CACHE_SIZE = 20
# REFRESH_CACHE_TIME = 60
REFRESH_CACHE_TIME = 300
MAX_RETRIES = 50
TIMEOUT = 10


#### DATABASE ####
# DATABASE_URL = 'postgresql+psycopg2://dbuser:e%40sy-p%40ssw0rd@127.0.0.1:5432/easy_challenge'
# DATABASE_URL = 'postgresql+psycopg2://dbuser:e%40sy-p%40ssw0rd@db:5432/easy_challenge'
DATABASE_URL = 'postgresql+psycopg2://dbuser:e%40sy-p%40ssw0rd@easy-challenge-db:5432/easy_challenge'


#### APP ####
APP_HOST = "0.0.0.0"
# APP_PORT = 12544
APP_PORT = 8000


#### CHALLENGE SERVER ####
# API_URL = 'http://127.0.0.1:30007'
# API_URL = 'http://host.docker.internal:12543'
API_URL = 'http://challenge-server:30007'