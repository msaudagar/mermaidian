'''
Provides a python interface for using Mermaid.js via the mermaid.ink service.

Mermaid.js is a Javascript based tool for creating diagrams from a set of text-lines.
The mermaid.ink service serves diagrams in response to http requests in prescribed format
The funtions in the pyMermaid module enable you to use Mermaid.js from Python
Mermaid.js diagrams are created by writing a set of language-agnostic text-lines 
In Python you write the Mermaid diagrams text-lines 'exactly' as prescribed in the Mermaid.js documentation. 
The get_mermaid_diagram() function is used to get a diagram from mermaid.ink service.
The module functions allow you to specify various options as key-value pairs
For the details of available mermaid.ink options, see https://mermaid.ink/
For mermaid configuration options, see https://mermaid.js.org/config/schema-docs/config.html
Your Mermaid-text with other options is appended to the http-request to the mermaid.ink service.
The following functions are meant to be used from the calling program (other functions are internal):
get_mermaid_diagram(): The main function to get the desired diagram either as image bytes or SVG text
show_image_ipython(): For displaying diagram from an image object in IPython setting (e.g. Jupyter notebook)
show_image_pyplot(): For displaying diagram from an image object with matplotlib's pyplot
show_svg_ipython(): For displaying diagram from a SVG object in IPython setting (e.g. Jupyter notebook)
save_diagram_as_image(): For saving the diagram as an image (png, jpeg etc.)
save_diagram_as_svg(): For saving the diagram as a SVG file 

Functions:

    _dict_to_yaml(dict) -> YAML
    _make_frontmatter_dict(title, theme) -> dict
    _make_image_options_string(options) -> dict
    get_mermaid_diagram(format, title, diagram_text, theme, config, options) -> bytes
    save_diagram_as_image(path, diagram) -> None
    save_diagram_as_svg(path, diagram) -> None
    show_image_ipython(image) -> None
    show_image_pyplot(image) -> None
    show_svg_ipython(svg) -> None
    
Main variables:

    title (string): Title of the diagram.
    diagram_text (string): Text-lines between triple quotes for the diagram as per Mermaid.js docs.
    theme (string|dict): If string, it can take any of '', 'default', 'forest', 'neutral', 'dark' or 'base' values.
                         If a dict, it represents theme_variables (see https://mermaid.js.org/config/schema-docs/config.html)
    config (dict): a dictionary for all Mermaid.js configuration options except 'theme' and 'theme_variables'. See https://mermaid.js.org/config/schema-docs/config.html
    options (dict): Options that are applied to the requested image (see https://mermaid.ink/ ).
    format (string): format of the requested image e.g. "svg", "img", "png" etc.
'''

__author__ = "Munawar Saudagar"

# Required imports

import numpy as np
import matplotlib.pyplot as plt
import cv2
import base64
from IPython.display import Image, display, SVG
import requests
import yaml


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


def show_image_pyplot(image):
    '''
    Displays the image-content as an image using matplotlib's pyplot
    Works across both IPython and non-IPython 
    uses numpy 'frombuffer' and cv2 'imdecode' and 'cvtColor' methods
    uses 'imshow', 'axis' and 'show' methods of matplotlib.pyplot (plt)  


            Parameters:
                    image (bytes): The diagram image to be displayed

            Returns:
                    None
    '''
    nparr = np.frombuffer(image, np.uint8)
    decoded_image = cv2.imdecode(nparr, -1)
    fig=plt.imshow(cv2.cvtColor(decoded_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()


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



def _make_frontmatter_dict(title, theme, configin):
    '''
    Creates a dictionary for frontmatter of the code for a Mermaid diagram.
    In Mermaid.js the frontmatter is a YAML for specifying title, theme and other configurations
    The frontmatter dictionary contains key-value pairs.
    The keys may include 'title' and other theme_variables (see Mermaid.js docs)

            Parameters:
                    title (str): Title of the diagram
                    theme (str/dict): The theme of the Mermaid diagram. Can be a string or a dict
                           If string, then it can take one of '', 'default', 'forest', 'dark', 'neutral' and 'base' values.
                           If dict, then it can have option-value pairs for theme_variables (see https://mermaid.js.org/config/schema-docs/config.html)
                    configin (dict): a dictionary for all Mermaid.js configuration options except 'theme' and 'theme_variables'.
                            (See https://mermaid.js.org/config/schema-docs/config.html for details)
            Returns:
                    The frontmatter dictionary contains  key-value pairs for various theme options  
    ''' 
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


def get_mermaid_diagram(format0, title, diagram_text, theme="default",config={},options={}):
    '''
    Sends a 'get' request to "https://mermaid.ink/" to get a diagram.
    The request includes a string of frontmatter, diagram-string, and options 
    
            Parameters:
                    format0 (str): The format of the requested diagram e.g. 'pdf', 'png','jpeg' or 'svg' etc.
                    title (str): Title of the diagram
                    diagram_text: The actual Mermaid code for the diagram as per Mermaid.js documentation 
                    theme (str/dict): The theme of the Mermaid diagram. Can be a string or a dict
                           If string, then it can take one of '', 'default', 'forest', 'dark', 'neutral' and 'base' values.
                           If dict, then it can have option-value pairs for theme_variables (see https://mermaid.js.org/config/schema-docs/config.html)
                    config (dict): a dictionary for all Mermaid.js configuration options except 'theme' and 'theme_variables'.
                           (See https://mermaid.js.org/config/schema-docs/config.html)
   
                    options (dict): a dict of option-value pairs. Some valid options include "bgColor", "width", "scale" etc. (see https://mermaid.ink)

            Returns:
                    diagram_content: The diagram content in the requested form 
    '''   
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

    

def _xmake_frontmatter_dict(title, theme):
    '''
    Creates a dictionary for frontmatter of the code for a Mermaid diagram.
    In Mermaid.js the frontmatter is a YAML for specifying title, theme and other configurations
    The frontmatter dictionary contains key-value pairs.
    The keys may include 'title' and other theme_variables (see Mermaid.js docs)

            Parameters:
                    title (str): Title of the diagram
                    theme (str/dict): The theme of the Mermaid diagram. Can be a string or a dict
                           If string, then it can take one of '', 'default', 'forest', 'dark', 'neutral' and 'base' values.
                           If dict, then it can have option-value pairs for theme_variables (see https://mermaid.js.org/config/schema-docs/config.html)

            Returns:
                    The frontmatter dictionary contains  key-value pairs for various theme options  
    ''' 
    frontmatter = {'title': title, 'config':{}}
    
    if type(theme) is str:
        frontmatter['config']['theme'] = theme       
    else:
        frontmatter['config']['theme'] = 'base'
        frontmatter['config']['themeVariables'] = theme
        
    return frontmatter

def xget_mermaid_diagram(format0, title, diagram_text, theme="forest",options={}):
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
                    options (dict): a dict of option-value pairs. Some valid options include "bgColor", "width", "scale" etc. (see https://mermaid.ink)

            Returns:
                    diagram_content: The diagram content in the requested form 
    '''   
    if format0 == 'svg':
        format = 'svg'
    elif format0 == 'pdf':
        format = 'pdf'             
    else:
        format = 'img'
        if format0 == 'jpeg' or format0 == 'png' or format0 == 'webp' :
            options['type']  = format0                    
    image_options_string = _make_image_options_string(options)
    frontmatter_dict = _make_frontmatter_dict(title, theme)
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
