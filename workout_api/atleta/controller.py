from fastapi import APIRouter, Body, HTTPException, status

from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate, AtletaCustomizadoOut
from workout_api.atleta.models import AtletaModel
from workout_api.contrib.dependences import DatabaseDependency

from uuid import uuid4
from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from pydantic import UUID4

from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel

from fastapi_pagination import Page, paginate

router = APIRouter()

@router.post(
    '/', 
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post(
    db_session: DatabaseDependency, 
    atleta_in: AtletaIn = Body(...)
):
    
    # Tratando dados da Categoria
    categoria_nome = atleta_in.categoria.nome    
    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_nome))
    ).scalars().first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'A categoria {categoria_nome} não foi encontrada.',
        )   
    ##############################

    # Tratando dados do Centro de Treinamento
    centro_treinamento_nome = atleta_in.centro_treinamento.nome    
    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))
    ).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'O centro de treinamento {centro_treinamento_nome} não foi encontrado.',
        )   
    ##############################

    try:
        atleta_out = AtletaOut(
            id=uuid4(), 
            created_at=datetime.utcnow(),
            **atleta_in.model_dump()
        )
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria','centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id    
        
        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um atleta cadastrado com o CPF: {atleta_in.cpf}',
        )        
    except Exception:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro ao inserir os dados no banco.',
        )          
        
    return atleta_out



# Consulta todos os atletas:
@router.get(
    '/', 
    summary='Consultar todos os Atletas',
    status_code=status.HTTP_200_OK,
    response_model=Page[AtletaCustomizadoOut],
)
async def consulta_todos(db_session: DatabaseDependency) -> list[AtletaCustomizadoOut]:
    atletas: list[AtletaCustomizadoOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
    
    return paginate([AtletaCustomizadoOut.model_validate(atleta) for atleta in atletas])




@router.get(
    '/by-id', 
    summary='Consultar um Atleta por id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado com o id: {id}',
        )
    
    return atleta


# Consulta Atleta por nome:
@router.get(
    '/by-nome', 
    summary='Consultar um Atleta por nome',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def consulta_nome(nome: str, db_session: DatabaseDependency) -> AtletaOut:
    
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(nome=nome))
    ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado com o nome: {nome}',
        )
    
    return atleta


# Consulta Atleta por cpf:
@router.get(
    '/by-cpf', 
    summary='Consultar um Atleta por CPF',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def consulta_nome(cpf: str, db_session: DatabaseDependency) -> AtletaOut:
    
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(cpf=cpf))
    ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado com o cpf: {cpf}',
        )
    
    return atleta



@router.patch(
    '/{id}', 
    summary='Editar um Atleta (nome e idade) por id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado com o id: {id}',
        )
        
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)
        
    await db_session.commit()
    await db_session.refresh(atleta)
    
    return atleta



@router.delete(
    '/{id}', 
    summary='Remover um Atleta por id',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> None:
    
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado com o id: {id}',
        )
    
    await db_session.delete(atleta)
    await db_session.commit()    
    
