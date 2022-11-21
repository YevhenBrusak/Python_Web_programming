from flask import Blueprint

cabinet_bp = Blueprint('cabinet', __name__,
                        template_folder='templates/form_cabinet')
from . import views