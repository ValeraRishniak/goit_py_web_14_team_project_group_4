import cloudinary
import qrcode
from io import BytesIO

from sqlalchemy.orm import Session

from app.database.models import Image, User
from app.conf.config import config_cloudinary
from app.schemas.transform import TransformBodyModel


async def transform_method(
    photo_id: int, body: TransformBodyModel, user: User, db: Session
) -> Image | None:
    """
    The transform_method function creates a transformation list that will be used to transform the image using Cloudinary's API.
    The function then checks if each filter is being used by checking if its use_filter attribute is True or False.
    If True, it adds all of its attributes to the transformation list as parameters for Cloudinary's API call.

    :param photo_id: int: Get the photo from the database
    :param body: TransformBodyModel: Pass the data from the frontend to this function
    :param user: User: Get the user id from the logged in user
    :param db: Session: Access the database
    :return: The photo object with the new transform_url
    """
    photo = (
        db.query(Image).filter(Image.user_id == user.id, Image.id == photo_id).first()
    )
    if photo:
        transformation = []

        if body.circle.use_filter and body.circle.height and body.circle.width:
            trans_list = [
                {
                    "gravity": "face",
                    "height": f"{body.circle.height}",
                    "width": f"{body.circle.width}",
                    "crop": "thumb",
                },
                {"radius": "max"},
            ]
            [transformation.append(elem) for elem in trans_list]

        if body.effect.use_filter:
            effect = ""
            if body.effect.art_audrey:
                effect = "art:audrey"
            if body.effect.art_zorro:
                effect = "art:zorro"
            if body.effect.blur:
                effect = "blur:300"
            if body.effect.cartoonify:
                effect = "cartoonify"
            if effect:
                transformation.append({"effect": f"{effect}"})

        if body.resize.use_filter and body.resize.height and body.resize.height:
            crop = ""
            if body.resize.crop:
                crop = "crop"
            if body.resize.fill:
                crop = "fill"
            if crop:
                trans_list = [
                    {
                        "gravity": "auto",
                        "height": f"{body.resize.height}",
                        "width": f"{body.resize.width}",
                        "crop": f"{crop}",
                    }
                ]
                [transformation.append(elem) for elem in trans_list]

        if body.text.use_filter and body.text.font_size and body.text.text:
            trans_list = [
                {
                    "color": "#FFFF00",
                    "overlay": {
                        "font_family": "Times",
                        "font_size": f"{body.text.font_size}",
                        "font_weight": "bold",
                        "text": f"{body.text.text}",
                    },
                },
                {"flags": "layer_apply", "gravity": "south", "y": 20},
            ]
            [transformation.append(elem) for elem in trans_list]

        if body.rotate.use_filter and body.rotate.width and body.rotate.degree:
            trans_list = [
                {"width": f"{body.rotate.width}", "crop": "scale"},
                {"angle": "vflip"},
                {"angle": f"{body.rotate.degree}"},
            ]
            [transformation.append(elem) for elem in trans_list]

        if transformation:
            config_cloudinary()
            url = cloudinary.CloudinaryImage(photo.public_id).build_url(
                transformation=transformation
            )
            photo.transform_url = url
            db.commit()

        return photo


async def show_qr(photo_id: int, user: User, db: Session) -> Image | None:
    """
    The show_qr function takes a photo_id and user, and returns an image of the QR code for that photo.

    :param photo_id: int: Get the photo from the database
    :param user: User: Get the user's id
    :param db: Session: Pass the database session to the function
    :return: A buffer, which is a memory-only file
    """
    photo = (
        db.query(Image).filter(Image.user_id == user.id, Image.id == photo_id).first()
    )
    if photo:
        if photo.transform_url:
            qr = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(photo.transform_url)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            qr_img.save(buffer)
            buffer.seek(0)

            return buffer
