# Distributed Systems Project 2024

Current bugs:
- When loading page, right-most column might be cut in half. When scrolling, the boxesPerRow gets recalculated and the column gets removed, messing up any drawing made. (Doesn't need to be fixed for prototype)

How to run frontend:
- npm install
- npm start
- open http://localhost:5173/ (might be different if that port is taken)

How to run backend:
- install redis and start the redis server with `redis-server`
- create a python virtual environment and enter it
- install requirements in venv `pip install -r requirements.txt`
- start the backend with `flask run`