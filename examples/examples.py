# un-comment following for running mermaidian from project directory without installing mermaidian from PyPI
import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mermaidian'))) 

import mermaidian as mm

out_path = 'output'

# Following are base values for config, options, pad_data, title_data and title_data_svg for the examples to follow
bg_color = "#ffffff"
config0 = {'fontSize':'24px'}
options0 = {'bgColor': bg_color, 'width': '600'}  # the hex bgColor in option should be witout '#'
pad_data0 = {'pad_top': 80, 'pad_bottom':30, 'border_thickness':8, 'border_color':"#aaaaaa", 'pad_color': bg_color}
title_data0 = {'position':'tc','title':'','font_scale':0.9, 'font_thickness':1, 'font_name':'duplex', 'font_bg_color':'', 'font_color':"#000000"}
title_data_svg0 = {'position':'tc','font_name':'Arial, sans-serif', 'font_size':24, 'font_color':'#000000', 'font_bg_color':'', 'font_weight':'normal'}


# A helper function to get, show and save Mermaid.js image (png/jpg) based diagrams  
def get_show_and_save_image(diagram_code, format, file_name, title, theme='default', config={**config0}, options={**options0}, pad_data={**pad_data0}, title_data={**title_data0}):
  options['bgColor'] = options['bgColor'].replace('#', '')
  diagram = mm.get_mermaid_diagram(format, diagram_code, theme, config, options)
  title_data = {**title_data, 'title':title}
  diagramPBT = mm.add_paddings_border_and_title_to_image(diagram, pad_data, title_data)
  mm.show_image_pyplot(diagramPBT)
  if file_name!="":
    mm.save_diagram_as_image(f'{out_path}/{file_name}.{format}', diagramPBT)
    
  return diagramPBT

# A helper function to get, show and save Mermaid.js svg based diagrams   
def get_show_and_save_svg(diagram_code, format, file_name, title, theme='default',  config={**config0}, options={**options0}, pad_data={**pad_data0}, title_data_svg={**title_data_svg0}):
  options['bgColor'] = options['bgColor'].replace('#', '')
  diagram = mm.get_mermaid_diagram(format, diagram_code, theme, config, options)
  title_data_svg = {**title_data_svg, 'title':title}
  diagramPBT = mm.add_paddings_border_and_title_to_svg(diagram, pad_data, title_data_svg)
  mm.show_svg_ipython(diagramPBT)
  if file_name!="":
    mm.save_diagram_as_svg(f'{out_path}/{file_name}.{format}', diagramPBT)
    
  return diagramPBT
# ===================================================================================================
# A simple organization chart example

# Following defines the Mermaid.js code for a simple organization chart of company "XYZ" with 3 departments, 2 sections in department-2 and
# 2 teams in section-1 of department-2

