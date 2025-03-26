# Setup

1. run following to up
   `docker compose up --build -d`
2. Setup .env file reffer .env.sample
3. run following to create tables
   `docker compose exec backend python init.py`

NOTE: Adjust number of workers in docker-compose.yml file as per your system configuration. deffault is 2 workers.
