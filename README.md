# Distributed Systems Project 2024

How to run frontend:
- npm install
- npm start
- open http://localhost:5173/ (might be different if that port is taken)

How to run backends:
- install redis and start the redis server with `redis-server`
- create a python virtual environment and enter it
- install requirements in venv `pip install -r requirements.txt`
- Add the following environment variables:
    - `REDIS_URL` (The url to the redis server)
    - `FLASK_INDEX` (0 or 1 depending on which flask server it is)
    - `WHITELIST` (The URLS from which HTTP requests are allowed separated by comma)
    - `SOCKET_URL` (The URL that flask hosts the websocket on. Default: `0.0.0.0:8000`)
    - `PEER_URL` (The URL of the other flask server)
- The command `gunicorn --config gevent_config.py -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker app:app` starts the server in production mode (doesn't work on windows).
- The command `flask run` start the server in development mode.