org_chart_code = """
flowchart TB
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

# Example-1 Forest theme .png format
options = {**options0, 'bgColor': '#f7fee7'}
pad_data = {**pad_data0, 'pad_color': options['bgColor'], 'border_color':"#65a30d"}
get_show_and_save_image(org_chart_code, 'png', 'org-chart-forest-theme', "Org-Chart 'Forest' Theme", 'forest', options=options, pad_data=pad_data)

# Example-2 Forest theme .svg format
options = {**options0, 'bgColor': '#f7fee7', 'width': '460'}
pad_data = {**pad_data0, 'pad_color': options['bgColor'], 'border_color':"#65a30d"}
title_data_svg = {**title_data_svg0, 'font_color':'#000000'}
get_show_and_save_svg(org_chart_code, 'svg', 'org-chart-forest-theme', "Org-Chart 'Forest' Theme", 'forest', config=config0, options=options, pad_data=pad_data, title_data_svg=title_data_svg)

# Example-3 Custom theme .png format
# Using custom theme. The background color is also changed using 'bgColor' in 'options'
config = {**config0, "flowchart": {"rankSpacing": 80}}
# "linkStyle default" is to set style for all Mermaid.js connector lines (strokes)  
link_style_string = '''linkStyle default stroke:#ffffff,stroke-width:3px;'''
org_chart_code1 = org_chart_code + link_style_string

theme = {'primaryColor':'#075985',
         'primaryTextColor': '#ffffff',
         'lineColor': '#ffffff',
         'fontSize':'24px',
         'primaryBorderColor': '#ffffff'
        }
options = {**options0, 'bgColor':'#262626'}
title_data = {**title_data0, 'font_color':'#ffffff', 'title_margin_y':40}
pad_data = {**pad_data0, 'border_color': '#0ea5e9', 'pad_x':60, 'pad_top': 100, 'pad_bottom': 40, 'pad_color': options['bgColor']}
# The 'png' version of "Org-Chart 'Custom' Theme"
get_show_and_save_image(org_chart_code1, 'png', 'org-chart-custom-theme', "Org-Chart 'Custom' Theme", theme, options=options, config=config, title_data=title_data, pad_data=pad_data)

# Example-4 Custom theme .svg format
# The svg version of "Org-Chart 'Custom' Theme"
title_data_svg = {**title_data_svg0, 'font_color':'#ffffff', 'title_margin_y':40}
pad_data = {**pad_data0, 'border_color': '#0ea5e9', 'pad_x':60, 'pad_top': 100, 'pad_bottom': 40, 'pad_color': options['bgColor']}
theme = {**theme, 'fontSize':'24px'}
options = {**options0, 'bgColor':'#262626', 'width': '440'}
get_show_and_save_svg(org_chart_code1, 'svg', 'org-chart-custom-theme', "Org-Chart 'Custom' Theme", theme, config=config, title_data_svg=title_data_svg, options=options, pad_data=pad_data)

# Example-5 Using 'styles' (via 'classes') in the mermaid-code (.png format)

# Define and assign classes. Note lines starting with %% are comment lines
styles = """    
%% Define links style (default means apply to all links) 
    linkStyle default stroke:#555555,stroke-width:3px;
    
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
# Append style to org_chart_code

org_chart_code_with_styles  = org_chart_code + styles

theme = {'lineColor': '#555555'}

# The image ('png') version of "Org-Chart With Styles"
options = {**options0, 'bgColor':'#262626', 'width': '600'}
options = {**options0, 'bgColor':'#dddddd', 'width': '600'}
pad_data = {**pad_data0, 'border_color': '#555555', 'pad_x':60, 'pad_top': 100, 'pad_bottom': 40, 'pad_color': options['bgColor']}
title_data = {**title_data0, 'font_color':'#222222', 'title_margin_y':40}
get_show_and_save_image(org_chart_code_with_styles, 'png', 'org-chart-with-styles', "Org-Chart With Styles", theme, config = config0, options=options, title_data=title_data, pad_data=pad_data)

# Example-6 Using 'styles' (via 'classes') in the mermaid-code (.svg format)
options = {**options0, 'bgColor':'#dddddd', 'width': '440'}
pad_data = {**pad_data0, 'border_color': '#555555', 'pad_x':60, 'pad_top': 100, 'pad_bottom': 40, 'pad_color': options['bgColor']}
title_data_svg = {**title_data_svg0, 'font_color':'#444444', 'title_margin_y':40}
get_show_and_save_svg(org_chart_code_with_styles, 'svg', 'org-chart-with-styles', "Org-Chart With Styles", theme, config = config0, options=options, title_data_svg=title_data_svg, pad_data=pad_data)

# Example-7 A Simple Git Diagram (.png format)

