# from typing import List
# from datetime import date, timedelta
# from sqlalchemy.orm import Session
# from sqlalchemy import and_, extract, or_, select
# import cloudinary
# import cloudinary.uploader
# import uuid
# import qrcode
# import os

# from fastapi import File, HTTPException, status

# import cloudinary
# import cloudinary.uploader
# import shutil
# from app.conf.config import config_cloudinary

# from app.database.models import   User, Image, QR_code
# from app.services.photo import validate_crop_mode, validate_gravity_mode

# # result = cloudinary.uploader.upload("https://upload.wikimedia.org/wikipedia/commons/a/ae/Olympic_flag.jpg", public_id = "olympic_flag")
# # url = result.get('url')
# # https://console.cloudinary.com/console/c-d8a03b96ed427346604eac79aeea58/media_library/homepage/asset/e6cfb21987e391a9c999f7a8fd6ddc51/manage?context=manage

# async def add_photo( photo:File(),
#                  #    user: User,
#                     db: Session,
#                     name: str | None = None,
#                     description: str | None = None,
#                     tags: List[str] | None = None,
#                     width: int | None = None,
#                     height: int | None = None,
#                     crop_mode: str | None = None,
#                     rounding: int | None = None,
#                     background_color : str | None = None,
#                     rotation_angle: int | None = None,
#                     ) -> Image:


#     config_cloudinary()

#     uploaded_file_info = cloudinary.uploader.upload(photo.file, **transformations)

#     photo_url = uploaded_file_info["secure_url"]

#     if validate_crop_mode(crop_mode):
#         transformations = {
#             "width": width,
#             "height": height,
#             "crop": crop_mode,
#             "radius": rounding,
#             "background": background_color,
#             "angle": rotation_angle,
#         }
#     else:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

#     photo = Image(
#         url=photo_url,
#         name= name,
#         description=description,
#         # user_id=user.id,
#         tags=tags,
#     )
#     try:
#         db.add(photo)
#         await db.commit()
#         await db.refresh(photo)
#     except Exception as e:
#         await db.rollback()
#         raise e

#     return photo

# async def get_URL_QR(photo_id: int, db: Session):

#     query = select(Image).filter(Image.id == photo_id)
#     result = await db.execute(query)
#     photo = result.scalar()

#     if photo is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

#     query = select(QR_code).filter(QR_code.photo_id == photo_id)
#     result = await db.execute(query)
#     qr = result.scalar_one_or_none()

#     if qr is None:
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )

#         qr.add_data(photo.url)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")

#         qr_code_file_path = "my_qr_code.png"
#         img.save(qr_code_file_path)

#         config_cloudinary()
#         upload_result = cloudinary.uploader.upload(
#             qr_code_file_path,
#             public_id=f"Qr_Code/Photo_{photo_id}",
#             overwrite=True,
#             invalidate=True,
#         )
#         qr = QR_code(url=upload_result["secure_url"], photo_id=photo_id)

#         try:
#             db.add(qr)
#             await db.commit()
#             db.refresh(qr)
#         except Exception as e:
#             await db.rollback()
#             raise e

#         os.remove(qr_code_file_path)
#         return {"source_url": photo.url, "qr_code_url": qr.url}

#     return {"source_url": photo.url, "qr_code_url": qr.url}
