# Distributed Systems Project 2024

How to run frontend:
- npm install
- npm start
- open http://localhost:5173/ (might be different if that port is taken)

How to run backends:
- install redis and start the redis server with `redis-server`
- create a python virtual environment and enter it
- install requirements in venv `pip install -r requirements.txt`
- Add the following environment variables: `REDIS_URL`, `FLASK_INDEX`, `WHITELIST` and `PEER_URL`
- The command `gunicorn app:app` starts the server.


- start the backends with `$env:FLASK_RUN_PORT = 5000; flask run` and `$env:FLASK_RUN_PORT = 5001; flask run` (might be slightly different for non Windows systems)