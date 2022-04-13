FROM tiangolo/uwsgi-nginx-flask:python3.6
ENV STATIC_URL ./app/static
COPY ./app /app
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt