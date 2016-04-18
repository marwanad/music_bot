from flask import Blueprint

main = Blueprint('main', __name__)
from setup import kik

from . import bot