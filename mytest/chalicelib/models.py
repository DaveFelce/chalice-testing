from chalicelib.service.db import base
from sqlalchemy import Column, ForeignKey, Integer, Sequence, String
from sqlalchemy.orm import relationship


class User(base):
    __tablename__ = 'user'
    user_id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    first_name = Column(String(150))
    last_name = Column(String(150))
    username = Column(String(100))

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"


class Post(base):
    __tablename__ = 'post'
    post_id = Column(Integer, Sequence('post_id_seq'), primary_key=True)
    headline = Column(String(150))
    text = Column(String(5000))
    user_id = Column(
        Integer, ForeignKey("user.user_id"), nullable=False
    )
    user = relationship("User")

    def __repr__(self):
        return self.headline
