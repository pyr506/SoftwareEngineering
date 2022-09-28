from flask import jsonify, request, g, url_for, current_app
from datetime import datetime
from . import api, response
from .. import app
from .decorators import token_required
import os

@api.route('/imageuploader', methods=['POST'])
@token_required
def image_uploader(current_user):
    file = request.files.get('file')
    if file:
        filename = str(current_user.id) + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '_' + file.filename.lower()
        fn, ext = filename.split('.')
        if ext in ['jpg', 'gif', 'png', 'jpeg']:
            img_fullpath = os.path.join(app.config['IMAGE_UPLOADED_PATH'], filename)
            file.save(img_fullpath)
            data = []
            data.append({'location' : filename})
            return response.success(data)
        else:
            return response.error(403, "Image failed to upload, only for jpg, jpeg, gif, png.")

    # fail, image did not upload
    return response.error(403, "Image failed to upload")