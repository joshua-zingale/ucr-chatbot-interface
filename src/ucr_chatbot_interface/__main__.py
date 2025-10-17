"""A chainlit-powered web server for interacting with an AI Tutor."""

from argparse import ArgumentParser
import uvicorn

from . import create_app

parser = ArgumentParser(description=__doc__)
parser.add_argument(
    "--host", type=str, default="127.0.0.1", help="the IP address for the application"
)
parser.add_argument(
    "--port", type=int, default=8000, help="the port on which the application"
)
args = parser.parse_args()

app = create_app()
uvicorn.run(app, host=args.host, port=args.port)
