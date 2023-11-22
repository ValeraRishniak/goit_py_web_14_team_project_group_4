from typing import List
from fastapi import Depends, HTTPException, status, Request

from app.database.models import Role, User
from app.services.auth import auth_service


class RoleChecker:
    def __init__(self, allowed_roles: List[Role]):
        """
        The __init__ function is called when the class is instantiated.
            It sets up the instance of the class with a list of allowed roles.
        
        :param self: Represent the instance of the class
        :param allowed_roles: List[Role]: Define the allowed roles for a user
        :return: The value of self
        """
        
        self.allowed_roles = allowed_roles

    async def __call__(
        self,
        request: Request,
        current_user: User = Depends(auth_service.get_current_user),
    ):
        """
        The __call__ function is a decorator that checks if the current user has access rights to perform an operation.
            If not, it raises an HTTPException with status code 403 and a detail message.
        
        :param self: Represent the instance of the class
        :param request: Request: Access the request object
        :param current_user: User: Get the current user
        :param : Get the current user from the database
        :return: The decorated function
        """

        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation forbidden, you don't have access rights",
            )


class RoleChecker:
    def __init__(self, allowed_roles: List[Role]):
        """
        The __init__ function is called when the class is instantiated.
            It sets up the instance of the class with a list of allowed roles.
        
        :param self: Represent the instance of the class
        :param allowed_roles: List[Role]: Define the allowed roles for this command
        :return: The class instance
        """

        self.allowed_roles = allowed_roles

    async def __call__(
        self,
        request: Request,
        current_user: User = Depends(auth_service.get_current_user),
    ):
        """
        The __call__ function is the actual decorator.
        It takes a function, adds some arguments, and returns a new function.
        The original function is available as __wrapped__ attribute of the returned function.
        
        :param self: Represent the instance of a class
        :param request: Request: Get the request object
        :param current_user: User: Get the current user
        :param : Get the current user from the database
        :return: A function that returns a response object
        """

        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation forbidden, you do not have access rights",
            )
