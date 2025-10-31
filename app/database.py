from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./library.db"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})