from sqlalchemy import MetaData,Column, JSON, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from auth.datebase import Base

# metadata = MetaData()

# class Base(DeclarativeBase):
#     metadata = metadata

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    email: Mapped[str] = mapped_column("email", String, nullable=False)
    username: Mapped[str] = mapped_column("username", String, nullable=False)
    password: Mapped[str] = mapped_column("password", String, nullable=False)
    registration_at: Mapped[datetime] = mapped_column("registration_at", TIMESTAMP, default=datetime.now)
    role_id: Mapped[int]= Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role", back_populates="users")

class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    name: Mapped[str] = mapped_column("name", String, nullable=False)
    permissions: Mapped[JSON] = mapped_column("permissions", JSON)
    users = relationship("User", back_populates="role")
