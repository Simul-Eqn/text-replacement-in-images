import os 
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'opendyslexic-text-replacement-20cd000fb0b1.json'

import io 

from PIL import Image, ImageDraw, ImageFont 

from google.cloud import vision 
  

def OpenDyslexicFontFitSize(text, w, h): # size limit in pixels
    fontsize = 1
    font = ImageFont.truetype("OpenDyslexic_0_91_12_regular.otf", fontsize)
    bbox = font.getbbox(text) # (left, top, right, bottom)

    #print(fontsize)
    #print(w, bbox[2]-bbox[0])
    #print(h, bbox[3]-bbox[1])

    # increase size until above
    while not ( ( (bbox[2]-bbox[0]) > w ) or ( (bbox[3]-bbox[1]) > h) ):
        fontsize += 1
        font = font.font_variant(size=fontsize)
        bbox = font.getbbox(text) # (left, top, right, bottom)
        #print(fontsize)
        #print(w, bbox[2]-bbox[0])
        #print(h, bbox[3]-bbox[1])

    # decrease back so it'll fit
    fontsize -= 1
    font = font.font_variant(size=fontsize)
    #print("FINAL FONT SIZE:", fontsize)

    return font

def ltrb_to_midxmidywh(left, top, right, bottom): # (midx, midy, width, height) 
    return (right+left)/2, (bottom+top)/2, right-left, bottom-top 

def PIL_to_bytearray(img:Image.Image): 
    img_byte_arr = io.BytesIO() 
    img.save(img_byte_arr, format='PNG') 
    return img_byte_arr.getvalue() 

def get_text_bboxes(img:Image.Image): 
    # TODO: use Google Vision API to detect the text in the image 
    # i think helpful Google Vision API docs link: https://cloud.google.com/vision/docs/ocr#vision_text_detection-python 

    client = vision.ImageAnnotatorClient() 
    image = vision.Image(content=PIL_to_bytearray(img)) 

    response = client.text_detection(image) 

    if response.error.message: 
        print("CHECK https://cloud.google.com/apis/design/errors")
        raise Exception(response.error.message) 
    
    texts = response.text_annotations 

    ress = [] 
    skippedfirst = False 
    for text in texts: 
        if not skippedfirst: 
            skippedfirst = True 
            continue 
        xs = [] 
        ys = [] 
        for vertex in text.bounding_poly.vertices: 
            xs.append(vertex.x) 
            ys.append(vertex.y) 
        
        sxs = sorted(xs) 
        sys = sorted(ys) 
        ltrb = sxs[1], sys[1], sxs[2], sys[2] # bbox that's guaranteed to fit 
        ress.append((text.description, ltrb)) 
    return ress 


def replace_image(img:Image.Image): 

    ress = get_text_bboxes(img) # each bbox is (left, top, right, bottom)
    

    draw = ImageDraw.Draw(img) 
    for (text, ltrb) in ress: 

        # TODO: account for bg colour? or even remove the text and try to recover background maybe 
        draw.rectangle( ltrb , fill="white" ) 

        bbox = ltrb_to_midxmidywh(*ltrb) 

        # TODO: account for text colour? 
        draw.text( (ltrb[0], ltrb[1]) , text , font=OpenDyslexicFontFitSize(text, bbox[2], bbox[3]) , fill='black') 
    return img 


