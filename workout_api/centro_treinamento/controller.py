from uuid import uuid4
from fastapi import APIRouter, Body, status, HTTPException
from pydantic import UUID4

from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependences import DatabaseDependency

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from fastapi_pagination import Page, paginate

router = APIRouter()

@router.post(
    '/', 
    summary='Criar novo Centro de Treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut
)
async def post(
    db_session: DatabaseDependency, 
    centro_treinamento_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:
    
    try:
        centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
        centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())
    
        # breakpoint()        
        db_session.add(centro_treinamento_model)
        await db_session.commit()
        
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um centro de treinamento cadastrado com o nome: {centro_treinamento_in.nome}',
        )        
    except Exception:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro ao inserir os dados no banco.',
        )       
    
    return centro_treinamento_out


@router.get(
    '/', 
    summary='Consultar todos os Centros de treinamento',
    status_code=status.HTTP_200_OK,
    response_model=Page[CentroTreinamentoOut],
)

async def query(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    centro_treinamentos: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    return paginate(centro_treinamentos)




@router.get(
    '/{id}', 
    summary='Consultar um Centro de treinamento por id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)

async def get(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    
    centro_treinamento: CentroTreinamentoOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Centro de treinamento não encontrado com o id: {id}',
        )
    
    return centro_treinamento