# mermaidpy 

![Last commit](https://img.shields.io/github/last-commit/msaudagar/mermaidpy?color=green&label=Last%20commit)
![Repo size](https://img.shields.io/github/repo-size/msaudagar/mermaidpy?color=orange&label=Repo%20size)
[![Stars](https://img.shields.io/github/stars/msaudagar/mermaidpy?color=yellow&label=Stars)](https://github.com/msaudagar/Expense-Tracker-Chatbot/stargazers)
[![Forks](https://img.shields.io/github/forks/msaudagar/mermaidpy?color=orange&label=Forks)](https://github.com/msaudagar/mermaidpy/forks)


mermaidpy is a simple Python interface for using Mermaid.js diagramming capabilities from Python. It can be used from stand-alone Python settings and also from IPython based notebooks. The core Mermaid.js syntax for writing diagram code is preserved so that the user can always refer to Mermaid.js documentation. However, the creation of the frontmatter for configuration and custom theme is made easier by using a dict instead of YAML encoding. 

A sample Mermaid.js diagram generated using mermaidpy is given below: 

![Machine Learning Types](https://raw.githubusercontent.com/msaudagar/mermaidpy/main/assets/ml-bg-black2.jpeg)

## Table of Contents 📋

- [Introduction](#Introduction)
- [Technologies Used](#Technologies-Used)
- [Getting Started](#Getting-Started)
- [Examples](#Examples)
- [Contributing](#Contributing)
- [Feedback](#Feedback)
- [Conclusion](#Conclusion)
- [Contact](#Contact)
- [License](#License)
- [References](#References)

## Introduction

Mermaid.js is a Javascript based package for creating many types of diagrams and charts from declative text-lines.

The **mermaidpy** package enables you to use Mermaid.js from Python. It utilizes the mermaid.ink service for getting diagrams in response to http requests in a prescribed format. mermaidpy provides a set of Python functions for sending requests with diagram data to mermaid.ink and for getting, showing and saving the returned diagrams.

The following functions are meant to be used from the calling program (other functions are internal):
- get_mermaid_diagram(): The main function to get the desired diagram either as image binary (bytes) or SVG text
- show_image_ipython(): For displaying diagram from an image object in IPython setting (e.g. Jupyter notebook)
- show_image_pyplot(): For displaying diagram from an image object with matplotlib's pyplot
- show_svg_ipython(): For displaying diagram from a SVG object in IPython setting (e.g. Jupyter notebook)
- save_diagram_as_image(): For saving the diagram as an image (png, jpeg etc.)
- save_diagram_as_svg(): For saving the diagram as a SVG file 

The mermaidpy functions allow you to specify various options as key-value pairs. For the details of available mermaid.ink options, see https://mermaid.ink/ and for mermaid configuration options, see https://mermaid.js.org/config/schema-docs/config.html

For a detailed help description on mermaidpy, execute `help(mm)` after importing it as pmm


## Technologies-Used

- [![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
- [![Numpy](https://img.shields.io/badge/numpy-2.0.1-yellow)](https://pypi.org/project/numpy/)
- [![Matplotlib](https://img.shields.io/badge/matplotlib-3.9.1-red)](https://pypi.org/project/matplotlib/)
- [![IPython](https://img.shields.io/badge/ipython-8.26.0-green)](https://pypi.org/project/ipython/)
- [![opencv-python](https://img.shields.io/badge/opencv_python-4.10.0.84-orange)](https://pypi.org/project/opencv-python/)
- [![PyYAML](https://img.shields.io/badge/PyYAML-6.0.1-magenta)](https://pypi.org/project/PyYAML/)
- [![requests](https://img.shields.io/badge/requests-2.32.3-cyan)](https://pypi.org/project/requests/)

## Getting-Started

- Install mermaidpy using `pip install mermaidpy`
- Read the "mermaidpy Functions" section for knowing purpose and syntax of callable functions
- See the [examples](#examples) to understand how mermaidpy works.


## mermaidpy Functions

#### `get_mermaid_diagram(format, title, diagram_text, theme, options)`
```python
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
                    options (dict): a dict of option-value pairs. Some valid options include "bgColor", "width", "scale" etc.

            Returns:
                    diagram_content: The diagram content in the requested form 
    '''   
```
#### `show_image_pyplot(image)`
```python
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
```
#### `show_image_ipython(image)`
```python
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
```
#### `show_svg_ipython(svg)`
```python
    '''
    Displays the SVG-text as an SVG in IPython systems (e.g. Jupyter notebooks) 
    uses IPython's 'SVG' and 'display' functions
    Does not work in non-IPython cases

            Parameters:
                    svg (text): The svg text to be displayed

            Returns:
                    None
    '''
```
#### `save_diagram_as_image(path, diagram)`
```python
    '''
    Saves the passed diagram content as an image file (png, jpeg, pdf etc.)
    Works across both IPython and non-IPython  

            Parameters:
                    path (str): Path of the output file. 
                    diagram (bytes): The diagram to be saved

            Returns:
                    None
    '''
```
#### `save_diagram_as_svg(path, diagram)`
```python
    '''
    Saves the passed diagram content as an SVG file
    Works across both IPython and non-IPython  

            Parameters:
                    path (str): Path of the output file. 
                    diagram (SVG text): The SVG of the diagram to be saved

            Returns:
                    None
    '''   
```


## Examples

The following examples demonstrate the use of mermaidpy functions for requesting, saving and displaying Mermaid.js diagrams from Python. 

### Example 1 : A Simple Flowchart

```python
import mermaidpy as pmm

# define the diagram code/text as per Mermaid.js docs.

diagram1_text = """
flowchart TD
%% Nodes
    c[Company XYZ]
    d1[Department-1]
    d2[Department-2]
    d3[Department-3]
    d2s1[Section-1]
    d2s2[Section-2]
    d2s1t1[Team-1]
    d2s1t2[Team-2]

%% Links
    c --- d1
    c --- d2
    c --- d3
    d2 --- d2s1
    d2 --- d2s2
    d2s1 --- d2s1t1
    d2s1 --- d2s1t2    
"""
# define styes string as per Mermaid.js docs.
styles = """    
%% Define links style (default means apply to all links) 
    linkStyle default stroke:#aaaaaa,stroke-width:2px,color:red;
    
%% define classes
    classDef comp fill:#93c5fd;
    classDef dep fill:#FF9999;
    classDef sec fill:#FFDEAD;
    classDef team fill:#BDFFA4;

%% Assign classes to nodes
    class c comp;
    class d1,d2,d3 dep;
    class d2s1,d2s2 sec;
    class d2s1t1,d2s1t2 team;  
"""
# concatenate styles with the diagram1_text  
diagram1_text_plus_styles = diagram1_text + styles

# Note that only following three function calls from mermaidpy to get, save and display the diagram.
# The names of the functions clearly describe their functionalities.

jpeg1 = pmm.get_mermaid_diagram('jpeg','Organization Structure', diagram1_text_plus_styles)
pmm.save_diagram_as_image('jpeg1.jpeg', jpeg1)
pmm.show_image_pyplot(jpeg1)
```

The result of the above code is given below:


<p align="center" width="100%">
    <img width="35%" src="https://raw.githubusercontent.com/msaudagar/mermaidpy/main/assets/jpeg1.jpeg">
</p>


![Organization Structure jpeg](https://raw.githubusercontent.com/msaudagar/mermaidpy/main/assets/jpeg1.jpeg)


### Example 2 : Git Commits Diagram


```python
import mermaidpy as pmm

# define the diagram code/text as per Mermaid.js docs.

diagram2_text = '''
    gitGraph LR:
       commit
       commit
       branch develop
       commit
       commit
       commit
       checkout main
       commit
       commit
       merge develop
       commit
       commit
'''

jpeg2 = pmm.get_mermaid_diagram('jpeg','Git Diagram', diagram2_text, 'default',{'bgColor': 'dbeafe','width':'600px','height':'300'})
pmm.save_diagram_as_image('jpeg2.jpeg', jpeg2)
pmm.show_image_pyplot(jpeg2)

```

### Example 3 : Client-Server Interaction


```python
import mermaidpy as pmm

# define the diagram code/text as per Mermaid.js docs.

diagram3_text = '''
flowchart LR
    subgraph Azure
        s[Server]
        db[(Database)]
    end
    subgraph Netlify
        c[Client]
    end

    c -- HTTP GET --> s
    s -. JSON .-> c    
    db -. Result Set .-> s
    s -- SQL Query --> db
'''    
jpeg3 = pmm.get_mermaid_diagram('jpeg','Client on Netlify, Server & Database on Azure', diagram3_text, 'default',{'bgColor': 'cccccc','width':'600px','height':'300'})
pmm.save_diagram_as_image('jpeg3.jpeg', jpeg3)
pmm.show_image_pyplot(jpeg3)
```

### Example 4 : A Customer-Cashier Interaction Sequence Diagram


```python
import mermaidpy as pmm

# define the diagram code/text as per Mermaid.js docs.

diagram4_text = '''
sequenceDiagram
  participant C as Customer
  participant CH as Cashier
  participant E as Email System

  rect rgb(236, 244, 203)
  C->>CH:  Put items on counter
  CH->>CH: Cashier Scans products
  CH-->>C: Gives total cost
  CH->>C: Asks for email address
  C->>CH: Provides email address
  C->>CH: Pays with cash/card
  CH->>E: Sends receipt to email 
  E-->>C: Emails receipt
  CH->>C: Gives 10% off coupon
  end
'''

jpeg4 = pmm.get_mermaid_diagram('jpeg','Customer-Cashier Interaction', diagram4_text, {'primaryColor':'#fcd34d'},{'bgColor':'fef3c7', 'height':'500'})
pmm.save_diagram_as_image('jpeg4.jpeg', jpeg4)
pmm.show_image_pyplot(jpeg4)
```

The resulting sequence diagram is given below:

### Example 5 : A Simple Entity Relationship Diagram (ERD)


```python
import mermaidpy as pmm

# define the diagram code/text as per Mermaid.js docs.

diagram5_text = '''
    erDiagram
    CAR ||--o{ NAMED-DRIVER : allows
    CAR {
        string registrationNumber PK
        string make
        string model
        string[] parts
    }
    PERSON ||--o{ NAMED-DRIVER : is
    PERSON {
        string driversLicense PK
        string(99) firstName
        string lastName
        string phone UK
        int age
    }
    NAMED-DRIVER {
        string carRegistrationNumber PK, FK
        string driverLicence PK, FK
    }
    MANUFACTURER ||--o{ CAR : makes
    MANUFACTURER {
        string manufacturerBrand PK
        string manufacturerName 
        string(99) manufacturerAddress
    }  
'''   

jpeg5 = pmm.get_mermaid_diagram('jpeg', 'Entity Relationship Diagram', diagram5_text,'forest', {'bgColor': 'e5e7eb', 'width': '400'})
pmm.save_diagram_as_image('output/jpeg5.jpeg', jpeg5)
pmm.show_image_pyplot(jpeg5)
```

The resulting sequence diagram is given below:


## Conclusions

- mermaidpy is a set of Python functions that enable users to easily use Mermaid.js diagramming capabilities from Python. It provides a simple way to include custom theme variables in a dict form. Other image options can also be specified as key-value pairs in a dict.

- The core Mermaid.js syntax is preserved, therefore most of the Mermaid.js documentation can be referred for syntax and configuration details. 

## License

This project is licensed under the terms of the [MIT license](https://choosealicense.com/licenses/mit/)

## References

- Mermaid Diagramming and charting tool. https://mermaid.js.org/

- Mermaid Ink. https://mermaid.ink/

- Mermaid Theme Configuration.  https://mermaid.js.org/config/theming.html.

- Mermaid: Flowcharts - Basic Syntax. https://mermaid.js.org/syntax/flowchart.html