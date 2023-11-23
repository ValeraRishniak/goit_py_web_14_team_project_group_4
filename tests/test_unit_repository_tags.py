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

from app.database.models import Image, ImageComment, User, ImageTag
from app.schemas.comment import CommentBase

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.repository.tags import    create_tag, remove_tag, get_tags, get_tag_by_id,  update_tag

from app.database.models import Image, User, Role
from app.schemas.photo import    ImageModel 
from typing import List

from sqlalchemy.orm import Session

from app.database.models import ImageTag
from app.schemas.tags import ImageTagModel



class TestContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        
   
    async def test_get_tags(self):
        ta = [ImageTag(), ImageTag(), ImageTag()]
        self.session.query().offset().limit().all.return_value = ta
        
        result = await get_tags(   skip=0, limit=10,  db=self.session)
        self.assertEqual(result, ta)   
        
      
    async def test_get_get_tag_by_id(self):
        tag_id = 1
        tagg = ImageTag( id=tag_id )
        self.session.query().filter().first.return_value   = tagg
        result = await get_tag_by_id(tag_id=tag_id ,  db=self.session)
        self.assertEqual(result.id,  tagg.id )

    async def test_if_get_tag_by_id_not_found(self):
        tag_id = 1
        self.session.query().filter().first.return_value = None
        result = await get_tag_by_id(tag_id=tag_id ,   db=self.session)
        self.assertIsNone(result)

   

    async def test_remove_tag(self):
        contact = ImageTag()
        self.session.query().filter().first.return_value = contact
        result = await remove_tag(tag_id=1,  db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_tag_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_tag(tag_id=1,   db=self.session)
        self.assertIsNone(result)

    
if __name__ == '__main__':
    unittest.main()
