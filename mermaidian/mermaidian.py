'''
Provides a python interface for using Mermaid.js via the mermaid.ink service. 

Mermaid.js is a Javascript based tool for creating diagrams and charts from a set of Markdown-like text-lines.
Each type of diagram has specific syntax which is clearly document on Mermaid.js homepage.
The mermaid.ink service returns diagrams as responses to http requests in prescribed format (see https://mermaid.ink/). 
The funtions in the Mermaidian module enable you to use Mermaid.js from Python.  
Using Mermaidian you write the Mermaid diagrams text-lines 'exactly' as prescribed in the Mermaid.js documentation. 
The get_mermaid_diagram() function is used to get a diagram from mermaid.ink service.
Mermaidian functions also allow you to specify various options as key-value pairs.
For the details of available mermaid.ink options, see https://mermaid.ink/
For mermaid configuration options, see https://mermaid.js.org/config/schema-docs/config.html
Your Mermaid-text with other options is appended to the http-request to the mermaid.ink service.
The following functions are meant to be used from the calling program (other functions are internal):
get_mermaid_diagram(): The main function to get the desired diagram either as image bytes or SVG text
add_paddings_border_and_title_to_image(): To add paddings, border and title to the diagram in png or jpg format
add_paddings_border_and_title_to_svg(): To add paddings, border and title to the diagram in svg format
show_image_ipython(): For displaying diagram from an image object in IPython setting (e.g. Jupyter notebook)
show_image_ipython_centered(): Show an image diagram "centralized" only in IPython/Jupyter setting  
show_svg_ipython_centered(): Show an svg diagram "centralized" only in IPython/Jupyter setting  
show_image_pyplot(): For displaying diagram from an image object with matplotlib's pyplot
show_image_cv2(): For displaying diagram from an image object using cv2.imshow().Doesn't work in some notebooks
show_svg_ipython(): For displaying diagram from a SVG object in IPython setting (e.g. Jupyter notebook)
save_diagram_as_image(): For saving the diagram as an image (png, jpeg etc.)
save_diagram_as_svg(): For saving the diagram as a SVG file 

Functions:

    _dict_to_yaml(dict) -> YAML
    _make_frontmatter_dict(title, theme) -> dict
    _make_image_options_string(options) -> dict
    get_mermaid_diagram(format0, diagram_text, theme="forest",config={},options={}, title='') -> bytes/svg_str
    add_paddings_border_and_title_to_image(image_bytes, padding_data={}, title_data={}) -> bytes
    add_paddings_border_and_title_to_svg(svg_str, padding_data={}, title_data_svg={}) -> svg_str
    save_diagram_as_image(path, diagram) -> None
    save_diagram_as_svg(path, diagram) -> None
    show_image_ipython(image) -> None
    show_image_ipython_centered(image_bytes, margin_top, margin_bottom)
    show_image_pyplot(image) -> None
    show_image_cv2(image) -> None
    show_svg_ipython(svg) -> None
    show_svg_ipython_centered(image_bytes, margin_top, margin_bottom)

    
Main variables:

    format (string): format of the requested image e.g. "svg", "img", "png" etc.
    title (string): Title of the diagram.
    diagram_text (string): Text-lines between triple quotes for the diagram as per Mermaid.js docs.
    theme (string|dict): If string, it can take any of '','forest','neutral', 'dark' or 'base' values.
                         If a dict, it represents theme_variables (see https://mermaid.js.org/config/schema-docs/config.html)
    config (dict): a dictionary for all Mermaid.js configuration options except 'theme' and 'theme_variables'. See https://mermaid.js.org/config/schema-docs/config.html
    options (dict): Options that are applied to the requested image (see https://mermaid.ink/ ).

    padding_data_defaults = {'pad_x':40, 'pad_top':40, 'pad_bottom':40, 'pad_color':'#aaaaaa', 'border_color':'#000000', 'border_thickness':2}   
    where, pad_x is for left and right paddings and pad_y is for top and bottom paddings.
    
    title_data (dict): A dict with required title properties
    The following describes the items in the title_data with default values.
    title_data_defaults = {'title':'', 'position':'tc', 'title_margin_x':20, 'title_margin_y':20, 'font_name':'simplex', 'font_scale':0.6, 'font_color':'#000000', 'font_bg_color':'', 'font_thickness':1}   
    'position' is the title's position and can be any one of the following seven positions:
    'tl' (top-left), 'tc' (top-center), 'tr' (top-right), 'mc' (middle-center), 'bl' (bottom-left), 'bc' (bottom-center), and 'br' (bottom-right)
    'font_name' can be any cv2 font name including: 'simplex', 'plain', 'duplex', 'complex', 'triplex', 'complex_small', 'script_simplex', and 'script_complex'
    'font_scale' is a decimal vaue corresponding to font size and 'font_thickness' is an interger (usually 1 or 2) for font weight.

    title_data_svg_defaults = {'title':'', 'position':'tc', 'title_margin_x':20, 'title_margin_y':20, 'font_name':'Arial, sans-serif', 'font_size':16, 'font_color':'#000000', 'font_bg_color':'', 'font_weight':'normal'}
    'position' is the title's position and can be any one of the following seven positions:
    'tl' (top-left), 'tc' (top-center), 'tr' (top-right), 'mc' (middle-center), 'bl' (bottom-left), 'bc' (bottom-center), and 'br' (bottom-right)
    'font_name' is any of usual system's font names (e.g. 'Arial, sans-serif' ) 
    'font_size' is a usual font size (e.g. 16, 20, 32 etc.) and 'font_weight' is usual font weight (e.g. 'normal', 'bold' etc.)
     
 '''

