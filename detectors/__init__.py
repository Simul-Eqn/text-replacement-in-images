from .opencv_EAST_detector import opencv_east_get_texts_bboxes_dirns 
from .Vision_API_detector import vision_api_get_texts_bboxes_dirns 

from PIL import Image 

names_fns = {
    'Vision API': vision_api_get_texts_bboxes_dirns, 
    'OpenCV EAST': opencv_east_get_texts_bboxes_dirns, 
}

def get_texts_bboxes_dirns(img:Image.Image, get_with='OpenCV EAST'): 
    assert get_with in names_fns.keys(), 'get_with not found: '+get_with 
    return names_fns[get_with](img) 
    
    '''if get_with == 'Vision API': 
        return vision_api_get_texts_bboxes_dirns(img) 
    elif get_with == 'OpenCV EAST': 
        return opencv_east_get_texts_bboxes_dirns(img) ''' 


