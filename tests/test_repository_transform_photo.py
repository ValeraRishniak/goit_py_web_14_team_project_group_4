import unittest
from unittest.mock import MagicMock
from datetime import date, timedelta

from sqlalchemy import and_
from sqlalchemy.orm import Session

import cloudinary
import qrcode
from io import BytesIO


from app.repository.transform_photo import  transform_method, show_qr
 

from app.database.models import Image, User
from app.schemas.photo import    ImageModel 
from app.schemas.transform import TransformBodyModel









