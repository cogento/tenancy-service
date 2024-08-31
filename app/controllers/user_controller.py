from cogento_core.db.models import User
from fastapi import APIRouter, Depends
from repositories.base_repositories import UserRepository
from repositories.user_repository import SqlUserRepository
from starlette import status

router = APIRouter(
    prefix="/user",
    tags=["users"]
)


@router.get(
    path="/{user_id}",
    operation_id="get_user_by_id",
    description="Get User by ID",
    status_code=status.HTTP_200_OK,
    response_model=User
)
def get_user(user_id: int, user_repo: UserRepository = Depends(SqlUserRepository.get)) -> User:
    """
    Get a user by id
    :return: user
    """
    return user_repo.get_by_id(user_id=user_id)


@router.get(
    path="/email/{email}",
    operation_id="get_user_by_email",
    description="Get User by Email",
    status_code=status.HTTP_200_OK,
    response_model=User
)
def get_user_by_email(email: str, user_repo: UserRepository = Depends(SqlUserRepository.get)) -> User:
    """
    Get a user by email
    :return: user
    """
    return user_repo.get_by_email(email=email)


@router.get(
    path="/list/{company_id}",
    operation_id="list_users",
    description="Get All Users by Company ID",
    status_code=status.HTTP_200_OK,
    response_model=User
)
def list_users(company_id: int, user_repo: UserRepository = Depends(SqlUserRepository.get)) -> User:
    """
    Get all users by company id
    :return: users
    """
    return user_repo.get_by_company(company_id=company_id)


@router.post(
    path="/",
    operation_id="create_user",
    description="Create User",
    status_code=status.HTTP_201_CREATED,
    response_model=User
)
def create_user(user: User, user_repo: UserRepository = Depends(SqlUserRepository.get)) -> User:
    """
    Create a user
    :param user:
    :param user_repo:
    :return:
    """
    return user_repo.create(user=user)
