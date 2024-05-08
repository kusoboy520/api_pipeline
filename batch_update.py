from rabbit_task.clients import PikaClient, redisClient
import json
import pandas as pd
from prefect import task, flow

@task(retries=3)
def getMessage(queue_name='demo', exchange='', routing_key='demo') -> list:
    '''
    get message from rabbit queue
    Args:
        queue_name: (string)
        exchange: (string)
        routing_key: (string)
    '''
    rabbit = PikaClient()
    all_Messages = rabbit.MessageConsume(queue_name=queue_name, exchange=exchange, routing_key=routing_key)
    if len(all_Messages) > 0:
        all_Messages = list(map(lambda x: json.loads(x), all_Messages))
    return all_Messages
@task()
def cleandata(all_Messages: list) -> pd.DataFrame:
    '''drop duplicate data and merge with redis data
    Args.
        all_Messages: API Message data (list[dict])
            ex. [{"userid": userid, "itemid":itemid}, {"userid": userid, "itemid":itemid},...]
    '''
    #get user info from redis db
    with redisClient(db=0) as r:
    # r = redisClient(db=0)
        newdf = pd.DataFrame(all_Messages)
        uid_lst = newdf['userid'].to_list()
        db_lst = r.mget(uid_lst)
        r.close() # disconnect the redis 
    db_df = pd.DataFrame({'userid': uid_lst, 'itemid': db_lst})
    db_df.dropna(axis=0, inplace=True)
    db_df['itemid'] = db_df['itemid'].map(lambda x: x.split(','))
    db_df = db_df.explode('itemid').reset_index(drop=True)

    # concat new data and rearrange
    final = pd.concat([db_df, newdf], ignore_index=True)
    final['sid'] = pd.Series([i for i in range(len(final))])
    final = final.groupby(['userid', 'itemid'])['sid'].max().reset_index()
    final = final.groupby('userid', sort='sid')['itemid'].agg(lambda x: ','.join(x)).reset_index()

    return final
@task(retries=1)
def insert_redis(final: pd.DataFrame):
    '''update data and insert into redis db'''
    index = 0
    r = redisClient(db=0)
    with redisClient(db=0).pipeline() as pipe:
        for key, value in zip(final['userid'], final['itemid']):
            r.set(key, value)
            if (index+1) % 2000 == 0:
                pipe.execute()
            index += 1
    print('Data insert success.')

@flow(name='batch_update')
def flow_update():
    try:
        all_Messages = getMessage(queue_name='demo', exchange='', routing_key='demo')
        if len(all_Messages) > 0:
            final = cleandata(all_Messages)
            insert_redis(final)
    except Exception as e:
        print(e)



if __name__ == '__main__':
    flow_update()