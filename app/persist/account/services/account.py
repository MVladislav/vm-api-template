import logging
from datetime import datetime, timedelta

from app.db.mongoDb import DBConnection
from app.persist.account.models.user import UserEntity, UserStatusEnum
from app.persist.account.schemas.request import (RequestLoginSchema,
                                                 RequestRegistrationSchema)
from app.persist.account.schemas.response import (
    ResponseLoginResultSchema, ResponseRegistrationResultSchema)
from app.utils.api.helper import createQrCode, validateEmail
from app.utils.api.responseHelper import (ErrorTypeEnum, MsgTypeEnum,
                                          ResponseHandlerObject,
                                          ResponseHolderObject,
                                          responseHandler)
from app.utils.api.securityHelper import (TokenDataObject, create_access_token,
                                          get_password_hash, totpCreate,
                                          totpVerify, verify_password)
from app.utils.config import (ACCOUNT_REGISTER_EXPIRE_MINUTES, PROJECT_NAME,
                              TOTP_ACTIVE)
from bson.objectid import ObjectId

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------

DB_TABLE = "account"
conn = DBConnection()


# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


async def registration(params: RequestRegistrationSchema) -> ResponseHolderObject:
    name = params.name
    surname = params.surname
    username = params.username
    password = params.password
    email = params.email

    try:
        if name is not None and surname is not None and username is not None \
                and password is not None and email is not None:
            if validateEmail(email):
                # search for user by existing username, if exist the user should try with other username
                user: UserEntity = conn.find_one(filter={"username": username},
                                                 entity=UserEntity, table_name=DB_TABLE)

                # if the username is free start creating the user
                if user is None:
                    # create the 2FA credentials
                    secret = totpCreate() if TOTP_ACTIVE else None

                    expireTime: int = ACCOUNT_REGISTER_EXPIRE_MINUTES  # here defined in minutes
                    expireDate = (datetime.now() + timedelta(minutes=expireTime)).timestamp()

                    # create and save the user
                    user = UserEntity(
                        name=name,
                        surname=surname,
                        username=username,
                        password=get_password_hash(password),
                        totpToken=secret.secret if TOTP_ACTIVE else None,
                        accountExpireDate=datetime.fromtimestamp(expireDate),
                        email=email,
                        status=UserStatusEnum.NEW,
                    )
                    conn.insert_one(obj=user, table_name=DB_TABLE)

                    # if user is created/saved, create the qrcode for the user
                    # for the 2FA
                    if user is not None:
                        try:
                            user.token = create_access_token(
                                data=TokenDataObject(
                                    id=str(user.id),
                                    username=user.username,
                                    isAdmin=False
                                )
                            ).access_token
                        except Exception as ex:
                            logging.log(logging.ERROR, ex)
                        if user.token is not None:
                            otp_auth_url = secret.provisioning_uri(
                                name=username,
                                issuer_name=PROJECT_NAME
                            ) if user.totpToken is not None else None
                            if otp_auth_url is not None or user.totpToken is None:
                                qrCodeSVG = createQrCode(otp_auth_url) if user.totpToken is not None else None

                                # ==> Here will response the best result, the other are warnings and errors
                                return responseHandler(
                                    [
                                        ResponseHandlerObject(
                                            msgType=MsgTypeEnum.RESULT,
                                            msg=ResponseRegistrationResultSchema(
                                                qrCode=qrCodeSVG if user.totpToken is not None else None,
                                                secret=secret.secret if user.totpToken is not None else None,
                                                expireTime=f"{expireTime}m",
                                                expireDate=user.accountExpireDate,
                                            ),
                                        ),
                                    ],
                                    200
                                )
                            else:
                                await remove(TokenDataObject(id=str(user.id),
                                                             username=user.username))
                                return responseHandler(
                                    [
                                        ResponseHandlerObject(msgType=MsgTypeEnum.ERROR,
                                                              msg="user saving failed!"),
                                        ResponseHandlerObject(msgType=MsgTypeEnum.STATE,
                                                              msg="QR_CODE_FAILED"),
                                    ],
                                    400
                                )
                        else:
                            await remove(TokenDataObject(id=str(user.id), username=user.username))
                            return responseHandler(
                                [
                                    ResponseHandlerObject(msgType=MsgTypeEnum.ERROR,
                                                          msg="user saving failed!"),
                                    ResponseHandlerObject(msgType=MsgTypeEnum.STATE,
                                                          msg="TOKEN_FAILED"),
                                ],
                                400
                            )
                    else:
                        return responseHandler(
                            [
                                ResponseHandlerObject(msgType=MsgTypeEnum.ERROR,
                                                      msg="user saving failed!"),
                                ResponseHandlerObject(msgType=MsgTypeEnum.STATE,
                                                      msg="USER_FAILED"),
                            ],
                            400
                        )
                else:
                    logging.log(
                        logging.NOTICE,
                        f"tried to create account where username already exist:: {username}"
                    )
                    return responseHandler(
                        [
                            ResponseHandlerObject(
                                msgType=MsgTypeEnum.ERROR,
                                msg="you can not use this username, choose any other :P")
                        ],
                        400
                    )
            else:
                return responseHandler(
                    [
                        ResponseHandlerObject(msgType=MsgTypeEnum.ERROR,
                                              msg="the E-Mail address is not valid")
                    ],
                    400
                )
        else:
            return responseHandler(
                [
                    ResponseHandlerObject(
                        msgType=MsgTypeEnum.ERROR,
                        msg="please fill name, surname, username, password and email")
                ],
                400
            )
    except Exception as ex:
        logging.log(logging.ERROR, ex)
    return None

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


