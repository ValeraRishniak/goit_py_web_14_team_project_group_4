import unittest
import os
import sys
from unittest.mock import MagicMock
from datetime import date, timedelta
import cloudinary
import cloudinary.uploader
from app.conf.config import config_cloudinary
from fastapi import UploadFile
from uuid import uuid4
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.database.models import Image, ImageComment, User
from app.schemas.comment import CommentBase

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.repository.comment import   create_comment, delete_comment , show_single_comment, show_my_comments, show_user_photo_comments

from app.database.models import Image, User, Role
from app.schemas.photo import    ImageModel 


class TestContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        
    async def test_create_comment(self):           
        coment  = CommentBase (comment_description="password12")
        image = Image(id=1)
        user = User(id=1)
        self.session.add.return_value = None
        self.session.commit.return_value = None
        self.session.refresh.return_value = None

        result = await create_comment(image_id=image.id, body=coment, user=user,  db=self.session)
        self.assertTrue(type(result), list)
    
    async def test_delete_comment(self):
            comment_id  = 1
            user_id = 1 
            user1 = User(id=1)
            coment = ImageComment(comment_description="asaaaaaaa",id=comment_id )
            self.session.query().filter().first.return_value = coment
            result = await delete_comment( comment_id = comment_id, user=user1, db=self.session)
            self.assertEqual(result, coment)

    #  
    async def test_delete_comment_not_found(self):
        comment_id  = 1
        user_id = 1 
        user1 = User(id=1)
        coment = ImageComment(comment_description="asaaaaaaa",id=comment_id )
        self.session.query().filter().first.return_value =   None
        result = await delete_comment( comment_id=1,  user=user1,    db=self.session)
        self.assertIsNone(result, )
     
     
     
    async def test_show_single_comment(self):
        comment_id  = 1
        user_id = 1 
        user1 = User(id=1)
        coment = ImageComment(comment_description="asaaaaaaa",id=comment_id )
        self.session.query().filter().first.return_value   = coment
        result = await show_single_comment(comment_id=comment_id , user=self.user, db=self.session)
        self.assertEqual(result.id,  coment.id )

    async def test_if_show_single_comment_not_found(self):
        comment_id  = 1
        self.session.query().filter().first.return_value = None
        result = await show_single_comment(comment_id=comment_id , user=self.user, db=self.session)
        self.assertIsNone(result)
    
    
    async def test_show_my_comments(self):
        imadge_id = 0
        user_id=1
        coment = ImageComment(user_id=user_id, image_id= imadge_id)
        self.session.query().filter().first.return_value = coment
        # self.session.query(ImageComment).filter(and_(ImageComment.image_id == 2, ImageComment.user_id == user_id)).all().return_value = coment
        result = await show_my_comments(user_id=user_id, image_id= imadge_id, db=self.session)
      
        self.assertEqual(len(result)   , coment.image_id  )
     
 
      
      
if __name__ == '__main__':
      unittest.main()  
        