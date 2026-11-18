from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel, Field
from database import get_connection
from mysql.connector import IntegrityError


class EquipmentCreate(BaseModel):
    name: str = Field(min_length=1)
    total_quantity: int = Field(ge=0)

class CustomerCreate(BaseModel):
    full_name: str = Field(min_length=1)
    email: str = Field(min_length=1)

app = FastAPI()

@app.get("/")
def home():
    return{"message": "Stockflow is running"}

@app.get("/health")
def health():
    return{"status": "ok"}

@app.get("/customers")
def get_customers():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT customer_id, full_name, email FROM customers ORDER BY customer_id"
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()



@app.post("/customers", status_code=201)
def create_customer(data: CustomerCreate):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO customers (full_name, email) VALUES (%s, %s)",
            (data.full_name, data.email)
        )

        connection.commit()
        new_id = cursor.lastrowid

        return {
            "customer_id": new_id,
            "full_name": data.full_name,
            "email": data.email
        }

    except IntegrityError as error:
        connection.rollback()

        if error.errno == 1062:
            raise HTTPException(
                status_code=409,
                detail="Customer email already exists"
            )

        raise

    finally:
        cursor.close()
        connection.close()

@app.get("/equipment")
def get_equipment():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT id, name, total_quantity FROM equipment ORDER BY id"
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

@app.get("/equipment/{equipment_id}")
def get_equipment_id(equipment_id: int):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT id, name, total_quantity FROM equipment WHERE id = %s",
            (equipment_id,)
        )

        item = cursor.fetchone()

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Equipment not found"
            )

        return item

    finally:
        cursor.close()
        connection.close()

@app.post("/equipment", status_code=201)
def create_equipment(data: EquipmentCreate):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO equipment (name, total_quantity) VALUES (%s, %s)",
            (data.name, data.total_quantity)
        )

        connection.commit()
        new_id = cursor.lastrowid

        return {
            "id": new_id,
            "name": data.name,
            "total_quantity": data.total_quantity
        }

    finally:
        cursor.close()
        connection.close()
