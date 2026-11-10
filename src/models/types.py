import datetime
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
]

updated_at = Annotated[
    datetime.datetime | None,
    mapped_column(
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    )
]
is_deleted = Annotated[bool, mapped_column(server_default=text("false"))]
