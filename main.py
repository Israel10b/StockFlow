from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel


class EquipmentCreate(BaseModel):
    name: str
    total_quantity: int

app = FastAPI()

@app.get("/")
def home():
    return{"message": "Stockflow is running"}

@app.get("/health")
def health():
    return{"status": "ok"}

equipment = [
    {"id": 1, "name": "Speaker", "total_quantity": 5},
    {"id": 2, "name": "Microphone", "total_quantity": 8}
]

@app.get("/equipment")
def get_equipment():
    return equipment

@app.get("/equipment/{equipment_id}")
def get_equipment_id(equipment_id: int):
    for item in equipment:
        if item["id"] == equipment_id:
            return item
    raise HTTPException(
        status_code=404,
        detail="Equipment not found"
    )

@app.post("/equipment", status_code=201)
def create_equipment(data: EquipmentCreate):
    new_id = len(equipment) + 1

    new_item = {
        "id": new_id,
        "name": data.name,
        "total_quantity": data.total_quantity
    }

    equipment.append(new_item)
    return new_item
