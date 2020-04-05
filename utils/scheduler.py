import schedule
import time
import requests
import json
import pytz
import datetime

def send_request():
    resp = requests.get('http://localhost:6800/listjobs.json?project=app')
    running = json.loads(resp.text)['running']
    if not running:
        ret = requests.post('http://localhost:6800/schedule.json', data={'project':'app', 'spider':'store'})
        print(ret.text)
        return ret.text

def job():
    now = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai'))
    # pause the job every Tuesday from 13:50 to 15:10
    if now.weekday() == 1 and now.time() > datetime.time(hour=13,minute=50) and now.time() < datetime.time(hour=15,minute=10):
        return
    send_request()

schedule.every(10).minutes.do(job)
schedule.run_all()

while True:
    schedule.run_pending()
    time.sleep(1)