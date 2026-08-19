from .database import Base
from sqlalchemy import TIMESTAMP, ForeignKey, String, Integer, Column, DATETIME,text
from sqlalchemy.orm import relationship



class Post(Base):

    __tablename__ = "new_posts"

    id = Column(Integer, primary_key=True)
    Caption = Column(String, nullable=False)
    Body = Column(String, nullable=False)
    Username = Column(String, nullable=False)
    Published_Date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    user_id = Column(Integer, ForeignKey("Accounts.id",ondelete="CASCADE"), nullable=False, )

    user_info = relationship("Account")




class Account(Base):

    __tablename__ = "Accounts"

    id = Column(Integer, primary_key=True)
    Gmail =  Column(String, nullable=False, unique=True)
    Name = Column(String, nullable=False)
    Password =  Column(String, nullable=False)
    Date_Created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    Phone_number = Column(String, nullable=False)


class vote(Base):

    __tablename__ = "Votes"

    Post_id = Column(Integer, ForeignKey("new_posts.id", ondelete="CASCADE"), primary_key=True)
    User_id = Column(Integer, ForeignKey("Accounts.id", ondelete="CASCADE"), primary_key=True)








