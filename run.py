"""
This module defines the entry point (run.py) for starting the Flask application.

Purpose:
* The run.py file serves as the entry point for launching the Flask application.

Usage:
* Execute (python run.py) in the terminal to start the Flask development server.
* Customize the (env and config.py) files to include any necessary
  initialization or configuration before running the application.

Doc: https://flask.palletsprojects.com/en/3.0.x/

-------------============= * Only for development! * =============-------------
"""

import logging
from dotenv import load_dotenv

from src import create_app
from src.messages import ApiMessages as msg
from src.messages import error_msg

load_dotenv()

app = create_app()

# Writes an error report to a file 'error.log'
logging.basicConfig(filename='error.log', level=logging.ERROR)


@app.errorhandler(500)
def internal_server_error(error) -> tuple[dict, int]:
    return error_msg(msg.INTERNAL_ERROR), 500


if __name__ == '__main__':
    """
    Run the Flask app
    """
    app.run(host=app.config['HOST'], port=app.config['PORT'])
