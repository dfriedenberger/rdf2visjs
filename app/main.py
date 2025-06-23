from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from rdf2vis.graph_utils import gen_graph
from rdf2vis.svg_utils import replace_placeholder


app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

projects = [
    {
        "id": "mut-flexidug",
        "name": "FlexiDug MicroModels and Transformations",
        "model": "data/mut-flexidug.ttl",
        "mapping": "data/mut-mapping.txt"
    },
    {
        "id": "mut-squirrl",
        "name": "SQuIRRL MicroModels and Transformations",
        "model": "data/mut-squirrl.ttl",
        "mapping": "data/mut-mapping.txt"
    },
    {
        "id": "map",
        "name": "Map",
        "model": "data/map.ttl",
        "mapping": "data/mapping.txt"
    },
    {
        "id": "flexidug",
        "name": "FlexiDug Model",
        "model": "data/flexidug.ttl",
        "mapping": "data/flexidug-mapping.txt"
    },
]

# Jinja2 Templates
templates = Jinja2Templates(directory="templates")


# Aufruf über /svg/filename.svg?text=Neuer Text
@app.get("/svg/{filename}")
def get_svg(filename: str, request: Request):
    query_params = dict(request.query_params)
    """
    Generate SVG with replaced placeholder text.
    :param filename: Name of the SVG file to be processed.
    :param text: Text to replace the placeholder in the SVG file.
    :return: Processed SVG file as a string.
    """

    svg_string = replace_placeholder(filename, query_params)

    return Response(svg_string, media_type="image/svg+xml")


@app.get("/graph/{projectId}")
def get_graph(projectId: str):
    print(f"Generating graph for project: {projectId}")
    project = next((p for p in projects if p["id"] == projectId), None)
    if not project:
        return Response(status_code=404, content="Project not found")
    return gen_graph(project["model"], project["mapping"])


# Dynamische Index-Seite
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "projects": projects})


# Dynamische Seite für Projektgraph
@app.get("/project/{projectId}", response_class=HTMLResponse)
async def read_graph(request: Request, projectId: str):
    print(f"Generating graph for project: {projectId}")
    project = next((p for p in projects if p["id"] == projectId), None)
    if not project:
        return Response(status_code=404, content="Project not found")
    return templates.TemplateResponse("graph.html", {
        "request": request,
        "project": project
    })


# Verzeichnis für statische Dateien
app.mount("/", StaticFiles(directory="static", html=True), name="static")
