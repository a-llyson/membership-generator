from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.card.card_gen import AccessCard


app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("web.html", context={"request": request, "id": id})

@app.post("/result", response_class=HTMLResponse)
async def create_card (
    request: Request, name: str = Form(...), memberCode: str = Form(...), tier: str = Form(...), date: str = Form(...)
):

    url = AccessCard(name, memberCode, tier, date).wrapper()
    return templates.TemplateResponse("success.html", {
        "request": request, "url" : url
        }) 

