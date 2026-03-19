from sqlalchemy.orm import mapped_column

from typing import Annotated


int_pk = Annotated[int, mapped_column(primary_key=True)]