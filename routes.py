from fastapi import APIRouter, status, Response
import crud

router = APIRouter()


@router.post('/pynotify/key', status_code=status.HTTP_201_CREATED)
async def create_key(app: str):
    return await crud.create_key(app)


@router.post('/pynotify/user', status_code=status.HTTP_201_CREATED)
async def create_user(key: str, userid: int, response: Response):
    if await crud.is_key(key):
        return await crud.create_user(key, userid)
    
    response.status_code = status.HTTP_403_FORBIDDEN
    return {'error': 'invalid key'}

@router.delete('/pynotify/user', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str, key: str, response: Response):
    if await crud.is_key(key):
        if await crud.is_user(id, key):
            await crud.delete_user(id)
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'error': 'this user was created with a different key or user did not created'}
    else:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {'error': 'invalid key'}


@router.post('/pynotify/notify', status_code=status.HTTP_201_CREATED)
async def create_notify(key: str, user: int, message: str, response: Response):
    if await crud.is_key(key):
        if await crud.is_user(user, key):
            return await crud.create_notify(key, user, message)
        
        response.status_code = status.HTTP_403_FORBIDDEN 
        return {'error': 'this user was created with a different key or user did not created'}
    response.status_code = status.HTTP_403_FORBIDDEN
    return {'error': 'invalid key'}