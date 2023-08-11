from flask import Blueprint
import ckan.plugins.toolkit as toolkit

datahub = Blueprint('datahub', __name__, template_folder='templates')
@datahub.route('/datahub', methods=['GET'])
def index():
    # return template
    return toolkit.render('datahub/base.html')