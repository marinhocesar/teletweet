FROM python:3.11-buster

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY . /app
RUN python3 -m pip install -r /app/requirements.txt

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]