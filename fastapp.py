import random

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from canvas import STYLES, styles, randomize_colors, process

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://lkpttn-image-bucket.s3.amazonaws.com/woods.jpg"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/')
async def root():
    return {'status': 'great job, you found the index'}


@app.get('/canvas')
def get_randomized_canvas():
    style = random.choice(STYLES)
    return {
        'msg': 'A random style was chosen',
        **get_canvas(style)
    }


@app.get('/canvas/render')
def render_randomized_canvas(req: Request):
    style = random.choice(STYLES)
    # TODO: Should this be an actual redirect so that style is in URL?
    return render_canvas(style, req)


@app.get('/canvas/{style}')
def get_canvas(style: str):
    response = {
        'style': style,
        'original_code': styles[style]['code'],
        'randomized': randomize_colors(styles[style]['code'])
    } if style in STYLES else {'msg': f'Sorry, but {style} is not an available style'}
    return response


@app.get('/canvas/{style}/render')
def render_canvas(style: str, req: Request):
    if style in STYLES:
        clean = process(styles[style]['code'])
        return templates.TemplateResponse(
            'layouts/canvas.html', dict(
                request=req,
                title='Random Canvas',
                name=style,
                code=clean
            ))
    else:
        response = {
            'msg': f'Sorry, but {style} is not an available style'
        }
        return response