__author__ = "Munawar Saudagar"

# =================================================================================
# Required imports

from io import BytesIO
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cv2
from PIL import Image as PImage
import base64
from IPython.display import Image, display, SVG, HTML
import requests
import yaml
import mimetypes
import math

# ---------------------------------------------------------------------------------
def _dict_to_yaml(dict):
    '''
    Returns the YAML equivalent of an input dictionary. The  returned YAML is delimited by three dashes

            Parameters:
                    dict (dict): A dictionary of key-value pairs

            Returns:
                    yaml_string_with_3dashes (yaml): YAML equivalent of the input dictionary
    '''
    yaml_without_3dashes = yaml.dump(dict)
    yaml_string_with_3dashes = f'---\n{yaml_without_3dashes}---' 
    return yaml_string_with_3dashes  

# ---------------------------------------------------------------------------------
def save_diagram_as_svg(path, diagram):
    '''
    Saves the passed diagram content as an SVG file 

            Parameters:
                    path (str): Path of the output file. 
                    diagram (SVG text): The SVG of the diagram to be saved

            Returns:
                    None
    '''   
    with open(path, 'w', encoding='utf-8') as file:
        file.write(diagram)

# ---------------------------------------------------------------------------------
def save_diagram_as_image(path, diagram):
    '''
    Saves the passed diagram content as an image file (png, jpeg etc.)  

            Parameters:
                    path (str): Path of the output file. 
                    diagram (bytes): The diagram to be saved

            Returns:
                    None
    '''
    with open(path, 'wb') as file:
        file.write(diagram)

# ---------------------------------------------------------------------------------
def show_image_ipython(image):
    '''
    Displays the image-content as an image in IPython systems (e.g. Jupyter notebooks) 
    uses IPython's 'Image' and 'display' functions
    Does not work in non-IPython cases
    For non-IPython cases use the show_image_pyplot() function  

            Parameters:
                    image (bytes): The diagram image to be displayed

            Returns:
                    None
    '''
    display(Image(image))

# ---------------------------------------------------------------------------------
def show_image_ipython_centered(image_bytes, margin_top = '40px', margin_bottom = '0px'):
    # Create an image from bytes
    image = PImage.open(BytesIO(image_bytes))
    
    # Save image temporarily in memory
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    
    # Encode the image to base64 for embedding in HTML
#     import base64
    encoded_image = base64.b64encode(buffer.getvalue()).decode()

    # Create HTML to display image centered
    html_code = f'''
    <div style="display: flex; justify-content: center; align-items: center; margin-top:{margin_top}; margin-bottom:{margin_bottom};">
        <img src="data:image/png;base64,{encoded_image}" />
    </div>
    '''

    # Display the image using IPython's display and HTML
    display(HTML(html_code)) 

# ---------------------------------------------------------------------------------

