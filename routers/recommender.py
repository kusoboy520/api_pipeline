from typing import Optional
import random
import uuid
import json
import re

from rabbit_task.clients import PikaClient
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from schemas.base_schema import ResponseSchema, ErrorSchema
from routers.models.itemtoitem import itemtoitme

router = APIRouter(
    prefix='/rec/v1', 
    tags=['Recommendation system'],
)

@router.get(
        '/itemtoitem',
        responses={
        200: {"model":ResponseSchema,'description': 'Successful Response'}, 
        400: {'description': 'Bad Request'},
        422: {'description':'Validation Error'},
        500: {'description': 'Server Error'},
    })
async def get_itemtoitem(itemid: int, userid: Optional[str]=None):
    if (itemid is None) or  (itemid>99999):
        raise HTTPException(
            status_code=400,
            detail = 'Itemid is required'
        )
    if userid is None:
        userid = f'user_{random.randint(1,10)}'
    rabbit = PikaClient()
    if rabbit.conn_check == True:
        data = {'userid': userid, 'itemid': str(itemid)}
        body = json.dumps(data)
        rabbit.MessageSender(queue_name='demo', routing_key='demo', exchange='', body =body)

    try:
        result = itemtoitme(itemid)
        return {
            'userid':userid,
            "rec_list":result
        }
    except:
        raise HTTPException(
            status_code=500,
            detail = 'Server error'
        )
        