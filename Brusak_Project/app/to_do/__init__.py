from flask import Blueprint

to_do_bp = Blueprint('to_do', __name__,
                        template_folder='templates/to_do')
from . import views