def show_image_pyplot(image):
    '''
    Displays the image-content as an image using matplotlib's pyplot
    Works across both non-IPython and IPython cases
    Not perfect for for Ipython notebooks. Use show_image_ipython() instead.
    uses numpy 'frombuffer' and cv2 'imdecode' and 'cvtColor' methods
    uses 'imshow', 'axis' and 'show' methods of matplotlib.pyplot (plt)  


            Parameters:
                    image (bytes): The diagram image to be displayed

            Returns:
                    None
    '''
    nparr = np.frombuffer(image, np.uint8)
    decoded_image = cv2.imdecode(nparr, -1)
    rgb_image = cv2.cvtColor(decoded_image, cv2.COLOR_BGR2RGB)
        
    # Acquire default dots per inch value of matplotlib
    dpi = matplotlib.rcParams['figure.dpi']
    # Determine the figures size in inches to fit your image
    height, width, depth = rgb_image.shape
    figsize = width / float(dpi), height / float(dpi)
    plt.figure(figsize=figsize)

    plt.axis('off')
    fig=plt.imshow(rgb_image)
    plt.show()  
    
# ---------------------------------------------------------------------------------
def show_image_cv2(image):
    '''
    Displays the image-content as an image using cv2.imshow()
    Works only with non-IPython. Does not work in some Jupyter notebook 
    To fix this in Colab use 'from google.colab.patches import cv2_imshow' and use 'cv2_imshow' in place of cv2.imshow
    uses numpy 'frombuffer' and cv2 'imdecode' and 'cvtColor' methods
    uses 'imshow()' function of cv2


            Parameters:
                    image (bytes): The diagram image to be displayed

            Returns:
                    None
    '''
    nparr = np.frombuffer(image, np.uint8)
    decoded_image = cv2.imdecode(nparr, -1)
    rgb_image = cv2.cvtColor(decoded_image, cv2.COLOR_BGR2RGB)
    cv2.imshow("", decoded_image)
    cv2.waitKey(0)
    # closing all open windows
    cv2.destroyAllWindows()
    
# ---------------------------------------------------------------------------------
def show_svg_ipython(svg):
    '''
    Displays the SVG-text as an SVG in IPython systems (e.g. Jupyter notebooks) 
    uses IPython's 'SVG' and 'display' functions
    Does not work in non-IPython cases

            Parameters:
                    svg (text): The svg text to be displayed

            Returns:
                    None
    '''
    display(SVG(svg))
    
# --------------------------------------------------------------------------------
def show_svg_ipython_centered(svg_string, margin_top = '40px', margin_bottom = '0px'):
    # Encode SVG string to base64
    svg_base64 = base64.b64encode(svg_string.encode('utf-8')).decode('utf-8')
    
    # Create HTML to display the SVG centered without scroll bars
    html_code = f'''
    <div style="display: flex; justify-content: center; align-items: center; width: 100%; margin-top:{margin_top}; margin-bottom:{margin_bottom} ">
        <img src="data:image/svg+xml;base64,{svg_base64}" style="max-width: 100%; max-height: 100%;"/>
    </div>
    '''
    
    # Display the SVG using IPython's display and HTML
    display(HTML(html_code))

# --------------------------------------------------------------------------------
def _make_image_options_string(options): 
    '''
    Converts the image options given in a dictionary to a query string.
    The query string is then appended to the http get request to mermaid.ink 

            Parameters:
                    options (dict): a dict of option-value pairs. Some valid options include "bgColor", "width", "scale" etc.

            Returns:
                    query_string: A  string starting with "?" and having option=value pairs separated by "&"
    '''    
    keys = options.keys()    
    image_options_string = ""
    for key in keys:
        image_options_string += "&" + key.strip() + "=" + options[key].strip()
    query_string = "?" + image_options_string[1:]
    return query_string

# ---------------------------------------------------------------------------------
def _make_frontmatter_dict(title, theme, configin):
    '''
    Creates a dictionary for frontmatter of the code for a Mermaid diagram.
    In Mermaid.js the frontmatter is a YAML for specifying title, theme and other configurations
    The frontmatter dictionary contains key-value pairs.
    The keys may include 'title' and other theme_variables (see Mermaid.js docs)

            Parameters:
                    title (str): Title of the diagram
                    theme (str/dict): The theme of the Mermaid diagram. Can be a string or a dict
                           If string, then it can take one of 'forest', 'dark', 'neutral' and 'base' values.
                           If dict, then it can have option-value pairs for theme_variables (see https://mermaid.js.org/config/schema-docs/config.html)
                    config (dict): a dictionary for all Mermaid.js configuration options except 'theme' and 'theme_variables'.
                            (See https://mermaid.js.org/config/schema-docs/config.html)
            Returns:
                    The frontmatter dictionary contains  key-value pairs for various theme options  
    ''' 
    frontmatter = {'config':{}}
    if title != '':
        frontmatter = {'title': title, 'config':{}}        
    
    if type(theme) is str:
        frontmatter['config']['theme'] = theme       
    else:
        frontmatter['config']['theme'] = 'base'
        frontmatter['config']['themeVariables'] = theme
    
    if isinstance(configin, dict) and configin!={}:
        keys = configin.keys()    
        for key in keys:
            frontmatter['config'][key] = configin[key]       
    return frontmatter

