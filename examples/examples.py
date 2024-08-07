# un-comment following for running mermaidian from project directory without installing mermaidian from PyPI
import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mermaidian'))) 

import mermaidian as mm

out_path = 'output'

def get_and_show_diagram(format, title, diagram_text, theme='default', config={}, options={}):
  diagram = mm.get_mermaid_diagram(format, title, diagram_text, theme, config, options)
  mm.show_image_pyplot(diagram)
  return diagram

def get_show_and_save_diagram(name, format, title, diagram_text, theme='default', config={}, options={}):
  diagram = mm.get_mermaid_diagram(format, title, diagram_text, theme, config, options)
  mm.show_image_pyplot(diagram)
  mm.save_diagram_as_image(f'{out_path}/{name}.{format}', diagram)
  return diagram

# help(mm)

# A simple organization chart

# Define the diagram in Mermaid syntax.
org_chart_text = """
flowchart TB
%% Define nodes
    c[Company XYZ]
    d1[Department-1]
    d2[Department-2]
    d3[Department-3]
    d2s1[Section-1]
    d2s2[Section-2]
    d2s1t1[Team-1]
    d2s1t2[Team-2]

%% Define links
    c --- d1
    c --- d2
    c --- d3
    d2 --- d2s1
    d2 --- d2s2
    d2s1 --- d2s1t1
    d2s1 --- d2s1t2    
"""

# Get, show and save the 'org_chart' as .jpeg with default theme, config and options
get_show_and_save_diagram('org-chart_default_theme', 'jpeg', 'Organization Structure', org_chart_text)

# Change the theme to 'forest'
get_show_and_save_diagram('org-chart_forest_theme', 'jpeg', 'Organization Structure', org_chart_text, 'forest')

# Change the theme to 'dark' 
get_show_and_save_diagram('org-chart_dark_theme', 'jpeg', 'Organization Structure', org_chart_text, 'dark')

# Define styles: linkStyle and classes, and assign classes to org_chart's nodes as 'styles' string
styles = """    
%% Define links style (default means apply to all links) 
    linkStyle default stroke:#aaaaaa,stroke-width:2px;
    
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
# Concatenate org_chart_text and styles strings
org_chart_text_plus_styles = org_chart_text + styles

# Get, display and save the styled org_chart
get_show_and_save_diagram('org-chart-styled', 'jpeg', 'Organization Structure', org_chart_text_plus_styles)

# Change org_chart direction by replacing 'TB' in org_chart_text_plus_styles to 'LR'
org_chart_text_plus_styles_LR = org_chart_text_plus_styles.replace('flowchart TB', 'flowchart LR', 1)
get_show_and_save_diagram('org-chart-styled-LR', 'jpeg', 'Organization Structure', org_chart_text_plus_styles_LR)


# Flowchart showing Client-Server interaction
client_server_text = '''
flowchart LR
    subgraph AWS
        s[Server]
        db[(Database)]
    end
    subgraph Vercel
        c[Client]
    end

    c -- HTTP GET --> s
    s -. JSON .-> c    
    db -. Result Set .-> s
    s -- SQL Query --> db
'''    
theme = {'primaryColor':'#0369a1', 'primaryTextColor': '#fff', 'secondaryColor':'#312e81', 'tertiaryColor':'#4a044e', 'tertiaryTextColor': '#fff','lineColor': '#aaaaaa', 'fontSize':'10px', 'primaryBorderColor': '#ffffff', 'tertiaryBorderColor': '#ffffff'}
config = {"flowchart": {"diagramPadding": 50,"padding": 30, 'curve':'basis', "subGraphTitleMargin": {"top":10}}}
options = {'bgColor':'000000','width':'800'}

get_show_and_save_diagram('client-sever-interaction', 'jpeg', 'Client-Server Interaction', client_server_text, theme, config, options)

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
theme = 'default'
config = {}
options = {'bgColor': 'dbeafe','width':'600px','height':'300'}
jpeg2 = mm.get_mermaid_diagram('jpeg','Git Diagram', diagram2_text, theme, config ,options)
mm.save_diagram_as_image('output/jpeg2.jpeg', jpeg2)
mm.show_image_pyplot(jpeg2)

diagram3_text = '''
flowchart LR
    subgraph AWS
        s[Server]
        db[(Database)]
    end
    subgraph Vercel
        c[Client]
    end

    c -- HTTP GET --> s
    s -. JSON .-> c    
    db -. Result Set .-> s
    s -- SQL Query --> db
'''    

theme = 'default'
config = {}
options = {'bgColor': 'cccccc','width':'600px','height':'300'}
jpeg3 = mm.get_mermaid_diagram('jpeg','Client on Vercel, Server & Database on AWS', diagram3_text, theme, config ,options)
mm.save_diagram_as_image('output/jpeg3.jpeg', jpeg3)
mm.show_image_pyplot(jpeg3)


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
theme = {'primaryColor':'#fcd34d'}
config = {}
options = {'bgColor':'fef3c7', 'height':'500'}
jpeg4 = mm.get_mermaid_diagram('jpeg','Customer-Cashier Interaction', diagram4_text, theme, config, options)
mm.save_diagram_as_image('output/jpeg4.jpeg', jpeg4)
mm.show_image_pyplot(jpeg4)

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
theme = 'forest'
config = {}
options = {'bgColor': 'e5e7eb', 'width': '400'}
jpeg5 = mm.get_mermaid_diagram('jpeg', 'Entity Relationship Diagram', diagram5_text, theme, config, options)
mm.save_diagram_as_image('output/jpeg5.jpeg', jpeg5)
mm.show_image_pyplot(jpeg5)

diagram6_text = '''
%%{
  init: {
    "gantt": {
      'barHeight' :100,
      'fontSize' :32,
      'barGap' :10,
      'sectionFontSize': 32
    }
  }
}%%
gantt
    dateFormat MM
    axisFormat %B
    section Task 1
        Design the GUI :task1, 01, 91d
    section Task 2
        Write code for the GUI :task2, 02, 60d
    section Task 3
        Test the GUI :task3, 05, 30d
'''   

theme = 'forest'
config = {}
options = {'bgColor':'e0f2fe', 'height':'300'}
jpeg6 = mm.get_mermaid_diagram('jpeg', ' ', diagram6_text, theme, config, options)
mm.save_diagram_as_image('output/jpeg6.jpeg', jpeg6)
mm.show_image_pyplot(jpeg6)
