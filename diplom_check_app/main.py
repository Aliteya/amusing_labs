import logging
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.db import get_db, Student, Diplom, Curator


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Diplom protection")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    logger.info("GET / called")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/stud/register", response_class=HTMLResponse)
async def register_form(request: Request):
    logger.info("GET /stud/register called")
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/stud/register", response_class=HTMLResponse)
async def register_student(request: Request, student_name: str = Form(...), student_age: int = Form(...), db: Session = Depends(get_db)):
    logger.info("POST /stud/register called")
    new_student = Student(student_name=student_name, student_age=student_age)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return templates.TemplateResponse("register.html", {"request": request, "message": "Регистрация успешна"})

@app.get("/stud/login", response_class=HTMLResponse)
async def login_form(request: Request):
    logger.info("GET /stud/login called")
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/stud/login", response_class=HTMLResponse)
async def login_student(request: Request, student_name: str = Form(...), db: Session = Depends(get_db)):
    logger.info("POST /stud/login called")
    student = db.query(Student).filter(Student.student_name == student_name).first()
    if student:
        return templates.TemplateResponse("diploma_form.html", {"request": request, "student": student})
    return templates.TemplateResponse("login.html", {"request": request, "message": "Студент не найден"})

@app.post("/stud/diploms", response_class=HTMLResponse)
async def add_diploma(request: Request, student_id: int = Form(...), diplom_name: str = Form(...), pages: int = Form(...), count_sources: int = Form(...), db: Session = Depends(get_db)):
    logger.info("POST /stud/diploms called")
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if student:
        new_diplom = Diplom(diplom_name=diplom_name, pages=pages, count_sources=count_sources, student_id=student.student_id)
        db.add(new_diplom)
        db.commit()
        db.refresh(new_diplom)
        return templates.TemplateResponse("diploma_form.html", {"request": request, "message": "Диплом успешно добавлен", "student": student})
    return templates.TemplateResponse("diploma_form.html", {"request": request, "message": "Студент не найден"})

@app.get("/curat/Cregister", response_class=HTMLResponse)
async def cregister_form(request: Request):
    logger.info("GET /curator/Cregister called")
    return templates.TemplateResponse("Cregister.html", {"request": request})

@app.post("/curat/Cregister", response_class=HTMLResponse)
async def register_curator(request: Request, curator_name: str = Form(...), curator_age: int = Form(...), db: Session = Depends(get_db)):
    logger.info("POST /curator/Cregister called")
    new_curator = Curator(curator_name=curator_name, curator_age=curator_age)
    db.add(new_curator)
    db.commit()
    db.refresh(new_curator)
    return templates.TemplateResponse("Cregister.html", {"request": request, "message": "Регистрация успешна"})


@app.get("/curat/Clogin", response_class=HTMLResponse)
async def curator_login_form(request: Request):
    logger.info("GET /curat/Clogin called")
    return templates.TemplateResponse("Clogin.html", {"request": request})

@app.post("/curat/Clogin", response_class=HTMLResponse)
async def login_curator(request: Request, curator_name: str = Form(...), db: Session = Depends(get_db)):
    logger.info("POST /curat/Clogin called")
    curator = db.query(Curator).filter(Curator.curator_name == curator_name).first()
    if curator:
        students = db.query(Student).all()
        return templates.TemplateResponse("curator_dashboard.html", {"request": request, "curator": curator, "students": students})
    return templates.TemplateResponse("Clogin.html", {"request": request, "message": "Куратор не найден"})

@app.post("/curat/check_diploms/student/{student_id}", response_class=HTMLResponse)
async def select_student(request: Request, student_id: int, curator_id: int = Form(...), db: Session = Depends(get_db)):
    logger.info(f"POST /curat/check_diploms/student/{student_id} called")
    student = db.query(Student).filter(Student.student_id == student_id).first()
    curator = db.query(Curator).filter(Curator.curator_id == curator_id).first()
    if student and curator:
        student.curator_id = curator.curator_id
        db.commit()
        diploms = db.query(Diplom).filter(Diplom.student_id == student_id, Diplom._checked == False).all()
        return templates.TemplateResponse("check_diploms.html", {"request": request, "diploms": diploms})
    return templates.TemplateResponse("curator_dashboard.html", {"request": request, "message": "Студент или куратор не найден"})


@app.get("/curat/check_diplom/{diplom_id}", response_class=HTMLResponse)
async def check_diplom(request: Request, diplom_id: int, db: Session = Depends(get_db)):
    logger.info(f"POST /curat/check_diplom/{diplom_id} called")
    diplom = db.query(Diplom).filter(Diplom.diplom_id == diplom_id).first()
    if diplom:
            diplom._checked = True
            db.commit()
            db.refresh(diplom)
            message = "Диплом успешно проверен"
            logger.info(f"Diploma checked: {diplom.diplom_name}")
    else:
        message = "Диплом не найден"

    diploms = db.query(Diplom).filter(Diplom._checked == False).all()
    return templates.TemplateResponse("check_diploms.html", {"request": request, "diploms": diploms, "message": message})


@app.get("/view_diploms", response_class=HTMLResponse)
async def view_diploms(request: Request, db: Session = Depends(get_db)):
    logger.info("GET /view_diploms called")
    diploms = db.query(Diplom).all()
    return templates.TemplateResponse("view_diploms.html", {"request": request, "diploms": diploms})
