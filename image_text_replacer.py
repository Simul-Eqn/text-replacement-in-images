from PIL import Image, ImageDraw, ImageFont 

  

def OpenDyslexicFontFitSize(text, w, h): # size limit in pixels 
    fontsize = 1 
    font = ImageFont.truetype("OpenDyslexic_0_91_12_regular.otf", fontsize)
    bbox = font.getbbox(text) # (left, top, right, bottom)

    # increase size until above 
    while ( (bbox[2]-bbox[0]) > w ) or ( (bbox[3]-bbox[1]) > h) : 
        fontize += 1 
        font = font.font_variant(size=fontsize) 
        bbox = font.getbbox(text) # (left, top, right, bottom) 

    # decrease back so it'll fit 
    fontsize -= 1
    font = font.font_variant("arial.ttf", fontsize)

    return font 

def ltrb_to_midxmidywh(left, top, right, bottom): 
    return (right+left)/2, (bottom+top)/2, right-left, bottom-top 

def replace_image(img:Image.Image): 
    # TODO: use Google Vision API to detect the text in the image 
    # i think helpful Google Vision API docs link: https://cloud.google.com/vision/docs/ocr#vision_text_detection-python 

    ress = [] 
    # bbox is (midx, midy, width, height) 

    draw = ImageDraw.Draw(img) 
    for (text, bbox) in ress: 

        # TODO: account for bg colour? or even remove the text and try to recover background maybe 
        draw.rectangle( (bbox[0],bbox[1]) ) 

        # TODO: account for text colour? 
        draw.text( (bbox[0],bbox[1]) , text , font=OpenDyslexicFontFitSize(text, bbox[1], bbox[2]) ) 
    return img 


