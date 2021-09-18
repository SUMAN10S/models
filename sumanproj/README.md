# Game Score Anomaly Detection

### Run on local system
* Install requirements using `pip3 install -r requiremnets.txt`
* Run `gunicorn app:app`
* App will be available on `localhost:8000`

### Run using Docker
* Build Docker images `docker built -t anomaly-api .`
* Run the image `docker run -p 8000:8000 anomaly-api`
* App will be available on `localhost:8000`

### Using the API

* Send a POST request to `localhost:8000` with the following JSON data:
```json
{"game": "Tower Jump", "score": "2000", "time": "100", "uid": "f38e42f5cc42c7b14de29e739cb87cc8ec6c6b127fb24c426668c13518ecac0b"}
```
* Using curl:
```bash
curl --location --request POST 'http://localhost:8080' \
--header 'Content-Type: application/json' \
--data '{"game": "Tower Jump", "score": "2000", "time": "100", "uid": "f38e42f5cc42c7b14de29e739cb87cc8ec6c6b127fb24c426668c13518ecac0b"}'
```