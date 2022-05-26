import PIL as PL

class MemeEngine:
    """
    MemeEngine class creates memes
    """

    def __init__(self, path):
        self.file_path = path

    def load_image(self):
        """Loads an image file from disc"""
        pass

    def transform_image(self):
        """Resizes picture to max width of 500px, keeping aspect ratio"""
        pass

    def add_caption(self):
        """Adds quote caption at random location into picture"""
        pass

    def make_meme(self, img, body, author):
        """
        Method creates a random meme
        Input:
        img - Image for the meme
        body - Text of a quote (String)
        author - Author of a quote (String)
        """
        pass