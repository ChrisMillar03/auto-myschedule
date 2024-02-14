# auto-myschedule
Simple Python script to fetch McDonald's UK schedules.

## How To Use:
1. Run `pip install -r requirements.txt` to install any dependencies.

2. Place your MySchedule username & password into a .env file with the following keys:
```
MCD_USERNAME=
MCD_PASSWORD=
```

3. Run app.py and enjoy not having to solve captchas every time you're checking shifts.

## Potential Errors:
If you get an error with this script there could be multiple reasons:
- The captcha solver failed (most common)
- Your login details in the .env file are incorrect
- Your password hasn't been updated in the last 180 days
- The site layout has changed and the script hasn't been updated

**tensorflow only works with Python 3.9 to 3.11**
