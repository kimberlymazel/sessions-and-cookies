from pydantic import BaseModel
from uuid import UUID, uuid4
from fastapi import HTTPException, FastAPI, Response, Depends

from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier

class SessionData(BaseModel):
    username: str

#-------------------------------------------------------#
#-------------------------------------------------------#
#---------------------- COOKIES ------------------------#
#-------------------------------------------------------#
#-------------------------------------------------------#

cookie_params = CookieParameters()

cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier", # Same with identifier in BasicVerifier below
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
)

# Stores SessionData in the memory of the server
backend = InMemoryBackend[UUID, SessionData]()

#-------------------------------------------------------#
#-------------------------------------------------------#
#---------------------- VERIFIER -----------------------#
#-------------------------------------------------------#
#-------------------------------------------------------#

# Verifies that the session does exist
class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, SessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        return True


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)

#-------------------------------------------------------#
#-------------------------------------------------------#
#---------------------- FASTAPI ------------------------#
#-------------------------------------------------------#
#-------------------------------------------------------#

app = FastAPI()

# Index
@app.get("/")
def index():
    return {"Hello":"Sessions made by FastAPI"}

# Create Session
@app.post("/create_session/{name}")
async def create_session(name: str, response: Response):

    session = uuid4()
    data = SessionData(username=name)

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    return f"Successfully created a session for {name}"

# Get Current Session
@app.get("/get_current_session", dependencies=[Depends(cookie)])
async def get_session(session_data: SessionData = Depends(verifier)):
    return session_data

# Delete Session
@app.post("/delete_session")
async def delete_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "Successfully deleted session."