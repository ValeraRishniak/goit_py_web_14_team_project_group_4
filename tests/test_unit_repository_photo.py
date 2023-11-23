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

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.repository.photo import  get_my_photos, get_photo_by_id,  update_description, remove_photo
 

from app.database.models import Image, User, Role
from app.schemas.photo import    ImageModel 


class TestContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        
   
        
    async def test_get_photo(self):
        photo_id = 0
        photka = Image( id=photo_id, user_id=self.user.id)
        self.session.query(Image).filter_by(and_(Image.id == photo_id, Image.user_id == self.user.id)).first.return_value = photka
        result = await get_my_photos( skip=0, limit=10,   user=self.user, db=self.session)
        self.assertEqual(len(result),  photka.id )
        

    async def test_if_get_my_photos_not_found(self):
        user = User(id=0)
        self.session.query().filter_by().first.return_value = None
        result = await get_my_photos(skip=0, limit=10,  user= user, db=self.session)
        self.assertEqual(len(result),0)
        
    async def test_get_photo_by_id(self):
        photo_id = 1
        photka = Image( id=photo_id, user_id=self.user.id)
        self.session.query().filter().first.return_value   = photka
        result = await get_photo_by_id(photo_id=photo_id , user=self.user, db=self.session)
        self.assertEqual(result.id,  photka.id )

    async def test_if_get_photo_by_id_not_found(self):
        photo_id = 1
        self.session.query().filter().first.return_value = None
        result = await get_photo_by_id(photo_id=photo_id, user=self.user, db=self.session)
        self.assertIsNone(result)

   

    async def test_remove_photo(self):
        contact = Image()
        self.session.query().filter().first.return_value = contact
        result = await remove_photo(photo_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_photo_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_photo(photo_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_description_found(self):
        photo_id = 1
        user = User(id=1)
        description = 'new foto fo you'
        body = ImageModel( description = description  , image_url= "ht omepa ", title='prosto', id= 1, role= Role.admin, tags = [] )
        result = await update_description(photo_id= photo_id, title=body.title, description=body.description, tags=body.tags ,  db=self.session, user= user)
        self.assertTrue(hasattr(result, description))

    async def test_update_description_not_found(self):
        photo_id = 1
        user = User(id=1)
        description = 'new foto fo you'
        body = ImageModel( description = description  , image_url= "ht omepa ", title='prosto', id= 1, role= Role.admin, tags = [] )
        self.session.query().filter_by().first.return_value = None
        self.session.commit.return_value = None
        result = await update_description(photo_id= photo_id, title=body.title, description=body.description, tags=body.tags ,  db=self.session, user= user)
        self.assertEqual(len(result.description),0)

if __name__ == '__main__':
    unittest.main()
