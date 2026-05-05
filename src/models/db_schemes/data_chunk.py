from pydantic import BaseModel, Field , validator
from typing import Optional
from bson.objectid import ObjectId


class DataChunk(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")  # MongoDB uses _id as the default primary key field
    chunk_text : str = Field(..., min_length=1)  # the text content of the chunk
    chunk_metadata: dict = Field(default_factory=dict)  # metadata associated with the chunk, stored as a dictionary
    chunk_order : int = Field(..., gt=0)  # the order of the chunk in the original file, must be a non-negative integer
    chunk_project_id : ObjectId = Field(..., alias="project_id")  # reference to the project this chunk belongs to, stored as an ObjectId
    chunk_asset_id : ObjectId

    # @validator('chunk_text')
    # def validate_chunk_text(cls, value):
    #     if not value.strip():  # ensure chunk_text is not empty or just whitespace
    #         raise ValueError('chunk_text must not be empty')
    #     return value
    

    class Config:
        allow_population_by_field_name = True  # allow using field names instead of aliases when creating instances
        arbitrary_types_allowed = True  # allow arbitrary types like ObjectId
        # json_encoders = {ObjectId: str}  # convert ObjectId to string when serializing to JSON


    @classmethod
    def get_indexes(cls):
        return [
            {
                "key":[("chunk_project_id", 1)],
                "name":"chunk_project_id_index_1",
                "unique": False
            }
        ]