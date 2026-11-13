from typing import TypeVar
from pydantic import BaseModel

from src.models import Base


DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: type[DBModelType]
    schema: type[SchemaType]

    @classmethod
    def map_to_db_model(cls, data: SchemaType) -> DBModelType:
        return cls.db_model(**data.model_dump())

    @classmethod
    def map_to_schema(cls, data: DBModelType, schema: type[SchemaType] | None = None) -> SchemaType:
        schema = schema or cls.schema
        return schema.model_validate(data, from_attributes=True)
