import os 
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'detectors/Vision_API_detector/opendyslexic-text-replacement-apikey.json'

import io 

from PIL import Image 

from google.cloud import vision 

def PIL_to_bytearray(img:Image.Image): 
    img_byte_arr = io.BytesIO() 
    img.save(img_byte_arr, format='PNG') 
    return img_byte_arr.getvalue() 



def vision_api_get_texts_bboxes_dirns(img:Image.Image): 

    client = vision.ImageAnnotatorClient() 
    image = vision.Image(content=PIL_to_bytearray(img)) 

    response = client.text_detection(image) 

    if response.error.message: 
        print("CHECK https://cloud.google.com/apis/design/errors")
        raise Exception(response.error.message) 
    
    texts = response.text_annotations 

    ress = [] 
    for text in texts: 
        if '\n' in text.description: # multiline will be detected twice, so skip it. 
            continue 
        

        # get bbox that's guaranteed to fit 

        xs = [] 
        ys = [] 
        for vertex in text.bounding_poly.vertices: # the first one will be the top left 
            xs.append(vertex.x) 
            ys.append(vertex.y) 
        
        sxs = sorted(xs) 
        sys = sorted(ys) 
        ltrb = sxs[1], sys[1], sxs[2], sys[2] # bbox that's guaranteed to fit 


        # get direction 
        tl = text.bounding_poly.vertices[0] 
        is_right = ( abs(tl.x-ltrb[0]) > abs(tl.x-ltrb[2]) ) # if it's closer to rightmost 
        is_bottom = ( abs(tl.y-ltrb[1]) > abs(tl.y-ltrb[3]) ) # if it's closer to bottommost 
        if ( (not is_right) and (not is_bottom) ): 
            dirn = 0 # upright 
        elif is_right: 
            if is_bottom: 
                dirn = 2 # upside down 
            else: 
                dirn = 1 # rotated clockwise 90 deg 
        else: 
            dirn = 3 

        #print('"'+text.description+'":',dirn, ltrb, tl) 

        ress.append((text.description, ltrb, dirn)) 

    return ress 
