from datetime import timedelta, datetime
from rabbit_task.clients import redisClient
from prefect import flow
from prefect.client.schemas.schedules import IntervalSchedule

@flow(name='daily_clean', log_prints=True)
def main():
    try:
        r = redisClient(db=0)
        for i in r.keys():
            r.delete(i)
        print('daily job success')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()