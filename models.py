from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String(11), nullable=False, primary_key=True)
    name = Column(String(45), nullable=True)
    password = Column(String(12), nullable=True)
    email = Column(String(45), nullable=True)
    user_id = Column(String(11), nullable=True)
    telp = Column(String(45), nullable=True)
    privilages = Column(String(45), nullable=True)

    try:
        engine = create_engine('mysql://root:password@localhost/ckdb', encoding='latin8', echo=True)
    except:
        try:
            engine = create_engine('mysql://root:andrewroot@localhost/ckdb', encoding='latin8', echo=True)    
        except:
            print "can't login"
        Base.metadata.create_all(engine)
