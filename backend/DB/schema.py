from pydantic import BaseModel,Field

class Book(BaseModel): #Create Validations for the data that is being Commited to the DB. This is needed in FastAPI and is sometimes like the schema and metadata validations for the tables.
    title :str = Field(min_length = 1)
    author :str = Field(min_length = 1,max_length= 100)
    description : str = Field(min_length = 1,max_length = 100)
    rating : int = Field(gt = -1,lt=101)
    


