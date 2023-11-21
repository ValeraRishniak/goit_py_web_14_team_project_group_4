import unittest
from unittest.mock import MagicMock
from datetime import date, timedelta

from sqlalchemy import and_
from sqlalchemy.orm import Session

import cloudinary
import qrcode
from io import BytesIO


from app.repository.transform_photo import  transform_method, show_qr
 

from app.database.models import Image, User, Role, QR_code
from app.schemas.photo import    ImageModel 
from app.schemas.transform import TransformBodyModel


class TestContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
            
    async def test_transform_method(self):
        user_id = 1
        photo_id = 1
        body = TransformBodyModel( 
                                    circle= {"use_filter": False,"height": 400,"width": 400,},
                                    effect=  {"use_filter": False, "art_audrey": False, "art_zorro": False, "cartoonify": False, "blur": False },
                                    resize=  { "use_filter": False,    "crop": False,    "fill": False,    "height": 350,    "width": 350  }, 
                                    text=  {    "use_filter": False,    "font_size": 70,    "text": ""  }, 
                                    rotate={    "use_filter": False,    "width": 400,    "degree": 45  }
                                    )
        photo = Image(description = 'foto1',
                        image_url= "http://console.cloudinary.com/console/c-d8a03b96ed427346604eac79aeea58/media_library/homepage/asset/e6cfb21987e391a9c999f7a8fd6ddc51/manage?context=manage", 
                            title='prosto', user_id = 1, 
                                id=1,
                                tags = [])
        
        self.session.scalars.return_value.all.return_value = photo
        
       
        
        result = await transform_method( photo_id= photo_id, user=user_id,  db=self.session, body= body )
        
    #     self.assertEqual(result, photo)
    
    
    async def test_show_qr(self):
    
              photo = Image(id=1, image_url="photo_url")
    
              qr = QR_code(url="qr_code_url", id=1)
              self.session.scalar.return_value = qr
              
 
              photo_id = 1
              result = await show_qr(photo_id, user=self,  db=self.session ) 
              self.assertIsNotNone (result ) 

    
if __name__ == '__main__':
    unittest.main()


