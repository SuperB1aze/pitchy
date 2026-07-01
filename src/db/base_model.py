from typing_extensions import Annotated
from datetime import datetime

from sqlalchemy import text, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, mapped_column

class Base(DeclarativeBase):
    repr_cols = ()
    repr_cols_length_only = ("text_content",)

    def __repr__(self) -> str:
        cols = []
        for col in self.__table__.columns.keys():
            if col not in self.repr_cols:
                continue
            value = getattr(self, col)
            if col in self.repr_cols_length_only and isinstance(value, str):
                cols.append(f"{col}_length = {len(value)}")
            else:
                cols.append(f"{col} = {value}")

        return f"<{self.__class__.__name__}({', '.join(cols)})>"
    
int_primary_key = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[datetime, mapped_column(TIMESTAMP(timezone=True), server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(TIMESTAMP(timezone=True), nullable=True)]