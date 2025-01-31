from decouple import config
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Configuration       
cloudinary.config( 
    cloud_name = config('CLOUDINARY_NAME'), 
    api_key = config("CLOUDINARY_API_Key"), 
    api_secret = config("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_image(preview_img):
    try:
        response = cloudinary.uploader.upload(preview_img)
        return response['secure_url']
    except Exception as e:
        print("Cloudinary Upload Error:", e)
        return None