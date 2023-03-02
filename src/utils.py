ALLOWED_EXTENSIONS = [
    ('png', 'jpg', 'gif', 'webp', 'jpeg'),
    ('jpg' , "jpeg" , 'png', 'webp', 'jfif', "tif" , "bmp")
]

def allowed_file (filename, allowed = 0):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS[allowed];