async def login(params: RequestLoginSchema) -> ResponseHolderObject:
    authCode = params.authCode
    username = params.username
    password = params.password

    try:
        # check if all needed value are available
        if (authCode is not None or TOTP_ACTIVE is False) and username is not None and password is not None:
            # get user by username and check next if valid passwd
            user: UserEntity = conn.find_one(
                filter={"username": username}, entity=UserEntity, table_name=DB_TABLE)

            if user is not None:
                # check if for username, the password is correct
                if verify_password(password, user.password):
                    # check totp
                    is_totp_verify = totpVerify(user.totpToken, authCode) if user.totpToken is not None else True
                    # => first check, if the user is a new one and if the expire date is not outdated
                    if user is not None and is_totp_verify:
                        # check if it is first login after creating account, to set the user active or remove after expire time
                        if user.status == UserStatusEnum.NEW and user.accountExpireDate is not None and user.accountExpireDate >= datetime.now():
                            token = create_access_token(data=TokenDataObject(
                                id=str(user.id), username=user.username, isAdmin=False)).access_token
                            user = conn.find_and_modify(
                                id=user.id, update={"accountExpireDate": None,
                                                    "status": UserStatusEnum.ACTIVE,
                                                    "lastLogin": datetime.now(),
                                                    "token": token}, entity=UserEntity, table_name=DB_TABLE)
                        # if expired, remove the user and return with that info
                        elif user.status == UserStatusEnum.NEW and user.accountExpireDate is not None and user.accountExpireDate < datetime.now():
                            conn.remove(user.id, DB_TABLE)
                            return responseHandler([ResponseHandlerObject(msgType=MsgTypeEnum.ERROR,
                                                                          msg="your registration is expired")], 400)

                        # if user is valid and has an account, go on and verify basic login
                        if user is not None:
                            # check if user is active and 2FA is valid, if yes return user info and TOKEN
                            if user.status == UserStatusEnum.ACTIVE:
                                conn.find_and_modify(id=user.id, update={
                                                     "lastLogin": datetime.now()},
                                                     entity=UserEntity,
                                                     table_name=DB_TABLE
                                                     )
                                return responseHandler(
                                    [
                                        ResponseHandlerObject(
                                            msgType=MsgTypeEnum.RESULT,
                                            msg=ResponseLoginResultSchema(
                                                username=user.username,
                                                firstName=user.name,
                                                lastName=user.surname,
                                                email=user.email,
                                                token=user.token,
                                            ),
                                        ),
                                        ResponseHandlerObject(
                                            msgType=MsgTypeEnum.STATE, errorType=ErrorTypeEnum.ACCESS_GRANT),
                                    ],
                                    200
                                )
                            else:
                                logging.log(
                                    logging.WARNING, f"user tried loggin to account which is not active: '{username}'")
                                return responseHandler(
                                    [
                                        ResponseHandlerObject(
                                            msgType=MsgTypeEnum.ERROR, msg="account is not active"),
                                        ResponseHandlerObject(
                                            msgType=MsgTypeEnum.STATE, errorType=ErrorTypeEnum.ACCESS_DECLINE),
                                    ],
                                    401
                                )
                        else:
                            logging.log(
                                logging.WARNING, f"user entity was null (maybe after first registration): '{username}'")
                            return responseHandler(
                                [
                                    ResponseHandlerObject(
                                        msgType=MsgTypeEnum.ERROR, errorType=ErrorTypeEnum.ACCESS_FAILED),
                                    ResponseHandlerObject(
                                        msgType=MsgTypeEnum.STATE, errorType=ErrorTypeEnum.ACCESS_DECLINE),
                                ],
                                401
                            )
                    else:
                        logging.log(logging.WARNING, f"totp verification failed: '{username}'")
                        return responseHandler(
                            [
                                ResponseHandlerObject(msgType=MsgTypeEnum.ERROR,
                                                      errorType=ErrorTypeEnum.TOTP_DECLINE),
                                ResponseHandlerObject(msgType=MsgTypeEnum.STATE,
                                                      errorType=ErrorTypeEnum.ACCESS_DECLINE),
                            ],
                            401
                        )
                else:
                    logging.log(
                        logging.WARNING, f"verify_password failed, has no more access or user has no totp: '{username}'")
                    return responseHandler(
                        [
                            ResponseHandlerObject(msgType=MsgTypeEnum.ERROR,
                                                  errorType=ErrorTypeEnum.ACCESS_FAILED),
                            ResponseHandlerObject(msgType=MsgTypeEnum.STATE,
                                                  errorType=ErrorTypeEnum.ACCESS_DECLINE),
                        ],
                        401
                    )
            else:
                logging.log(logging.WARNING, f"requested user did not exists: '{username}'")
                return responseHandler(
                    [
                        ResponseHandlerObject(msgType=MsgTypeEnum.ERROR,
                                              errorType=ErrorTypeEnum.ACCESS_FAILED),
                        ResponseHandlerObject(msgType=MsgTypeEnum.STATE,
                                              errorType=ErrorTypeEnum.ACCESS_DECLINE),
                    ],
                    401
                )
        else:
            return responseHandler([ResponseHandlerObject(msgType=MsgTypeEnum.ERROR,
                                                          msg="please fill authCode, username and password")], 400)

    except Exception as ex:
        logging.log(logging.ERROR, ex)
    return None

# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


async def remove(params: TokenDataObject) -> ResponseHolderObject:
    id = params.id
    username = params.username
    # isAdmin = params.isAdmin

    try:
        # check if all needed value are available
        if id is not None and username is not None:
            # get user by username and check next if valid passwd
            user: UserEntity = conn.find_one(filter={"_id": ObjectId(
                id), "username": username}, entity=UserEntity, table_name=DB_TABLE)

            # check if user is active
            if user is not None:  # and user.status == UserStatusEnum.ACTIVE:
                conn.remove(id=user.id,  table_name=DB_TABLE)
                return responseHandler(
                    [
                        ResponseHandlerObject(msgType=MsgTypeEnum.RESULT, msg="user removed"),
                        ResponseHandlerObject(msgType=MsgTypeEnum.STATE,
                                              errorType=ErrorTypeEnum.REMOVED),
                    ],
                    200
                )
            else:
                return responseHandler(
                    [
                        ResponseHandlerObject(msgType=MsgTypeEnum.ERROR,
                                              errorType=ErrorTypeEnum.ACCESS_FAILED),
                        ResponseHandlerObject(msgType=MsgTypeEnum.STATE,
                                              errorType=ErrorTypeEnum.ACCESS_DECLINE),
                    ],
                    401
                )
        else:
            return responseHandler([ResponseHandlerObject(msgType=MsgTypeEnum.ERROR,
                                                          msg="missing attributes from token")], 400)

    except Exception as ex:
        logging.log(logging.ERROR, ex)
    return None
