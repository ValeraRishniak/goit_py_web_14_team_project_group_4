import unittest
from unittest.mock import MagicMock
from datetime import date, timedelta

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.repository.photo import get_photos,   get_my_photos,  get_photo_by_id , create_photo , update_description , remove_photo
 

from app.database.models import Image, User, Role
from app.schemas.photo import    ImageModel 


class TestContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        
     
    async def test_get_photos(self):
        photo = [Image(), Image(), Image()]
        self.session.query().offset().limit().all.return_value = photo
        result = await get_photos( skip=0, limit=10, user= self.user, db=self.session )
        self.assertEqual(result, photo)
        

        
    # async def test_get_photo(self):
    #     photo_id = 1
    #     photka = Image( id=photo_id, user_id=self.user.id)
    #     self.session.query(Image).filter_by(and_(Image.id == photo_id, Image.user_id == self.user.id)).first.return_value = photka
    #     result = await get_my_photos(photo_id=photo_id , user=self.user, db=self.session)
    #     self.assertEqual(result,  photka )

    # async def test_if_get_my_photos_not_found(self):
    #     self.session.query().filter_by().first.return_value = None
    #     result = await get_my_photos(photo_id=1, user=self.user, db=self.session)
    #     self.assertIsNone(result)
        
    # async def test_get_photo_by_id(self):
    #     photo_id = 1
    #     photka = Image( id=photo_id, user_id=self.user.id)
    #     self.session.query(Image).filter_by(and_(Image.id == photo_id, Image.user_id == self.user.id)).first.return_value = photka
    #     result = await get_photo_by_id(photo_id=photo_id , user=self.user, db=self.session)
    #     self.assertEqual(result,  photka )

    # async def test_if_get_photo_by_id_not_found(self):
    #     self.session.query().filter_by().first.return_value = None
    #     result = await get_photo_by_id(photo_id=1, user=self.user, db=self.session)
    #     self.assertIsNone(result)

    # async def test_create_photo(self):
    #     body = ImageModel( description = 'new foto fo you'   , url= "http://console.cloudinary.com/console/c-d8a03b96ed427346604eac79aeea58/media_library/homepage/asset/e6cfb21987e391a9c999f7a8fd6ddc51/manage?context=manage", 
    #                         # name='prosto',
    #                         id= self.user.id,
    #                         tags = [] )
          
    #     result = await create_photo(body=body, db=self.session, user=self.user)
    #     self.assertEqual(result.description, body.description)
    #     self.assertEqual(result.image, body.url)
    #     self.assertEqual(result.tags, body.tags)
    #     self.assertEqual(result.user_id, self.user.id)
    #     self.assertTrue(hasattr(result, "id"))
 

    # async def test_remove_photo(self):
    #     contact = Image()
    #     self.session.query().filter().first.return_value = contact
    #     result = await remove_photo(photo_id=1, user=self.user, db=self.session)
    #     self.assertEqual(result, contact)

    # async def test_remove_photo_not_found(self):
    #     self.session.query().filter().first.return_value = None
    #     result = await remove_photo(photo_id=1, user=self.user, db=self.session)
    #     self.assertIsNone(result)

    # async def test_update_description_found(self):
    #     photo_id = 1
    #     body = ImageModel( description = 'new foto fo you'   , image_url= "http://console.cloudinary.com/console/c-d8a03b96ed427346604eac79aeea58/media_library/homepage/asset/e6cfb21987e391a9c999f7a8fd6ddc51/manage?context=manage", 
    #                         title='prosto', id= 1, role= Role.admin, 
    #                         tags = [] )

    #     phot  = Image( description = 'foto1'    ,  image_url= "http://console.cloudinary.com/console/c-d8a03b96ed427346604eac79aeea58/media_library/homepage/asset/e6cfb21987e391a9c999f7a8fd6ddc51/manage?context=manage", 
                         
    #                         id=1,
    #                         tags = [] )

    #     self.session.query().filter_by().first.return_value  = phot
    #     self.session.commit.return_value = None
    #     result = await update_description(photo_id= 1,body=body,  db=self.session, user= self.user.id)
    
    #     self.assertEqual(result.description, body.description)
     
    #     self.assertTrue(hasattr(result, "id"))

    # async def test_update_description_not_found(self):
    #     body = ImageModel( description = 'new foto fo you'   , url= "http://console.cloudinary.com/console/c-d8a03b96ed427346604eac79aeea58/media_library/homepage/asset/e6cfb21987e391a9c999f7a8fd6ddc51/manage?context=manage", 
    #                         name='prosto', id= 1,
    #                         tags = [])
    #     self.session.query().filter_by().first.return_value = None
    #     self.session.commit.return_value = None
    #     result = await update_description(photo_id=1, body=body, user=self.user, db=self.session)
    #     self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
