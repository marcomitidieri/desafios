# Os schemas são responsáveis por:
# fazer validações
# serializar os dados
# Ou seja, os dados que voce quer que apareça na sua API,
# no JSON de retorno, passam pelos schemas.

from typing import Annotated
from pydantic import UUID4, Field
from datetime import datetime

from workout_api.contrib.schemas import BaseSchema

class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', examples=['Scale'], max_length=10)]
    
class CategoriaOut(CategoriaIn):    
    id: Annotated[UUID4, Field(description='Identificador da categoria')]
    