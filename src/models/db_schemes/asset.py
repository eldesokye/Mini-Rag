from pydantic import BaseModel, Field , validator
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime
from typing import Optional

class Asset(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")  # MongoDB uses _id as the default primary key field
    asset_project_id : ObjectId   # reference to the project this asset belongs to, stored as an ObjectId
    asset_type: str = Field(..., min_length=1)  # the type of the asset (e.g., "pdf", "docx", "txt")
    asset_name: str = Field(..., min_length=1)  # the original name of the asset file
    asset_size: Optional[int] = Field(default=None, gt=0)
    asset_config : dict = Field(default=None)  # configuration settings for processing the asset, stored as a dictionary
    asset_upload_at: datetime = Field(default=datetime.utcnow)  # the date and time when the asset was uploaded


    class Config:
        allow_population_by_field_name = True  # allow using field names instead of aliases when creating instances
        arbitrary_types_allowed = True  # allow arbitrary types like ObjectId
        json_encoders = {ObjectId: str}  # convert ObjectId to string when serializing to JSON  


    @classmethod
    def get_indexes(cls):
        return [
            {
                "key":[("asset_project_id", 1)],
                "name":"asset_project_id_index_1",
                "unique": False
            },
            {
                "key":[("asset_project_id", 1),
                       ("asset_name", 1)],
                "name":"asset_project_id_name_index_1",
                "unique": True
            },
        ]