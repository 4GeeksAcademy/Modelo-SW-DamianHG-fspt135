from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    favorite =  relationship('Favorite')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

    def serialize_update(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            "password":self.password
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    img: Mapped[str] = mapped_column(String(80), nullable=False)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    birth_year: Mapped[str] = mapped_column(String(80), nullable=False)
    gender: Mapped[str] = mapped_column(String(80), nullable=False)
    height: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(String(80), nullable=False)
    favorite: Mapped[List["Favorite"]] = relationship(back_populates="character")

    def serialize(self):
        return{
           "id": self.id,
           "img": self.img,
           "name": self.name,
           "birth_year": self.birth_year,
           "gender": self.gender,
           "height": self.height,
           "description": self.description
        }
    def serialize_fav(self):
        return{
            "id": self.id,
            "name": self.name,
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    img: Mapped[str] = mapped_column(String(80), nullable=False)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(80), nullable=False)
    diameter: Mapped[str] = mapped_column(String(80), nullable=False)
    gravity: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(String(80), nullable=False)
    favorite: Mapped[List["Favorite"]] = relationship(back_populates="planet")

    def serialize(self):
        return{
            "id": self.id,
            "img": self.img,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "description": self.description
        }

    def serialize_fav(self):
        return{
            "id": self.id,
            "name": self.name,
        }

class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"), nullable=False)
    user = relationship('User')
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=True)
    character: Mapped["Character"] = relationship(back_populates="favorite")
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    planet: Mapped["Planet"] = relationship(back_populates="favorite")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character": self.character.serialize_fav() if self.character else None,
            "planet": self.planet.serialize_fav() if self.planet else None
        }
    
    def serialize_fav_character(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "character": self.character.serialize_fav()
        }
    
    def serialize_fav_planet(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "planet": self.planet.serialize_fav()
        }