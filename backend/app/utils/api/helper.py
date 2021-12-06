import logging
import re
from typing import Union

import qrcode
import qrcode.image.svg

from app.utils.config import settings


# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
def validateEmail(mail: str) -> bool:
    try:
        regexp = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        x = re.match(regexp, mail)
        return bool(x)

    except Exception as e:
        logging.log(logging.CRITICAL, e, exc_info=True)
    return False




# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
def createQrCode(data: str) -> Union[str, None]:
    try:
        if settings.QR_FACTORY is not None and settings.QR_FACTORY == "basic":
            # Simple factory, just a set of rects.
            if settings.QR_FILLED:
                factory = qrcode.image.svg.SvgFillImage
            else:
                factory = qrcode.image.svg.SvgImage
        elif settings.QR_FACTORY is not None and settings.QR_FACTORY == "fragment":
            # Fragment factory (also just a set of rects)
            factory = qrcode.image.svg.SvgFragmentImage
        else:
            # Combined path factory, fixes white space that may occur when zooming
            if settings.QR_FILLED:
                factory = qrcode.image.svg.SvgPathFillImage
            else:
                factory = qrcode.image.svg.SvgPathImage
        qr = qrcode.QRCode(
            version=settings.QR_VERSION,
            box_size=settings.QR_BOX_SIZE,
            border=settings.QR_BORDER,
            image_factory=factory,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        # svg_path = img.make_path()
        # svg_path = ET.tostring(svg_path)
        return str(img.to_string())

    except Exception as e:
        logging.log(logging.CRITICAL, e, exc_info=True)
    return None
