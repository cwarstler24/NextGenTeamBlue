# NextGenTeamBlue

## Using Python 3.13.9

## Create a Virtual Environment
```
  python -m venv venv
```
Then, activate the virtual environment.
Windows
```
  .\venv\Scripts\activate
```

macOS/Linux
```
  source venv/bin/activate
```

## Install pip packages
```
  pip install -r .\src\requirements.txt
```


<!-- Add postman link: https://app.getpostman.com/join-team?invite_code=ab7344646b2880073777a5bb776ac96f69630cdd797209261c2d5da5114dbb94&target_code=09cb41bcbfab941002074de5f23bfb5b -->


## Test API (Linux)
1. Start up listener in terminal:
```
  uvicorn src.main:app --reload
```
2. Open a new terminal and run:
```
  curl -X POST "http://127.0.0.1:8000/listener" \
  -H "Authorization: Bearer <insert_token_here>" \
  -H "Content-Type: application/json" \
  -d '{"type_id": "2", "location_id": "1", "employee_id": 31, "notes": "This is a test", "is_decommissoned": "0"}'
```
