# import pymermaid as mm
import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mermaidpy'))) 
import mermaidpy as mmp

# help(mm)

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

diagram1_text_plus_styles = diagram1_text + styles

jpeg1 = mmp.get_mermaid_diagram('jpeg','Organization Structure', diagram1_text_plus_styles)
mmp.save_diagram_as_image('output/jpeg1.jpeg', jpeg1)
mmp.show_image_pyplot(jpeg1)

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

jpeg2 = mmp.get_mermaid_diagram('jpeg','Git Diagram', diagram2_text, 'default',{'bgColor': 'dbeafe','width':'600px','height':'300'})
mmp.save_diagram_as_image('output/jpeg2.jpeg', jpeg2)
mmp.show_image_pyplot(jpeg2)

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
jpeg3 = mmp.get_mermaid_diagram('jpeg','Client on Vercel, Server & Database on AWS', diagram3_text, 'default',{'bgColor': 'cccccc','width':'600px','height':'300'})
mmp.save_diagram_as_image('output/jpeg3.jpeg', jpeg3)
mmp.show_image_pyplot(jpeg3)


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

jpeg4 = mmp.get_mermaid_diagram('jpeg','Customer-Cashier Interaction', diagram4_text, {'primaryColor':'#fcd34d'},{'bgColor':'fef3c7', 'height':'500'})
mmp.save_diagram_as_image('output/jpeg4.jpeg', jpeg4)
mmp.show_image_pyplot(jpeg4)

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

jpeg5 = mmp.get_mermaid_diagram('jpeg', 'Entity Relationship Diagram', diagram5_text,'forest', {'bgColor': 'e5e7eb', 'width': '400'})
mmp.save_diagram_as_image('output/jpeg5.jpeg', jpeg5)
mmp.show_image_pyplot(jpeg5)

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
        Test the GUI :task3, 05, 30d'''   

jpeg6 = mmp.get_mermaid_diagram('jpeg', ' ', diagram6_text,'forest', {'bgColor':'e0f2fe', 'height':'300'})
mmp.save_diagram_as_image('output/jpeg6.jpeg', jpeg6)
mmp.show_image_pyplot(jpeg6)
