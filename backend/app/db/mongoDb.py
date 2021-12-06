"""
    database connection handler for mongoDB
    with base class-object for creating new
    table-schemas.
    Use: 'DBConnection' in the code for
    handling connection
"""
import logging
import sys
from time import sleep
from typing import Any, Dict, Type, Union

import pymongo
import verboselogs
from bson.objectid import ObjectId
from pydantic.fields import Field
from pydantic.main import BaseConfig, BaseModel
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertOneResult

from app.utils.config import settings


# myquery = { "address": { "$regex": "^S" } }
# newvalues = { "$set": { "name": "Minnie" } }
# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
class PyObjectId(ObjectId):
    """
    mongDB id generator class
    used in 'MongoModel'
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, id):
        if not ObjectId.is_valid(id):
            raise ValueError("Invalid objectid")

        return ObjectId(id)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MongoModel(BaseModel):
    """
    base model config for creating new database model
    entities
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config(BaseConfig):
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {
            # datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid)
        }




# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
class DBConnector:
    """
    a "singelton" to connect with database
    do not use it in project
    it will called in next class 'DBConnection'
    which should be used instead
    """

    def __init__(self):
        pass


    # creates new connection
    def create_connection(self) -> Database:
        """
        creates a connection to database
        if connection can not created
        program will exit
        """
        try:
            # create a connection using MongoClient
            if settings.DB_URL is None:
                settings.DB_URL = f"{settings.DB_PROTOCOL}://{settings.DB_HOST}:{settings.DB_PORT}/"
            if settings.DB_USER is not None and settings.DB_PASSWORD is not None:
                settings.DB_URL = f"{settings.DB_PROTOCOL}://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/"
            logging.log(
                verboselogs.NOTICE,
                f"start connecting to database... to => {settings.DB_URL}",
            )
            max_sev_sel_delay = 1
            client: MongoClient = MongoClient(
                settings.DB_URL, serverSelectionTimeoutMS=max_sev_sel_delay
            )
            # dirty check if connection exist, if not error will throw
            is_connected: bool = False
            is_connected_retry: int = 5
            while not is_connected and is_connected_retry > 0:
                try:
                    client.server_info()
                    is_connected = True
                except pymongo.errors.ServerSelectionTimeoutError as e:
                    logging.log(
                        logging.WARNING,
                        f"Connect to database failed, retry {is_connected_retry}/5",
                    )
                    is_connected_retry -= 1
                    sleep(1)
            if not is_connected:
                raise pymongo.errors.ServerSelectionTimeoutError("Failed to connect")

            logging.log(verboselogs.NOTICE, "... connected with database")
            logging.log(
                verboselogs.NOTICE, f"access schema ... => {settings.DB_SCHEMA}"
            )
            # create the database access
            schema: Database = client[settings.DB_SCHEMA]
            logging.log(verboselogs.NOTICE, "... access create, you can use db")
            return schema

        except pymongo.errors.ServerSelectionTimeoutError as e:
            logging.log(logging.CRITICAL, f"1:: {e}")
            sys.exit(4)
        except Exception as e:
            logging.log(logging.CRITICAL, f"2:: {e}", exc_info=True)


    # for explicitly opening database connection
    def __enter__(self) -> Database:
        self.dbconn = self.create_connection()
        return self.dbconn

    def __exit__(self, a, b, c):
        self.dbconn.close()




# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------
class DBConnection:
    """
    class to use in project to handle
    database interactions
    use: in main to first call and check
         if database is reachable
    contains some base functions
    to call with database
    """
    connection: Union[Database, None] = None

    @classmethod
    def get_connection(cls, new: bool = False) -> Union[Database, None]:
        """
        creates return new Singleton database connection
        """
        if new or cls.connection is None:
            cls.connection = DBConnector().create_connection()
        return cls.connection


    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------
    @classmethod
    def insert_one(cls, obj: MongoModel, table_name: str) -> Union[PyObjectId, None]:
        """
        insert a model-table
        """
        connection: Database = cls.get_connection()
        result: InsertOneResult = connection[table_name].insert_one(obj.dict())
        return PyObjectId(result.inserted_id) if result is not None else None

    @classmethod
    def find_one(
        cls, filter: Dict[str, Any], entity: Type[Any], table_name: str
    ) -> Union[Any, None]:
        """
        finds a model-table by filter
        and transforms it into the class
        provided by 'entity'-Type
        """
        connection: Database = cls.get_connection()
        result: Union[Any, None] = connection[table_name].find_one(filter)
        if result is not None:
            result = entity(**result)
        return result

    @classmethod
    def find_and_modify(
        cls, id: PyObjectId, update: Dict[str, Any], entity: Type[Any], table_name: str
    ) -> Union[Any, None]:
        """
        finds and modify a model-table by id
        and transforms it into the class
        provided by 'entity'-Type
        """
        connection: Database = cls.get_connection()
        result: Union[Any, None] = connection[table_name].find_one_and_update(
            {"_id": id}, {"$set": update}, upsert=False, new=True
        )
        if result is not None:
            result = entity(**result)
        return result

    @classmethod
    def remove(cls, id: PyObjectId, table_name: str) -> bool:
        """
        removes an entity from model-table
        by id
        """
        connection: Database = cls.get_connection()
        # connection[table_name].remove(id)
        result: DeleteResult = connection[table_name].delete_one({"_id": id})
        return result is not None and result.deleted_count > 0
