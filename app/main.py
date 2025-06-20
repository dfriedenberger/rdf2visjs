from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

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


@app.get("/graph/")
def get_graph():
    return gen_graph("data/mut.ttl", "data/mapping.txt")
    # return gen_graph("data/map.ttl", "data/mapping.txt")


app.mount("/", StaticFiles(directory="static", html=True), name="static")
