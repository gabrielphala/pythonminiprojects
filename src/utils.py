ALLOWED_EXTENSIONS = ('jpg' , "jpeg" , 'gif', 'png', 'webp', 'jfif', "tif" , "bmp")

def allowed_file (filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS;
