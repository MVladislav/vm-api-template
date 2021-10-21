"""
    database connection handler for mongoDB
    with base class-object for creating new
    table-schemas.
    Use: 'DBConnection' in the code for
    handling connection
"""
import logging
import sys
from typing import Dict, Type

import pymongo
from app.utils.config import (DB_HOST, DB_PASSWORD, DB_PORT, DB_PROTOCOL,
                              DB_SCHEMA, DB_URL, DB_USER)
from bson.objectid import ObjectId
from pydantic.fields import Field
from pydantic.main import BaseConfig, BaseModel
from pymongo import MongoClient
from pymongo.database import Database

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
            ObjectId: lambda oid: str(oid),
        }


# ------------------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------------------


class DBConnector():
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
            connect_with = DB_URL

            # create a connection using MongoClient
            if connect_with is None:
                connect_with = f"{DB_PROTOCOL}://{DB_HOST}:{DB_PORT}/"
            if DB_USER is not None and DB_PASSWORD is not None:
                connect_with = f"{DB_PROTOCOL}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
            logging.log(logging.NOTICE, f"start connecting to database... to => {connect_with}")
            max_sev_sel_delay = 1
            client: MongoClient = MongoClient(
                connect_with,
                serverSelectionTimeoutMS=max_sev_sel_delay
            )

            # dirty check if connection exist, if not error will throw
            client.server_info()
            logging.log(logging.NOTICE, "... connected with database")

            logging.log(logging.NOTICE, f"access schema ... => {DB_SCHEMA}")

            # create the database access
            schema: Database = client[DB_SCHEMA]
            logging.log(logging.NOTICE, "... access create, you can use db")
            return schema
        except pymongo.errors.ServerSelectionTimeoutError as ex:
            logging.log(logging.ERROR, ex)
            sys.exit(4)
        except Exception as ex:
            logging.log(logging.ERROR, ex)

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


class DBConnection():
    """
        class to use in project to handle
        database interactions
        use: in main to first call and check
             if database is reachable
        contains some base functions
        to call with database
    """

    connection: Database = None

    @classmethod
    def get_connection(cls, new=False) -> Database:
        """
            creates return new Singleton database connection
        """
        if new or not cls.connection:
            cls.connection = DBConnector().create_connection()
        return cls.connection

    # --------------------------------------------------------------------------
    #
    #
    #
    # --------------------------------------------------------------------------

    @classmethod
    def insert_one(cls, obj: MongoModel, table_name: str):
        """
            insert a model-table
        """
        connection = cls.get_connection()
        connection[table_name].insert_one(obj.dict())

    @classmethod
    def find_one(cls, filter: Dict, entity: Type, table_name: str):
        """
            finds a model-table by filter
            and transforms it into the class
            provided by 'entity'-Type
        """
        connection = cls.get_connection()
        result = connection[table_name].find_one(filter)
        if result is not None:
            result = entity(**result)
        return result

    @classmethod
    def find_and_modify(cls, id: PyObjectId, update: Dict, entity: Type, table_name: str):
        """
            finds and modify a model-table by id
            and transforms it into the class
            provided by 'entity'-Type
        """
        connection = cls.get_connection()
        result = connection[table_name].find_and_modify(
            {"_id": id}, {"$set": update},
            upsert=False,
            new=True
        )
        if result is not None:
            result = entity(**result)
        return result

    @classmethod
    def remove(cls, id: PyObjectId, table_name: str):
        """
            removes an entity from model-table
            by id
        """
        connection = cls.get_connection()
        connection[table_name].remove(id)
