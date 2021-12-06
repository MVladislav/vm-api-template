import logging
import os
import re
import smtplib
import socket
import ssl
import sys
import unicodedata
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from shutil import which
from subprocess import check_call
from typing import Any, List, Union
from urllib.parse import urlparse

from app.utils.config import settings


# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
def group(flat: List[Any], size: int) -> List[Any]:
    """
    group list a flat list into a matrix of "size"
    """
    return [flat[i: i + size] for i in range(0, len(flat), size)]


def normalize_caseless(text: str) -> str:
    """
    lowercase a string, for any unicode
    """
    return unicodedata.normalize("NFKD", text.casefold())


def slugify(value: Union[str, None], allow_unicode: bool = False) -> Union[str, None]:
    """
    https://github.com/django/django/blob/main/django/utils/text.py
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode(
            "ascii"
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")




# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
def in_sudo_mode() -> None:
    """
    If the user doesn't run the program with super user privileges, don't allow them to continue.
    """
    try:
        if "SUDO_UID" not in os.environ.keys():
            logging.log(logging.ERROR, "Try running this program with sudo.")
            sys.exit(1)
    except Exception as e:
        logging.log(logging.CRITICAL, e, exc_info=True)


def prompt_sudo() -> bool:
    """
    will prompt as for sudo root pw if user is not in sudo mode
    """
    try:
        if os.geteuid() != 0:
            msg = 'you run service with "-s" in "sudo" mode, you need enter sudo password to use some functions\n--> [sudo] password for %u: '
            return check_call(f'sudo -v -p "{msg}"', shell=True) == 0

        else:
            return True

    except Exception as e:
        logging.log(logging.CRITICAL, e, exc_info=True)
    return False


def is_tool(name: str) -> bool:
    """
    Check whether `name` is on PATH and marked as executable.
    """
    return which(name) is not None




# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
def geo() -> Union[str, None]:
    """
    This is a geo test example
    """
    try:
        from app.utils.locater import Locator
        return Locator().check_database()

    except Exception as e:
        logging.log(logging.CRITICAL, e, exc_info=True)
    return None


def get_ip_address() -> Union[str, None]:
    IP: Union[str, None] = None
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as st:
            st.connect(("10.255.255.255", 1))
            IP = st.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    return IP


def uri_validator(url: str) -> Union[str, None]:
    try:
        if url.endswith("/"):
            url = url[:-1]
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return url

    except Exception as e:
        logging.log(logging.WARNING, e)
    return None




# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
# async def send_email(
#     email_to: str,
#     subject_template: str = "",
#     html_template: str = "",
#     environment: Dict[str, Any] = {},
# ) -> None:
#     message = emails.Message(
#         subject=JinjaTemplate(subject_template),
#         html=JinjaTemplate(html_template),
#         mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
#     )
#     smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
#     if settings.SMTP_TLS:
#         smtp_options["tls"] = True
#     if settings.SMTP_USER:
#         smtp_options["user"] = settings.SMTP_USER
#     if settings.SMTP_PASSWORD:
#         smtp_options["password"] = settings.SMTP_PASSWORD
#     response = message.send(to=email_to, render=environment, smtp=smtp_options)
#     logging.info(f"send email result: {response}")
async def sendMail(
    email_to: Union[str, None],
    subject_template: Union[str, None],
    html_template: Union[str, None],
) -> None:
    """
        ...
    """
    try:
        if settings.SMTP_USER is None and settings.EMAILS_FROM_EMAIL is not None:
            settings.SMTP_USER = settings.EMAILS_FROM_EMAIL
        subtype: str = "html"  # plain | html
        if (
            email_to is not None and
            subject_template is not None and
            html_template is not None and
            settings.SMTP_PORT is not None and
            settings.SMTP_HOST is not None and
            settings.EMAILS_FROM_EMAIL is not None and
            settings.SMTP_PASSWORD is not None and
            settings.SMTP_USER is not None and
            settings.SMTP_PASSWORD is not None
        ):
            message = MIMEMultipart("alternative")
            message["To"] = email_to
            message["Subject"] = subject_template
            message.attach(MIMEText(html_template, subtype))
            message["From"] = settings.EMAILS_FROM_EMAIL
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(
                settings.SMTP_HOST, settings.SMTP_PORT, context=context
            ) as server:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(
                    from_addr=settings.EMAILS_FROM_EMAIL,
                    to_addrs=email_to,
                    msg=message.as_string(),
                )
        else:
            logging.log(logging.WARNING, "Not all mail values are set up!")
    except Exception as e:
        logging.log(logging.CRITICAL, e, exc_info=True)




# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
def define_option_list(
    options: str,
    default_options: List[Any] = [],
    options_append: bool = False,
    # default_split_by: str = ",",
) -> List[Any]:
    """
    defines a list of option to use in a callable service
    to define how to create this list
    by:
        - create it from a default only
        - create it from params only
        - create it by combine default and params
    """
    try:
        result: List[Any] = []
        # add options from params
        if options is not None and not options_append:
            result = [options]  # .split(default_split_by)
        # add options from params to existing options
        elif options is not None and options_append:
            result = default_options + [options]  # .split(default_split_by)
        # use existing options
        else:
            result = default_options
        return result

    except Exception as e:
        logging.log(logging.CRITICAL, e, exc_info=True)
    return []
