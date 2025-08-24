from fastapi import FastAPI
from fastapi_pagination import add_pagination
from workout_api.routers import api_router

app = FastAPI(title='WorkoutAPI')
app.include_router(api_router)

add_pagination(app)




# O código abaixo não é necessário por causa da linha de comando usada para iniciar a aplicação.
# uvicorn workout_api.main:app --reload

# if __name__ == 'main':
#     import uvicorn
    
#     uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='info', reload=True)