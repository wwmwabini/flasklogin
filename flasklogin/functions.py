import secrets, os
from flasklogin import app
from PIL import Image

def save_picture(form_picture):
    random_name = secrets.token_hex(12)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_file_name = random_name + file_extension
    picture_path = os.path.join(app.root_path, 'static/profile_pictures', picture_file_name)

    img = resize_image(form_picture, picture_path)
    img.save(picture_path)
    return picture_file_name



def resize_image(form_picture, picture_path):
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return i



def remove_old_picture(old_profile_picture_path):

    if os.path.isfile(old_profile_picture_path):
        try:
            os.remove(old_profile_picture_path)
        except Exception as e:
            print('Error. Could not delete file.', e)