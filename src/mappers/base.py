from typing import TypeVar
from pydantic import BaseModel

from src.models import Base


DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: type[DBModelType]
    schema: type[SchemaType]
    nested_mappers: dict[str, type["DataMapper"]] = {}

    @classmethod
    def map_to_db_model(cls, data: SchemaType) -> DBModelType:
        data_dict = data.model_dump()

        for field, mapper in cls.nested_mappers.items():
            if field in data_dict:
                data_dict[field] = [
                    mapper.map_to_db_model(item)
                    for item in getattr(data, field)
                ]

        return cls.db_model(**data_dict)

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
            if key not in cls.nested_mappers:
                setattr(db_model, key, value)
                continue

            nested_mapper = cls.nested_mappers[key]
            existing_items = getattr(db_model, key)
            existing_by_id = {item.id: item for item in existing_items}

            for item in getattr(data, key):
                existing_item = existing_by_id.get(item.id)

                if existing_item is None:
                    existing_items.append(nested_mapper.map_to_db_model(item))
                else:
                    nested_mapper.map_to_existing_model(item, existing_item)

        return db_model