# ---------------------------------------------------------------------------------
def get_mermaid_diagram(format0, diagram_text, theme="forest",config={},options={}, title=''):
    
    '''
    Sends a 'get' request to "https://mermaid.ink/" to get a diagram.
    The request includes a string of frontmatter, diagram-string, and options 
    
            Parameters:
                    format (str): The format of the requested diagram e.g. 'pdf', 'png','jpeg' or 'svg' etc.
                    title (str): Title of the diagram
                    diagram_text: The actual Mermaid code for the diagram as per Mermaid.js documentation 
                    theme (str/dict): The theme of the Mermaid diagram. Can be a string or a dict
                           If string, then it can take one of 'forest', 'dark', 'neutral' and 'base' values.
                           If dict, then it can have option-value pairs for theme_variables (see https://mermaid.js.org/config/schema-docs/config.html)
                    config (dict): a dictionary for all Mermaid.js configuration options except 'theme' and 'theme_variables'.
                           (See https://mermaid.js.org/config/schema-docs/config.html)
   
                    options (dict): a dict of option-value pairs. Some valid options include "bgColor", "width", "scale" etc. (see https://mermaid.ink)
                    title (str): Title of the diagram. Default is ''. 
                    
            Returns:
                    diagram_content: The diagram content in the requested form 
    '''   
    if format0 == 'jpg':
        format0 = 'jpeg'
    
    if format0 == 'svg':
        format = 'svg'
    elif format0 == 'pdf':
        format = 'pdf'             
    else:
        format = 'img'
        if format0 == 'jpeg' or format0 == 'png' or format0 == 'webp' :
            options['type']  = format0                    
    image_options_string = _make_image_options_string(options)
    frontmatter_dict = _make_frontmatter_dict(title, theme, config)
#     frontmatter_dict = _make_frontmatter_dict(title, theme)
    frontmatter_yaml = _dict_to_yaml(frontmatter_dict)
    graph_string = frontmatter_yaml + diagram_text
    graphbytes = graph_string.encode("utf8")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    url_string = f"https://mermaid.ink/{format}/{base64_string}{image_options_string.strip()}"
    diagram = requests.get(url_string)

    #  diagram.text returns a string object, it is used for text files, such as SVG (.svg), HTML (.html) file, etc.
    #  diagram.content returns a bytes object, it is used for binary files, such as PDF (.pdf), audio file, image (.png, .jpeg etc.), etc.
    diagram_content = diagram.text if format == "svg" else diagram.content
    return diagram_content


# =================================================================================
# Functions for adding paddings, border and title to images (png or jpg)
# =================================================================================

# ---------------------------------------------------------------------------------
# A function to get x and y coordinate of title string
def get_title_xy(image_width, image_height, title_width, title_height, position='tc', title_margin_y = 20, title_margin_x = 15):
    if position == 'tl' or position == 'tc' or position == 'tr':
        title_y = title_height + title_margin_y
    else:
        title_y = image_height-(title_height + title_margin_y)
        
    if position == 'tl' or position == 'bl':
        title_x = title_margin_x
    elif position == 'tc' or position == 'bc':
        title_x = (image_width - title_width) // 2    
    elif position == 'tr' or position == 'br':
        title_x = image_width - (title_width + title_margin_x)        
    return (title_x, title_y)  

# ---------------------------------------------------------------------------------    
# Define a function to convert a hexadecimal color code to a BGR tuple
def hex_to_bgr(hex):
    hex=hex.replace('#', '')  # if hex starts with '#', replace it with '' (effectively remove '#')
    # Use a generator expression to convert pairs of hexadecimal digits to integers and create a tuple
    rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    bgr = tuple(reversed(rgb))
    return bgr

