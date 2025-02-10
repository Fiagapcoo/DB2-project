from decouple import config
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url


cloudinary.config( 
    cloud_name = config('CLOUDINARY_NAME'), 
    api_key = config("CLOUDINARY_API_Key"), 
    api_secret = config("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_image(preview_img):
    try:
        response = cloudinary.uploader.upload(preview_img)
        print("Cloudinary Response:", response)

        if isinstance(response, dict) and "secure_url" in response:
            return response["secure_url"]
        else:
            print("Erro: Resposta inesperada do Cloudinary", response)
            return None
    except Exception as e:
        print("Cloudinary Upload Error:", e)
        return None
