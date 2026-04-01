from pydantic import BaseModel 
from typing import Optional

# Request model for processing a file 
# This model will be used to receive the parameters for processing a file, including the file ID, chunk size, chunk overlap,
#  and whether to reset the processing state. The chunk size and overlap have default values if not provided in the request.
class ProcessRequest(BaseModel):
    file_id: str
    chunk_size: Optional[int] = 100 # default to 1MB if not provided 
    chunk_overlap: Optional[int] = 20 # default to 20% overlap if not provided
    do_reset: Optional[int] = 0

     

