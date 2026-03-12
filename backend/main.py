
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from datetime import date

DATABASE_URL = "sqlite:///./hrms.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class EmployeeDB(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String)
    department = Column(String)
    attendance = relationship("AttendanceDB", back_populates="employee")

class AttendanceDB(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    date = Column(Date)
    status = Column(String)
    employee = relationship("EmployeeDB", back_populates="attendance")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HRMS Lite API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Employee(BaseModel):
    employee_id: str
    full_name: str
    email: EmailStr
    department: str

class Attendance(BaseModel):
    employee_id: int
    date: date
    status: str

@app.get("/")
def root():
    return {"message": "HRMS Lite API running"}

@app.get("/employees")
def get_employees(db: Session = Depends(get_db)):
    return db.query(EmployeeDB).all()

@app.post("/employees")
def add_employee(emp: Employee, db: Session = Depends(get_db)):
    existing = db.query(EmployeeDB).filter(EmployeeDB.employee_id == emp.employee_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    obj = EmployeeDB(**emp.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = db.query(EmployeeDB).get(emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(emp)
    db.commit()
    return {"message": "Employee deleted"}

@app.post("/attendance")
def mark_attendance(att: Attendance, db: Session = Depends(get_db)):
    emp = db.query(EmployeeDB).get(att.employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    rec = AttendanceDB(**att.dict())
    db.add(rec)
    db.commit()
    return {"message": "Attendance marked"}

@app.get("/attendance/{employee_id}")
def get_attendance(employee_id: int, db: Session = Depends(get_db)):
    return db.query(AttendanceDB).filter(AttendanceDB.employee_id == employee_id).all()
