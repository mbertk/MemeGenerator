from PIL import Image, ImageFont, ImageDraw
from random import randint


class MemeEngine:
    """
    MemeEngine class creates memes
    """

    def __init__(self, path):
        self.file_path = path

    def make_meme(self, path, body, author, width=500) -> str:
        """Method creates a random meme
        path -- path to Image
        body -- Text of a quote (String)
        author -- Author of a quote (String)
        """

        with Image.open(path) as image:
            # copy image to new object
            meme = image.copy()
            # resize
            meme.thumbnail(width)
            # add caption
            draw = ImageDraw.Draw(meme)
            random_x = randint(10, width - 50)
            random_y = randint(10, width - 50)
            font =  ImageFont.truetype("src/_data/fonts/comici.ttf", 15)
            # draw body
            draw.text((random_x, random_y), body, font=font, encoding="unic", fill='red' )
            # save file
            file_path = f"{self.file_path}/{randint(0,1000)}.png"
            meme.save(file_path)

        return file_path

