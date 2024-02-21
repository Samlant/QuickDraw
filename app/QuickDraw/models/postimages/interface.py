from pathlib import Path
from QuickDraw.helper import open_config
from QuickDraw.models.postimages.postimages import PostImages

class PostImgInterface: 
    def __init__(self): 
        pass    

    @property
    def email(self) -> str:
        config = open_config()
        config.get("post_img", "email").value

    @property
    def password(self) -> str:
        config = open_config()
        config.get("post_img", "password").value
    
    def upload_photo(self, image_path: Path)
        client = PostImages(self.email, self.password)

        # Login to your PostImages account
        client.login()

        # Upload an image
        image_urls = client.upload_image(str(image_path))
        if image_urls:
            for url in image_urls.values():
                return url
        else:
            return False