# ---------------------------------------------------------------------------------    
# Define a function to convert a hex color code to a BGRA tuple
def hex_to_bgra(hex):
    hex=hex.replace('#', '')  # if hex starts with '#', replace it with '' (effectively remove '#')
    if len(hex) == 6:
        hex = hex + 'ff' 
    abgr = list(int(hex[i:i+2], 16) for i in (0, 2, 4, 6)[::-1])
    bgr = abgr[1:]
    bgra_list = [*bgr, abgr[0]]
    bgra_tuple = tuple(bgra_list)
    return bgra_tuple

# ---------------------------------------------------------------------------------    
def get_bgr_and_bgra(hex):
    if len(hex) == 7:
        hex += 'ff'  # Assume fully opaque if no alpha is provided
    bgr = hex_to_bgr(hex[:7])
    bgra = hex_to_bgra(hex)
    return bgr, bgra

# ---------------------------------------------------------------------------------
def get_image_format(image_bytes):
    if image_bytes[:2] == b'\xff\xd8':
        return '.jpeg'  # JPEG format
    elif image_bytes[:8] == b'\x89PNG\r\n\x1a\n':
        return '.png'  # PNG format
    elif image_bytes[:4] == b'GIF8':
        return '.gif'  # GIF format
    elif image_bytes[:4] == b'%PDF':
        return '.pdf'  # PDF format
    elif image_bytes[:4] == b'RIFF' and image_bytes[8:12] == b'WEBP':
        return '.webp'  # WEBP format
    else:
        return None     
    
