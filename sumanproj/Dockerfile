FROM python:3.8-slim

RUN apt-get update

WORKDIR /usr/app
COPY . .

RUN pip install -r requirements.txt
RUN export FLASK_APP=app.py
EXPOSE 8000

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000"]
CMD ["app:app"]
