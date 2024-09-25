import logging
from sqlalchemy import create_engine, Column, Integer, Text, Boolean, ForeignKey, MetaData
from sqlalchemy.orm import relationship, Session, validates, DeclarativeBase

engine = create_engine('sqlite:///mydb.db')

conn = engine.connect()

# Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()

class Base(DeclarativeBase): pass


class Student(Base):
    __tablename__ = "students"
    student_id = Column("student_id", Integer, primary_key=True, index=True)
    student_name = Column("student_name", Text)
    student_age = Column("student_age", Integer)
    curator_id = Column(Integer, ForeignKey("curators.curator_id"))
    curator = relationship("Curator", back_populates="students")
    diplom = relationship("Diplom", back_populates="student", uselist=False)

class Curator(Base):
    __tablename__ = "curators"
    curator_id = Column("curator_id", Integer, primary_key=True, index=True)
    curator_name = Column("curator_name", Text)
    curator_age = Column("curator_age", Integer)
    students = relationship("Student", back_populates="curator")


class Diplom(Base):
    __tablename__ = "diploms"
    diplom_id = Column("diplom_id", Integer, primary_key=True, index=True)
    diplom_name = Column("diplom_name", Text)
    pages = Column("pages", Integer)
    count_sources = Column("count_sources", Integer)
    _now = Column("now", Boolean, default=False)
    _checked = Column("checked", Boolean, default=False)
    
    student_id = Column(Integer, ForeignKey("students.student_id"))
    student = relationship("Student", back_populates="diplom")


Base.metadata.create_all(bind=engine)
print("db created")
logger = logging.getLogger(__name__)

def get_db():
    db = Session(autocommit=False, autoflush=False, bind=engine)
    try:
        yield db
    except Exception as e:
        logger.error(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()
