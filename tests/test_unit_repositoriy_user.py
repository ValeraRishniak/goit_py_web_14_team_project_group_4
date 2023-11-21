import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.schemas.user import UserModel, UserDb
from app.database.models import User, Role
from app.repository.users import ( get_me, get_user_by_email, get_user_by_username, get_users, 
                                  create_user, create_admin_user, confirmed_email, update_avatar, 
                                  update_token,   delete_user, make_user_role, ban_user, razban_user)

class TestUsersRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

 
    
    async def test_get_me(self):
        id = 1
        username='Anton'
        email = "test_mail@example.com"
        user = User(email=email, id=id)
        self.session.query(User).filter_by(and_(User.email==email, User.id==self.id)).first.return_value= user
        result = await get_me(  user=self, db=self.session)
    
    async def test_get_user_by_email(self):
        email = "test_mail@example.com"
        user = User(id=1,  email=email)
        self.session.query().filter_by().first.return_value = user

        result = await get_user_by_email(email=email, db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_nonexistent(self):
        user_email = "non_existent_mail@example.com"
        self.session.query().filter_by().first.return_value = None

        result = await get_user_by_email(email=user_email, db=self.session)
        self.assertIsNone(result)
   
    async def test_get_user_by_username(self):
        # email = "test_mail@example.com"
        username_new='Anton'
        user1 = User(username=username_new)
        self.session.scalar.return_value = user1
       
        result = await get_user_by_username(username=username_new, db=self.session)
      
        self.assertEqual(result , user1 )
   
    async def test_get_user_by_username_nonexistent(self):
        username = "non_Anton"
        self.session.scalar.return_value = None
        result = await get_user_by_username(username=username, db=self.session)
        self.assertIsNone(result)
    
    async def test_get_users(self):
        users = [User(), User(), User()]
        self.session.query().offset().limit().all.return_value = users
        
        result = await get_users(   skip=0, limit=10,  db=self.session)
        self.assertEqual(result, users)

    async def test_create_user(self):
                       
        user_data = UserModel (username="nnnnnn", email="test@example.com", password="password12")
        new_user = User(id=1, email=user_data.email)
        self.session.add.return_value = None
        self.session.commit.return_value = None
        self.session.refresh.return_value = None

        result = await create_user(body=user_data, db=self.session)
        self.assertEqual(result.email, new_user.email)
        
    async def test_create_admin_user(self):
        user_data = UserModel (username="nnnnnn", email="test@example.com", password="password12")
        new_user = User(id=1, email=user_data.email, role= Role.admin)
        
        result = await create_admin_user(user=new_user, db=self.session)
        self.assertEqual(result.role, new_user.role)

    async def test_update_token(self):
        user = User(id=1,  email="test_mail@example.com")
        token = "new_refresh_token"
        self.session.commit.return_value = None
        self.session.refresh.return_value = None

        await update_token(user=user, token=token, db=self.session)
        self.assertEqual(user.refresh_token, token)

    async def test_confirmed_email(self):
        user_email = "test_mail@example.com"
        user = User(id=1,  email=user_email, confirmed=True)
        self.session.commit.return_value = None
        self.session.refresh.return_value = None

        await confirmed_email(email=user_email, db=self.session)
        self.assertTrue(user.confirmed)

    async def test_update_avatar(self):
        user_email = "test_mail@example.com"
        avatar_url = "https://fake.com/avatar.png"
        user2 = User(avatar=avatar_url)
        self.session.scalar.return_value = user2

        updated_user = await update_avatar(email=user_email,  url=avatar_url, db=self.session)
        self.assertEqual(updated_user.avatar, user2.avatar)
          
    async def test_delete_user(self):
            user_id = 1
            user1 = User(id=1)
            self.session.query().filter().first.return_value = user1
            result = await delete_user( user_id=user_id, db=self.session)
            self.assertEqual(result, None)

            
    async def test_remove_user_not_found(self):
        user1 = User(id=1)       
        self.session.query().filter().first.return_value = user1 
        result = await delete_user( user_id=1,     db=self.session)
        self.assertIsNone(result)
             
    async def test_make_user_role_found(self):
        user_email = "test_mail@example.com"
        rol = Role.admin
        user2 = User(role=rol, email=user_email)
       
        self.session.scalar.return_value = user2
      
        await make_user_role(user_email, rol, self.session)
        self.assertEqual(user2.role, rol)
     
    async  def test_ban_user(self):
        user_email = "test_mail@example.com"
        is_active = False
        user1 = User(is_active=is_active)
        self.session.scalar.return_value = user1
        
        result = await ban_user(user_email, db=self.session)

        self.assertEqual(user1.is_active, is_active)
    
    async def test_razban_user(self):
        user_email = "test_mail@example.com"
        is_active = True
        user1 = User(is_active=is_active)
        self.session.scalar.return_value = user1
       
        await razban_user(email=user_email, db=self.session)
      
        self.assertEqual(user1.is_active, is_active )  
        
if __name__ == '__main__':
    unittest.main()