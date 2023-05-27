import uvicorn

from src.api.http.factories import AuthAPIFactory

app = AuthAPIFactory().create_app()
uvicorn.run(app)