git_diagram_code = '''
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

theme = {'primaryColor':'#3b82f6',
         'primaryTextColor': '#ffffff',
         'secondaryColor':'#fbbf24',
         'secondaryTextColor': '#000000',
         'fontSize':'16px',
        }

options = {**options0, 'bgColor': '#e7e5e4','width':'800px'}
title_data = {**title_data0, 'font_color':'#000000', 'title_margin_y':60, 'font_scale':1.2, 'font_name':'complex'}
pad_data = {**pad_data0, 'border_thickness':8, 'border_color': '#1e3a8a', 'pad_x':60, 'pad_top': 150, 'pad_bottom': 80, 'pad_color': options['bgColor']}

get_show_and_save_image(git_diagram_code, 'png', 'a-simple-git-diagram', "A Simple Git Diagram", theme, config = config0, options=options, title_data=title_data, pad_data=pad_data)

# Example-8 Flowchart with Subgraphs to depict a typical client-server architecture (.png format)
client_server_diagram_code = '''
flowchart LR 
    linkStyle default stroke-width:2px;
    subgraph Vercel
        c[Client]
    end    subgraph AWS
        s[Server]
        db[(Database)]
    end


    c -- HTTP GET --> s
    s -. JSON .-> c    
    db -. Result Set .-> s
    s -- SQL Query --> db
''' 
theme = {'primaryColor':'#000000',
         'secondaryColor':'#555555',        
         'tertiaryColor':'#777777',        
         'primaryTextColor': '#ffffff',
         'secondaryTextColor': '#ffffff',
         'tertiaryTextColor': '#ffffff',
         'primaryBorderColor': '#ffffff',
         'lineColor': "#312e81"
     }

options = {**options0, 'bgColor': '#e7e5e4', 'width': '800'}
pad_data = {**pad_data0, 'pad_color': options['bgColor'], 'border_color': "#1e3a8a", 'pad_x':60, 'pad_top': 150, 'pad_bottom': 80}
title_data = {**title_data0, 'font_color':'#000000', 'title_margin_y':60, 'font_scale':1.2, 'font_name':'complex'}
get_show_and_save_image(client_server_diagram_code, 'png', 'client-server architecture', "A Client-Server Architecture", theme, config = config0, options=options, title_data=title_data, pad_data=pad_data)

# Example-9  A customer-cashier interaction "Sequence Diagram" (.png format)
interaction_diagram_code = '''
sequenceDiagram
  participant C as Customer
  participant CH as Cashier
  participant E as Email System

  C->>CH:  Puts items on counter
  CH->>CH: Cashier Scans products
  CH-->>C: Gives total cost
  CH->>C: Asks for email address
  C->>CH: Provides email address
  C->>CH: Pays with cash/card
  CH->>E: Sends receipt to email 
  E-->>C: Emails receipt
  CH->>C: Gives 10% off coupon
'''
theme = {'primaryColor':'#fcd34d',
         'tertiaryColor':'#fcd34d',        
         'primaryTextColor': '#000000',
        }

options = {**options0, 'bgColor': '#ffffff', 'width': '600'}
pad_data = {**pad_data0, 'pad_color': options['bgColor'], 'border_color': "#44403c", 'pad_x':60, 'pad_top': 150, 'pad_bottom': 80}
title_data = {**title_data0, 'font_color':'#000000', 'title_margin_y':60, 'font_scale':1.0, 'font_name':'triplex'}
get_show_and_save_image(interaction_diagram_code, 'png', 'customer-cashier-interaction', "Customer-Cashier Interaction", theme, config = config0, options=options, title_data=title_data, pad_data=pad_data)

# Example-10 A Simple Entity Relationship Diagram (ERD) 
erd_code = '''
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

options = {**options0, 'bgColor': '#eeeeee', 'width': '600'}
pad_data = {**pad_data0, 'pad_color': options['bgColor'], 'border_color': "#cde498", 'pad_x':60, 'pad_top': 150, 'pad_bottom': 40}
title_data = {**title_data0, 'font_color':'#444444', 'title_margin_y':60, 'font_scale':1.1, 'font_name':'complex'}
get_show_and_save_image(erd_code, 'png', 'entity relationship diagram', "Entity Relationship Diagram", 'forest', config = config0, options=options, title_data=title_data, pad_data=pad_data)