# ---------------------------------------------------------------------------------    
def add_paddings_border_and_title_to_image(image_bytes, padding_data={}, title_data={}):
    '''
    Adds paddings, border and title to Mermaid.js 'png' or 'jpg' diagrams using cv2 methods

            Parameters:
                    image_bytes (bytes): the 'png' or 'jpg' diagram's binary data
                    padding_data (dict): A dict with required padding and border properties
                    The following describes the items in the padding_data with default values.
                    padding_data_defaults = {'pad_x':40, 'pad_top':40, 'pad_bottom':40, 'pad_color':'#aaaaaa', 'border_color':'#000000', 'border_thickness':2}   
                    where, pad_x is for left and right paddings and pad_y is for top and bottom paddings.
                    title_data (dict): A dict with required title properties
                    The following describes the items in the title_data with default values.
                    title_data_defaults = {'title':'', 'position':'tc', 'title_margin_x':20, 'title_margin_y':20, 'font_name':'simplex', 'font_scale':0.6, 'font_color':'#000000', 'font_bg_color':'', 'font_thickness':1}   
                    'position' is the title's position and can be any one of the following seven positions:
                    'tl' (top-left), 'tc' (top-center), 'tr' (top-right), 'mc' (middle-center), 'bl' (bottom-left), 'bc' (bottom-center), and 'br' (bottom-right)
                    'font_name' can be any cv2 font name including: 'simplex', 'plain', 'duplex', 'complex', 'triplex', 'complex_small', 'script_simplex', and 'script_complex'
                    'font_scale' is a decimal vaue corresponding to font size and 'font_thickness' is an interger (usually 1 or 2) for font weight.
            Returns:
                    The diagram with specified paddings, border and title (in binary data)  
    ''' 
    
    def destructure_dict(dict, *args):
        return [dict[arg] for arg in args]
    # OpenCV font types are cv2.FONT_HERSHEY_SIMPLEX, cv2.FONT_HERSHEY_DUPLEX etc. enumerations.
    # For simplicity following dict is used to map the 
    fonts = {'simplex':0, 'plain':1, 'duplex':2, 'complex':3, 'triplex':4, 'complex_small':5, 'script_simplex':6, 'script_complex':7}
    
    # defaults
    padding_data_defaults = {'pad_x':40, 'pad_top':40, 'pad_bottom':40, 'pad_color':'#aaaaaa', 'border_color':'#000000', 'border_thickness':2}
    title_data_defaults = {'title':'', 'position':'tc', 'title_margin_x':20, 'title_margin_y':30, 'font_name':'simplex', 'font_scale':0.6, 'font_color':'#000000', 'font_bg_color':'', 'font_thickness':1}
    
    # Overwrite defaults by actual props
    padding_data = {**padding_data_defaults, **padding_data}
    title_data = {**title_data_defaults, **title_data}
    
    # Destructure into variables for easy coding
    pad_x, pad_top, pad_bottom, pad_color, border_color, border_thickness = destructure_dict(padding_data, 'pad_x', 'pad_top', 'pad_bottom', 'pad_color', 'border_color', 'border_thickness') 
        
    title, position, title_margin_x, title_margin_y, font_name, font_scale, font_color, font_bg_color, font_thickness = destructure_dict(title_data, 'title', 'position', 'title_margin_x', 'title_margin_y', 'font_name', 'font_scale', 'font_color', 'font_bg_color', 'font_thickness')
    
    # Convert all colors BGRA equivalents
    if pad_color != "":
        pad_color_bgra = hex_to_bgra(pad_color)
    border_color_bgra = hex_to_bgra(border_color)
    font_color_bgra = hex_to_bgra(font_color)
    if font_bg_color != "":
        font_bg_color_bgra = hex_to_bgra(font_bg_color)
    
    # Convert image bytes to a numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    
    # Decode image bytes to OpenCV format, preserving alpha channel by using 'cv2.IMREAD_UNCHANGED' option
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    
    # Get the height, width and channels of the original image
    height, width, channels = img.shape
    
    # Calculate the height and width of the paded image
    heightp = height + pad_top + pad_bottom
    widthp = width + 2*pad_x
        
    # Create a numpy array for the padded image with same channels as in the input image
    if pad_color != "":
        padded_img = np.full((heightp, widthp, channels), pad_color_bgra[:channels], dtype=np.uint8)
    else:
        padded_img = np.zeros((heightp, widthp, channels),dtype=np.uint8)
    
    # Draw a border rectangle if border_thicness>=1
    if border_thickness>=1:            
        # Calculate the top_left and bottom_right vertices for the border
        # top_left = (math.ceil(border_thickness/2), math.ceil(border_thickness/2+1))
        top_left = (math.ceil(border_thickness/2), math.ceil(border_thickness/2))
        bottom_right = (widthp-math.ceil(border_thickness/2)-1, heightp-math.ceil(border_thickness/2)-1)
        cv2.rectangle(padded_img, top_left, bottom_right, border_color_bgra[:channels], border_thickness)
        
    if title !='':
        # Determine text_size of the title      
        text_size = cv2.getTextSize(title, fonts[font_name], font_scale, font_thickness)[0]

        # Calculate title x and y positions
        text_x, text_y = get_title_xy(padded_img.shape[1], padded_img.shape[0], text_size[0], text_size[1], position, title_margin_y, title_margin_x)

        # Add a rectangle of bg_color behind the text for better visibility
        if font_bg_color != '':
            top_left_corner = (text_x - 10, text_y - text_size[1] - 10)
            bottom_right_corner = (text_x + text_size[0] + 10, text_y + 10)
            cv2.rectangle(padded_img, top_left_corner, bottom_right_corner, font_bg_color_bgra[:channels], -1)

        # Add text (title) on the image
        cv2.putText(padded_img, title, (text_x, text_y), fonts[font_name], font_scale, font_color_bgra[:channels], font_thickness, cv2.LINE_AA)
    
        
    # Put title text on the padded image     
#     cv2.putText(padded_img, "Organization Chart", (50, 50), fonts[font_name], 
#             font_scale, font_color_bgra[:channels], font_thickness, lineType=cv2.LINE_AA)
    
    # Place the original image on empty padded image.
    padded_img[pad_top:pad_top + height, pad_x:pad_x + width] = img   
        
    # Detect image format
    image_format = get_image_format(image_bytes)
    if image_format is None:
        image_format = 'png'  # Fallback to PNG if format detection fails 
        
    # Encode the padded image back to the original format   
    _, img_encoded = cv2.imencode(f'.{image_format}', padded_img)
    
    # Convert to bytes
    padded_image_bytes = img_encoded.tobytes()
    
    return padded_image_bytes           

# =================================================================================
# Functions for adding paddings, border and title to SVGs
# =================================================================================

# ---------------------------------------------------------------------------------    
def get_svg_attribute_value(svg, attribute):
    attribute_value = None
    svg_root = ET.fromstring(svg)
    for element in svg_root.iter():
        if element.tag.endswith('svg'):            
            if attribute in element.attrib:
                attribute_value = element.attrib.get(attribute)
                break
    return attribute_value 

# ---------------------------------------------------------------------------------    
def is_attribute_in_svg(svg, attribute):
    attribute_value = get_svg_attribute_value(svg, attribute)
    if attribute_value == None:
        return False
    else:
        return True
    
