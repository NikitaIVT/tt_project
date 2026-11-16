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

    @classmethod
    def map_to_schemas(cls, data: list[DBModelType], schema: type[SchemaType] | None = None) -> list[SchemaType]:
        schema = schema or cls.schema
        return [cls.map_to_schema(element, schema) for element in data]

    @classmethod
    def map_to_existing_model(cls, data: SchemaType, db_model: DBModelType) -> DBModelType:
        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_model, key, value)
        return db_model
