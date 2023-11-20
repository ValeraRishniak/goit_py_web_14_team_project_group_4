from typing import Any, List 
from fastapi import Depends, HTTPException, status, Request

from app.database.models import Role, User
from app.services.auth import auth_service

class RoleChecker():
    def __init__(self, allowed_roles: List[Role]):
        self.allwed_roles = allowed_roles

    async def __call__(self, request: Request, current_user: User = Depends(auth_service.get_current_user)):
        if current_user.role not in self.allwed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Operation forbiden, you do not have access rights")

Admin_Moder = RoleChecker([Role.admin, Role.moderator])
Admin = RoleChecker([Role.admin])