# ---------------------------------------------------------------------------------    
def get_svg_aspect_ratio_from_viewbox(svg):    
    viewbox_value = get_svg_attribute_value(svg, 'viewBox')
    if viewbox_value == None:
        return None
    else:
        viewbox_strings = viewbox_value.split(' ')
        viewbox_floats = [float(x) for x in viewbox_strings]
        aspect_ratio = viewbox_floats[2]/viewbox_floats[3]
        return aspect_ratio  

# ---------------------------------------------------------------------------------    
def get_mermaid_svg_width_and_height(svg):
    svg_aspect_ratio = get_svg_aspect_ratio_from_viewbox(svg)
    svg_width = get_svg_attribute_value(svg, 'width')
    if svg_width == '100%':
        svg_width = None
    if svg_width==None:
        svg_height = get_svg_attribute_value(svg, 'height')
        if svg_height != None:
            svg_height_float = float(svg_height.replace('px', ''))
            svg_width_float = svg_aspect_ratio*svg_height_float
            print(svg_height, svg_height_float, svg_width_float)
        else:
            svg_width_float = 500.0
    else:
        svg_width_float = float(svg_width.replace('px', ''))      
            
    svg_height_float = svg_width_float/svg_aspect_ratio
    return svg_width_float, svg_height_float

# ---------------------------------------------------------------------------------    
def add_paddings_border_and_title_to_svg(svg_str, padding_data={}, title_data_svg={}):
    '''
    Adds paddings, border and title to Mermaid.js 'svg' diagrams using xml.etree.ElementTree (ET)

            Parameters:
                    svg_str (string): the 'svg' diagram's string
                    padding_data (dict): A dict with required padding and border properties
                    The following describes the items in the padding_data with default values.
                    padding_data_defaults = {'pad_x':40, 'pad_top':40, 'pad_bottom':40, 'pad_color':'#aaaaaa', 'border_color':'#000000', 'border_thickness':2}   
                    where, pad_x is for left and right paddings and pad_y is for top and bottom paddings.
                    title_data_svg (dict): A dict with required title properties.
                    The following describes the items in the title_data_svg with default values.
                    title_data_svg_defaults = {'title':'', 'position':'tc', 'title_margin_x':20, 'title_margin_y':20, 'font_name':'Arial, sans-serif', 'font_size':16, 'font_color':'#000000', 'font_bg_color':'', 'font_weight':'normal'}
                    'position' is the title's position and can be any one of the following seven positions:
                    'tl' (top-left), 'tc' (top-center), 'tr' (top-right), 'mc' (middle-center), 'bl' (bottom-left), 'bc' (bottom-center), and 'br' (bottom-right)
                    'font_name' is any of usual system's font names (e.g. 'Arial, sans-serif' ) 
                    'font_size' is a usual font size (e.g. 16, 20, 32 etc.) and 'font_weight' is usual font weight (e.g. 'normal', 'bold' etc.)
            Returns:
                    The diagram with specified paddings, border and title (in binary data)  
    ''' 
    
    set_width = get_svg_attribute_value(svg_str, 'width')
    if set_width == '100%':
        set_width = None        
    set_height = get_svg_attribute_value(svg_str, 'height')  
    
    if (set_width == None) and (set_height == None):
        return svg_str
    
    def destructure_dict(dict, *args):
        return [dict[arg] for arg in args]
    
    # defaults
    padding_data_defaults = {'pad_x':40, 'pad_top':40, 'pad_bottom':40, 'pad_color':'#aaaaaa', 'border_color':'#000000', 'border_thickness':1}
    title_data_svg_defaults = {'title':'', 'position':'tc', 'title_margin_x':20, 'title_margin_y':20, 'font_name':'Arial, sans-serif', 'font_size':16, 'font_color':'#000000', 'font_bg_color':'', 'font_weight':'normal'}
    
    # Overwrite defaults by actual props
    padding_data = {**padding_data_defaults, **padding_data}
    title_data_svg = {**title_data_svg_defaults, **title_data_svg}
    
    # Destructure into variables for easy coding
    pad_x, pad_top, pad_bottom, pad_color, border_color, border_thickness = destructure_dict(padding_data, 'pad_x', 'pad_top', 'pad_bottom', 'pad_color', 'border_color', 'border_thickness') 
        
    title, position, title_margin_x, title_margin_y, font_name, font_size, font_color, font_bg_color, font_weight = destructure_dict(title_data_svg, 'title', 'position', 'title_margin_x', 'title_margin_y', 'font_name', 'font_size', 'font_color', 'font_bg_color', 'font_weight')
   
    if pad_color == '':
        pad_color = 'transparent'
        # Parse the original SVG string
    svg_root = ET.fromstring(svg_str)

    # Get the width and height of the original svg
    width, height = get_mermaid_svg_width_and_height(svg_str)
    
    # Calculate the height and width of the paded svg
    heightp = height + pad_top + pad_bottom
    widthp = width + 2*pad_x
    
    # Create the outer SVG element with increased width and height from paddings
    outer_svg = ET.Element('svg', {
        'width': str(widthp),
        'height': str(heightp),
        'xmlns': 'http://www.w3.org/2000/svg'
    })
    
    top_left = (math.ceil(border_thickness/2), math.ceil(border_thickness/2))
