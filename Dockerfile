FROM tiangolo/uwsgi-nginx-flask:python3.6
COPY isd_api_server.py /app/main.py
