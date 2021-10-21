import logging
import re

import qrcode
import qrcode.image.svg
from app.utils.config import (QR_BORDER, QR_BOX_SIZE, QR_FACTORY, QR_FILLED,
                              QR_VERSION)

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


def validateEmail(mail: str) -> bool:
    try:
        regexp = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        x = re.match(regexp, mail)

        return bool(x)
    except Exception as ex:
        logging.log(logging.ERROR, ex)
    return False

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


def createQrCode(data: str) -> str:
    try:
        if QR_FACTORY is not None and QR_FACTORY == 'basic':
            # Simple factory, just a set of rects.
            if QR_FILLED:
                factory = qrcode.image.svg.SvgFillImage
            else:
                factory = qrcode.image.svg.SvgImage
        elif QR_FACTORY is not None and QR_FACTORY == 'fragment':
            # Fragment factory (also just a set of rects)
            factory = qrcode.image.svg.SvgFragmentImage
        else:
            # Combined path factory, fixes white space that may occur when zooming
            if QR_FILLED:
                factory = qrcode.image.svg.SvgPathFillImage
            else:
                factory = qrcode.image.svg.SvgPathImage

        qr = qrcode.QRCode(
            version=QR_VERSION,
            box_size=QR_BOX_SIZE,
            border=QR_BORDER, image_factory=factory
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        # svg_path = img.make_path()
        # svg_path = ET.tostring(svg_path)
        return img.to_string()
    except Exception as ex:
        logging.log(logging.ERROR, ex)
    return None
