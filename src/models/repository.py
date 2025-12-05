from src.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func, datetime
from sqlalchemy import String, Integer

class RepositoryBase(Base):
    __tablename__ = "repositories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    owner: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    last_analyzed_at: Mapped[datetime | None] = mapped_column(server_default=func.now())