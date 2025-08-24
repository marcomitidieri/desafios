# Os schemas são responsáveis por:
# fazer validações
# serializar os dados
# Ou seja, os dados que voce quer que apareça na sua API,
# no JSON de retorno, passam pelos schemas.

from typing import Annotated
from pydantic import UUID4, Field

from workout_api.contrib.schemas import BaseSchema

class CentroTreinamentoIn(BaseSchema):
    nome:         Annotated[str, Field(description='Nome do centro de treinamento',         examples=['CT King'], max_length=20)]
    endereco:     Annotated[str, Field(description='Endereço do centro de treinamento',     examples=['Rua dos exercicios, 50.'], max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietário do centro de treinamento', examples=['Miriam meu bem'], max_length=30)]


class CentroTreinamentoOut(CentroTreinamentoIn):    
    id: Annotated[UUID4, Field(description='Identificador do centro de treinamento')]


class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', examples=['CT King'], max_length=20)]