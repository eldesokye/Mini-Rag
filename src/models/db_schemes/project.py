from pydantic import BaseModel, Field , validator
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")  # MongoDB uses _id as the default primary key field
    project_id: str = Field(...,min_length=1, max_length=100)  # unique identifier for the project

    @validator('project_id')
    def validate_project_id(cls, value):
        if not value.isalnum():  # ensure project_id is alphanumeric
            raise ValueError('project_id must be alphanumeric')
        return value
    

    class Config:
        allow_population_by_field_name = True  # allow using field names instead of aliases when creating instances
        arbitrary_types_allowed = True  # allow arbitrary types like ObjectId
        json_encoders = {ObjectId: str}  # convert ObjectId to string when serializing to JSON



    @classmethod
    def get_indexes(cls ):
        return [
            {
                "key":[("project_id", 1)],
                "name":"project_id_index_1",
                "unique": True
            }
        ]