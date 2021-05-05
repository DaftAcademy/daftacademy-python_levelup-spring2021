### ROZWIAZANIE DO ZADANIA 3.5 Z UZYCIEM DEKORATORA

import secrets
import uuid
from contextlib import contextmanager
from datetime import datetime
from functools import wraps
from hashlib import sha512
from typing import List, Optional

from fastapi import (Cookie, Depends, FastAPI, HTTPException, Request,
                     Response, status)
from fastapi.responses import (HTMLResponse, JSONResponse, PlainTextResponse,
                               RedirectResponse)
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
app.username = "4dm1n"
app.password = "NotSoSecurePa$$"
app.secret_key = "T00Sh0rtAppS3cretK3y"
app.api_token: List[str] = []
app.session_token: List[str] = []
app.token_limits = 3


def add_token(token: str, cache_ns: str):
    tokens = getattr(app, cache_ns)
    if len(tokens) >= app.token_limits:
        tokens.pop(0)
    tokens.append(token)
    setattr(app, cache_ns, tokens)


def remove_token(token: str, cache_ns: str):
    tokens = getattr(app, cache_ns)
    try:
        index = tokens.index(token)
        tokens.pop(index)
        setattr(app, cache_ns, tokens)
    except ValueError:
        return None


def generate_token(request: Request):
    return sha512(
        bytes(
            f"{uuid.uuid4().hex}{app.secret_key}{request.headers['authorization']}",
            "utf-8",
        )
    ).hexdigest()


def auth_basic_auth(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    correct_user = secrets.compare_digest(credentials.username, app.username)
    correct_pass = secrets.compare_digest(credentials.password, app.password)
    if not (correct_user and correct_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials"
        )

    return True


def auth_session(session_token: str = Cookie(None)):
    if app.session_token and session_token in app.session_token:
        return session_token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials"
    )


def auth_token(token: Optional[str] = None):
    if app.api_token and token in app.api_token:
        return token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials"
    )


def response_decorator(func):
    def message_response(format: str, func_value: str):
        if format == "json":
            return JSONResponse(content={"message": func_value})
        if format == "html":
            return HTMLResponse(content=f"<h1>{func_value}</h1>")

        return PlainTextResponse(content=func_value)

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_value = func(*args, **kwargs)
        return message_response(kwargs.get("format"), func_value)

    return wrapper


@app.get("/hello", response_class=HTMLResponse)
def read_root_hello():
    return f"""
    <html>
        <head>
            <title></title>
        </head>
        <body>
            <h1>Hello! Today date is { datetime.now().date() }</h1>
        </body>
    </html>
    """


@app.post("/login_session", status_code=201, response_class=HTMLResponse)
def create_session(
    request: Request, response: Response, auth: bool = Depends(auth_basic_auth)
):
    token = generate_token(request)
    add_token(token, "session_token")
    response.set_cookie(key="session_token", value=token)
    return ""


@app.post("/login_token", status_code=201)
def create_token(request: Request, auth: bool = Depends(auth_basic_auth)):
    token = generate_token(request)
    add_token(token, "api_token")
    return {"token": token}


@app.get("/welcome_session")
@response_decorator
def show_welcome_session(received_token: str = Depends(auth_session), format: str = ""):
    return "Welcome!"


@app.get("/welcome_token")
@response_decorator
def show_welcome_token(received_token: str = Depends(auth_token), format: str = ""):
    return "Welcome!"


@app.get("/logged_out")
@response_decorator
def logged_out(format: str = ""):
    return "Logged out!"


@app.delete("/logout_session")
def logout_session(received_token: str = Depends(auth_session), format: str = ""):
    remove_token(received_token, "session_token")
    return RedirectResponse(
        url=f"/logged_out?format={format}", status_code=status.HTTP_302_FOUND
    )


@app.delete("/logout_token")
def logout_token(received_token: str = Depends(auth_token), format: str = ""):
    remove_token(received_token, "api_token")
    return RedirectResponse(
        url=f"/logged_out?format={format}", status_code=status.HTTP_302_FOUND
    )
