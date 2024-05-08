from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from routers import recommender
import time

app = FastAPI(
    docs_url='/swagger',
    title='Reccomendation API Service',
    version='1.0.0'
)
app.include_router(recommender.router)
templates = Jinja2Templates(directory='templates')

@app.middleware('http')
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(f'{process_time:0.4f} sec')
    return response


