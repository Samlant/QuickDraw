from pathlib import Path
from QuickDraw.helper import open_config
from QuickDraw.models.postimages.postimages import PostImages


class FlickrInterface:
    def __init__(self) -> None:
        pass
    
    @property
    def email(self) -> str:
        config = open_config()
        email = config.get("post_img", "email").value
        return email

    @property
    def password(self) -> str:
        config = open_config()
        pw = config.get("post_img", "password").value
        return pw

    def upload_photo(self, image_path: Path):
        pass

    def login(self):
        pass

class PostImgInterface: 
    def __init__(self): 
        pass    

    @property
    def email(self) -> str:
        config = open_config()
        email = config.get("post_img", "email").value
        return email

    @property
    def password(self) -> str:
        config = open_config()
        pw = config.get("post_img", "password").value
        return pw
    
    def upload_photo(self, image_path: Path):
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