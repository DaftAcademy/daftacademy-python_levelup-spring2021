import hashlib
from datetime import date, datetime, timedelta
from typing import Dict, Optional

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from pydantic import BaseModel


class Patient(BaseModel):
    id: Optional[int]
    name: str
    surname: str
    register_date: Optional[date]
    vaccination_date: Optional[date]

    def __init__(self, **data):
        super().__init__(
            register_date=datetime.now().date(),
            vaccination_date=datetime.now().date()
            + timedelta(
                days=Patient.vaccination_timedelta(
                    data.get("name"), data.get("surname")
                )
            ),
            **data
        )

    @classmethod
    def vaccination_timedelta(cls, name, surname):
        name_letters = "".join(filter(str.isalpha, name))
        surname_letters = "".join(filter(str.isalpha, surname))
        """
        Przykład z uzyciem regexp'a:

        import re
        regex = re.compile(r'[A-Za-z]+') // tylko litery! Uzycie \w przepuszcza tez cyfry oraz podloge
        name_letters = "".join(filter(regex.match, name))
        surname_letters = "".join(filter(regex.match, surname))       
        """
        return len(name_letters) + len(surname_letters)


app = FastAPI()
app.counter: int = 1
app.storage: Dict[int, Patient] = {}


@app.get("/")
def read_root():
    return {"message": "Hello world!"}


@app.api_route(
    path="/method", methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"], status_code=200
)
def read_request(request: Request, response: Response):
    request_method = request.method

    if request_method == "POST":
        response.status_code = status.HTTP_201_CREATED

    return {"method": request_method}


@app.get("/auth")
def auth_request(password: str = "", password_hash: str = ""):
    authorized = False
    if password and password_hash:
        phash = hashlib.sha512(bytes(password, "utf-8")).hexdigest()
        authorized = phash == password_hash

    if authorized:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


"""
Przykładowe inputy dla zadania nr. 4 i 5:
{"name": "Jan", "surname": "Nowak 2"}
{"name": "Jan", "surname": "Nowak-Jezioranski"}
{"name": "Jan", "surname": "!@#$%^&*()1234567890"}
"""


@app.post("/register", status_code=201)
def create_patient(patient: Patient):
    patient.id = app.counter
    app.storage[app.counter] = patient
    app.counter += 1
    return patient


@app.get("/patient/{patient_id}")
def show_patient(patient_id: int):
    if patient_id < 1:
        raise HTTPException(status_code=400, detail="Invalid patient id")

    if patient_id not in app.storage:
        raise HTTPException(status_code=404, detail="Patient not found")

    return app.storage.get(patient_id)