#     bottom_right = (widthp-math.ceil(border_thickness/2)-1, heightp-math.ceil(border_thickness/2)-1)
    bottom_right = (widthp-math.ceil(border_thickness/2)-0, heightp-math.ceil(border_thickness/2))
    # bottom_right = (widthp-math.ceil(border_thickness/2)-1, heightp-math.ceil(border_thickness/2))

    # Create a rect for 
    outer_rect_element = ET.Element('rect', {
        'x': str(0),
        'y': str(0),
        'width': str(widthp),
        'height': str(heightp), 
        'fill': pad_color
    })
    
    # Create a rect for border
    outer_rect_border = ET.Element('rect', {
        'x': str(top_left[0]),
        'y': str(top_left[1]),
        'width': str(bottom_right[0]-top_left[0]),
        'height': str(bottom_right[1]-top_left[1]), 
        'fill': 'transparent',
        'stroke': border_color,
        'stroke-width': str(border_thickness)
    })
    
    outer_svg.append(outer_rect_element)
    outer_svg.append(outer_rect_border)
    
    # Insert the original SVG inside the outer SVG, with y-offset for the title and padding
    
    pad_avg = 0.5*(pad_top + pad_bottom)
    delta_pad_top = pad_top - pad_avg
        
    if set_width != None and set_height != None:
        svg_root.attrib['x'] = str(pad_x)+'px'
        svg_root.attrib['y'] = str(pad_top)+'px'
    else:        
        if set_height == None:
            svg_root.attrib['x'] = str(pad_x)+'px'
            svg_root.attrib['y'] = str(delta_pad_top)+'px'
        if set_width == None:
            svg_root.attrib['y'] = str(pad_top)+'px'
            
    outer_svg.append(svg_root)
    
        
    if title !='':        
        # Estimate title width based on character count
        avg_char_width = font_size/2  # average width of a character in pixels for font-size 16
        title_width = avg_char_width * len(title)
        title_height = font_size       

        # Calculate title x and y positions
        text_x, text_y = get_title_xy(widthp, heightp, title_width, title_height, position, title_margin_y, title_margin_x)
    
        # Create the title text element
        title_element = ET.Element('text', {
            'x': str(text_x),
            'y': str(text_y),
            'font-size': str(font_size),
            'stroke': 'black',
            'stroke-width': '0',
            'fill': font_color,
            'font-weight': font_weight,
#             'font-style': 'italic',
#             'font-family': 'Script',
            'font-family': font_name
        })
        title_element.text = title
        
        # Add a rectangle of bg_color behind the text for better visibility
        if font_bg_color != '':
            top_left_corner = (text_x - 0, text_y - title_height)
            bottom_right_corner = (text_x + title_width + 0, text_y + 0)
            title_rect = ET.Element('rect', {
                'x': str(text_x - 7),
                'y': str(text_y-title_height),
                'width': str(title_width),
                'height': str(title_height + 10), 
                'fill': font_bg_color,
                'fill-opacity': str(0.5),
                'stroke': '#000000',
                'stroke-width': '0'
            })
            outer_svg.append(title_rect)
             
        outer_svg.append(title_element)


    # Convert the outer SVG element back to string
    outer_svg_str = ET.tostring(outer_svg, encoding='unicode', method='xml')
        
    # Remove namespace prefixes by replacing 'ns0:' with ''
    outer_svg_str = outer_svg_str.replace('ns0:', '')

    return outer_svg_str    

# ---------------------------------------------------------------------------------    