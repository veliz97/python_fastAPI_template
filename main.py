from ast import Str
from re import S
from typing import List,  Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import uuid

# Inicializamos una variable que tendrá todas las carácteristicas de FastAPI
app = FastAPI() 

# Definimos un modelo
class Course(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    level: str
    duration: int
    
# Simularemos una base de Datos.
courses_db = []

# CRUD
@app.get("/cursos/", response_model=List[Course])
def getCourses():
    return courses_db

@app.post("/cursos/", response_model = Course)
def create_course(course:Course):
    course.id = str(uuid.uuid4())
    courses_db.append(course)
    return course
    
@app.get("/cursos/{course_id}", response_model= Course)
def getCourse(course_id: str):
    course = next((course for course in courses_db if course.id == course_id), None)
    if course is None:
        raise HTTPException(status_code=404, detal = "Curso no encontrado")
    return course

@app.put("/cursos/{course_id}", response_model= Course)
def updateCourse(course_id: str, updateCourse: Course):
    course = next((course for course in courses_db if course.id == course_id), None)
    if course is None:
        raise HTTPException(status_code=404, detal = "Curso no encontrado")
    updateCourse.id = course_id
    index = courses_db.index(course)
    courses_db[index] = updateCourse
    return updateCourse

@app.delete("/cursos/{course_id}", response_model= Course)
def deleteCourse(course_id: str):
    course = next((course for course in courses_db if course.id == course_id), None)
    if course is None:
        raise HTTPException(status_code=404, detal = "Curso no encontrado")
    courses_db.remove(course)
    return course     