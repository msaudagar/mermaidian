# un-comment following for running mermaidian from project directory without installing mermaidian from PyPI
import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mermaidian'))) 

import mermaidian as mm

out_path = 'output'

def get_and_show_diagram(format, title, diagram_text, theme='default', config={}, options={}):
  diagram = mm.get_mermaid_diagram(format, title, diagram_text, theme, config, options)
  mm.show_image_pyplot(diagram)
  mm.show_image_cv2(diagram)
  return diagram

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

get_and_show_diagram('jpeg', "Organization Chart", org_chart_text)

llm_in_business = """
mindmap
  root(LLM / GPT Uses in Business)
    ))Customer Service((
      Chatbots
      Email Support
      Call Center Assistance
    ))Marketing((
      Content Creation
      SEO Optimization
      Ad Copywriting
    ))Human Resources(
      Recruitment Assistance
      Employee Training
      Policy Documentation
    ))Data Analysis((
      Data Cleaning
      Predictive Analytics
      Report Generation
    ))Sales((
      Lead Generation
      Sales Forecasting
      Personalized Sales Pitches
"""
config = {'fontSize':'10px',
          "mindmap": {"maxNodeWidth": 130,"padding": 25}
         }

theme = {'primaryColor':'#00ff00',
         'secondaryColor':'#f97316',
         'primaryTextColor': '#ffffff',
#          'tetiaryTextColor':'#ffffff',
         'tertiaryColor':'#ff0000',
         'tertiaryTextColor': '#fff',
         'lineColor': '#aaaaaa',
         'fontSize':'18px',
         'primaryBorderColor': '#ffffff'
        }
options = {'bgColor':'000000','width':'1200', 'height': '600' , 'scale':'1.0' }
get_and_show_diagram('jpeg', 'Mindmap', llm_in_business, theme, config, options)

