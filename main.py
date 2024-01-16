from typing import Union

from fastapi import FastAPI
from PIL import Image, ImageDraw, ImageFont
from fastapi.responses import Response
import io

app = FastAPI()


def get_concat_h_resize(im1, im2, resample=Image.BICUBIC, resize_big_image=True):
    if im1.height == im2.height:
        _im1 = im1
        _im2 = im2
    elif (((im1.height > im2.height) and resize_big_image) or
          ((im1.height < im2.height) and not resize_big_image)):
        _im1 = im1.resize((int(im1.width * im2.height / im1.height), im2.height), resample=resample)
        _im2 = im2
    else:
        _im1 = im1
        _im2 = im2.resize((int(im2.width * im1.height / im2.height), im1.height), resample=resample)
    dst = Image.new('RGBA', (_im1.width + _im2.width, _im1.height))
    dst.paste(_im1, (0, 0))
    dst.paste(_im2, (_im1.width, 0))
    return dst

def get_concat_v_resize(im1, im2, q, resample=Image.BICUBIC, resize_big_image=True):
    if im1.width == im2.width:
        _im1 = im1
        _im2 = im2
    elif (((im1.width > im2.width) and resize_big_image) or
          ((im1.width < im2.width) and not resize_big_image)):
        _im1 = im1.resize((im2.width, int(im1.height * im2.width / im1.width)), resample=resample)
        _im2 = im2
    else:
        _im1 = im1
        _im2 = im2.resize((im1.width, int(im2.height * im1.width / im2.width)), resample=resample)

    im_width = 533
    dst = Image.new('RGBA', (im_width, _im1.height + _im2.height))
    offset = (im_width - _im1.width) // 2
    dst.paste(_im1, (offset, 0))
    dst.paste(_im2, (offset, _im1.height))
    draw = ImageDraw.Draw(dst)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("nba.ttf", 60)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((im_width/2, (_im1.height + _im2.height)/2), q, (255,255,255), font=font, stroke_width=2, stroke_fill='black', anchor="mm")
    # draw.text((30, 370),"13.1.2024",(0,0,0),font=font)
    return dst

@app.get("/vertical_logo/{team1}/{team2}")
def read_item(team1: str, team2:str, q: Union[str, None] = ''):
    image = io.BytesIO()

    im1 = Image.open("new_logos/{}.png".format(team1)).convert("RGBA")
    im2 = Image.open("new_logos/{}.png".format(team2)).convert("RGBA")

    im = get_concat_v_resize(im1, im2, q)

    im.save(image, format='PNG')
    image.seek(0)

    return Response(content = image.read(), media_type="image/png")

@app.get("/horizontal_logo/{team1}/{team2}")
def read_item(team1: str, team2:str, q: Union[str, None] = None):
    image = io.BytesIO()

    im1 = Image.open("new_logos/{}.png".format(team1)).convert("RGBA")
    im2 = Image.open("new_logos/{}.png".format(team2)).convert("RGBA")

    im = get_concat_h_resize(im1, im2)

    im.save(image, format='PNG')
    image.seek(0)

    return Response(content = image.read(), media_type="image/png")