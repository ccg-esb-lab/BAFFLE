#ToDo: 

#   - Integrate back light controller

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table
import dash_daq as daq
import json
import random
import time
import pandas as pd
from ctypes import *
import sys
from time import sleep
import os, random, shutil, datetime, time
import re
import argparse
import time
import numpy as np
import matplotlib.pyplot as plt
import os, random, shutil, datetime, time
from time import sleep
from ctypes import *

#Phidget specific imports (stepper22)
from Phidget22.Devices.DigitalInput import *
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.Stepper import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalInput import DigitalInput

# Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse
from pythonosc import udp_client

########################## Import libraries

CODE_path='./lib/'  #MyCloud/rpm/ESB_CODDE/ESBOT_data
sys.path.insert(0, CODE_path)
from baffle import *

df_params=getParams()


########################## OSC setup

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=2345,
      help="The port the OSC server is listening on")
args = parser.parse_args()
client = udp_client.SimpleUDPClient(args.ip, args.port)


########################## CSS STYLESHEETS

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.GRID])
#app.css.append_css({'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'})
app.css.config.serve_locally = False
app.css.append_css({'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'})
theme = {
    'dark': True,
    'detail': '#77C3E5',
    'primary': '#77C3E5', 
    'secondary': '#77C3E5'
}

########################## Container: I/O
body_IO = dbc.Container([
				
    #Power button
    daq.PowerButton(
        id='Z_STEPPER_engage',
        on=False,
        className='dark-theme-control',
        size=40
    ),	
	dbc.Row([
        dbc.Col([
                html.P("Stepper (z-pos):"),
            ], className="col-7", style={"padding-left":10}),

        dbc.Col([
                dcc.Input(
                    id='z_stepper_serial',
                    size="7",
                    value=df_params.loc[1,'z_stepper_serial'],  
                    placeholder=df_params.loc[1,'z_stepper_serial'],   
                    style={'background-color':'#23262A','color':'#95999F'},
                ),
            ], className="col-3"),

        dbc.Col([
            daq.Indicator(
              id='z_stepper_engaged',
              value=False,
              style={"padding-left":10,"padding-top":5}
            ),
            ], className="col-2"),

    ],no_gutters=True,style={"margin-top":40}),

    dbc.Row([

        dbc.Col([
                html.P("Stepper (f_pos):"),
            ], className="col-7", style={"padding-left":10}),

        dbc.Col([
                dcc.Input(
                    id='f_stepper_serial',
                    size="7",
                    value=df_params.loc[1,'f_stepper_serial'],  
                    placeholder=df_params.loc[1,'f_stepper_serial'],  
                    style={'background-color':'#23262A','color':'#95999F'}
                ),
            ], className="col-3"),

        dbc.Col([
            daq.Indicator(
              id='f_stepper_engaged',
              value=False,
              style={"padding-left":10,"padding-top":5}
            ),
        ], className="col-2"),
    ],no_gutters=True,style={"padding-bottom":5}),

    dbc.Row([


        dbc.Col([
                html.P("interfaceKit:"),
            ], className="col-7", style={"padding-left":10}),

        dbc.Col([
            
                dcc.Input(
                    id='interfaceKit_serial',
                    size="7",
                    value=df_params.loc[1,'interfaceKit_serial'],  
                    placeholder=df_params.loc[1,'interfaceKit_serial'],    
                    style={'background-color':'#23262A','color':'#95999F'},
                ),
            ], className="col-3"),	

        dbc.Col([
            daq.Indicator(
              id='interfaceKit_engaged',
              value=False,
              style={"padding-left":10,"padding-top":5}
            ),
            ], className="col-2"),

            # Hidden div inside the app that stores the intermediate value
            html.Div(id='zpos_var', style={'display': 'none'}, children=([0])),
            html.Div(id='fpos_var', style={'display': 'none'}, children=([0])),

            html.Div(id='ledBRIGHT_isOn', style={'display': 'none'}, children=[0]),
            html.Div(id='ledDARK_isOn', style={'display': 'none'}, children=[0]),
            html.Div(id='ledGFP_isOn', style={'display': 'none'}, children=[0]),
            html.Div(id='ledCFP_isOn', style={'display': 'none'}, children=[0]),
            html.Div(id='ledRFP_isOn', style={'display': 'none'}, children=[0]),
            html.Div(id='ledYFP_isOn', style={'display': 'none'}, children=[0]),
        
            dcc.Interval(id="listener", interval=500, n_intervals=0),
            dcc.Interval(id="timelapse_t", interval=1000, n_intervals=0),

                    

			],no_gutters=True,style={"margin-bottom":20}),
	],style={"background-color":"#13161D","padding":10,"margin":0}, fluid=True),



########################## Container: STAGE

body_stage = dbc.Container([
	dbc.Row([
		dbc.Col([
			
			daq.Gauge(
				  id='fpos_gauge',
				  label='Filter Wheel',
				  labelPosition='top',
				  value=(df_params.loc[1,'fpos_max']-df_params.loc[1,'fpos_min'])/2,
				  max=df_params.loc[1,'fpos_max'],
				  min=df_params.loc[1,'fpos_min'],
				  size=150
				),
											
		], width=3, style={"margin-left":30}),
		
		dbc.Col([
					html.Div(
						style={'width': '100%', 'display': 'inline-block','padding-left':20,'padding-right':20, 'padding-bottom':0,'padding-top':40},
						children=[
				    		html.Div(
									style={'width': '33%', 'padding':0,'float':'left'},
									children=[
								    	html.Button(id='btn-home', className='fa fa-home', style={"color":"#95999F"}),
				            ]),
							html.Div(
									style={'width': '33%', 'padding':0,'float':'left'},
									children=[
								    	html.Button(id='btn-up', className='fa fa-arrow-up', style={"color":"#95999F"}),
				            ]),
						]),
				    	
				    	html.Div(
							style={'width': '100%','padding-left':20,'padding-right':20,'float':'left'},
							children=[
								html.Div(style={'width': '33%', 'padding':0,'float':'left'}, 
								children=[
									html.Button(id='btn-minus', className='fa fa-arrow-left', style={"color":"#95999F"}),
								]),
								html.Div(
									style={'width': '33%', 'padding':0,'float':'left','color':'#000'},
									children=[
				                        html.Button(id='btn-click', className='fa fa-camera', style={"color":"#95999F"}),
                                    ]),
								
								html.Div(style={'width': '33%', 'padding':0,'float':'left','margin-left':2}, 
								children=[
									html.Button(id='btn-plus', className='fa fa-arrow-right', style={"color":"#95999F"}),
								]),
						]),
						
						html.Div(style={'width': '100%', 'display': 'inline-block','padding-left':20,'padding-right':20},
						children=[
							html.Div(style={'width': '33%', 'padding-top':10,'padding-left':10,'float':'left'},
									children=[
                                        daq.Slider(
                                            id='deltaJog_slider',
                                            marks={i: '{}'.format(10 ** i) for i in range(0,3)},
                                            size=50,
                                            min=0,
                                            max=2,
                                            value=1,
                                            step=0.0005,
                                            updatemode='drag'
                                        ),
                                        
									]),
						
				    		html.Div(style={'width': '33%', 'padding':0,'float':'left','margin-top':8},
									children=[
								    	html.Button(id='btn-down', className='fa fa-arrow-down', style={"color":"#95999F"}),
									]),
						]),
		
		], width=5),
		
		dbc.Col([
				daq.Tank(
					id='zpos_tank',
					className='dark-theme-components',
					value=50,
					height=150,
					min=0,
					max=100,
					label='Vertical Axis',
					labelPosition='top'
				),
		], width=3),
	],style={"background-color":"#13161D","padding":10,"padding-bottom":25},no_gutters=True),
],fluid=True,
)

#################### Container: CONTROL
header_control=dbc.Container([
	dbc.Row([
		dbc.Col(["Control"
		], 
		style={"margin-bottom":20,"padding":5})
	]),
],
)
body_control = dbc.Container([

	dbc.Row([
		dbc.Col([
			html.P("LED"),

		],width={"size": 2, "offset": 0}, style={"padding-left":20}),
		
		dbc.Col([
			html.P("Filter"),		
		], className="col-3",style={"padding-left":20}),
		
		dbc.Col([
			html.P("Exposure",style={"padding-left":0}),
		], className="col-4"),
		
		dbc.Col([
			html.P("Set",style={"padding-left":0,"margin-left":10}),
		], className="col-1"),
	]),
    dbc.Row([
		dbc.Col([
			daq.BooleanSwitch(
			  id='ledBRIGHT_switch',
			  on=False
			)
		], width={"size": 2, "offset": 0} ,style={"padding-top":5,"margin-left":0}),
		
		dbc.Col([
			html.Button(id='btn-filterBRIGHT', children='BRIGHT',style={"color":"white","width":100,"margin-right":0}),
		], className="col-3"),
		
		dbc.Col([
			daq.Slider(
				id='filterBRIGHT_slider',
				#marks={i: '{}'.format(10 ** i) for i in range(-2,2)},
				size=100,
				min=-2,
		       max=1,
		       value=0.01,
		       step=0.005,
		       updatemode='drag'
			),
		], className="col-3",style={"padding-top":10}),
		dbc.Col([
			html.Div(id='exposureBRIGHT',style={"padding-top":5})
		], className="col-1"),
		dbc.Col([
			
			html.Button(id='btn-set-BRIGHT', className='fa fa-angle-double-left', 
				style={"width":20,"padding":0, "margin-right":0, "height":20,"margin-top":3,"color":"#95999F"}),
			
		], className="col-2",style={"padding-top":5,"margin-left":10}),	
	]),
	dbc.Row([
		dbc.Col([
			daq.BooleanSwitch(
			  id='ledDARK_switch',
			  on=False
			)
		], width={"size": 2, "offset": 0} ,style={"padding-top":5,"margin-left":0}),
		
		dbc.Col([
			html.Button(id='btn-filterDARK', children='DARK',style={"color":"DARK","width":100,"margin-right":0}),
		], className="col-3"),
		
		dbc.Col([
			daq.Slider(
				id='filterDARK_slider',
				#marks={i: '{}'.format(10 ** i) for i in range(-2,2)},
				size=100,
				min=-2,
		       max=1,
		       value=0.01,
		       step=0.005,
		       updatemode='drag'
			),
		], className="col-3",style={"padding-top":10}),
		dbc.Col([
			html.Div(id='exposureDARK',style={"padding-top":5})
		], className="col-1"),
		dbc.Col([
			
			html.Button(id='btn-set-DARK', className='fa fa-angle-double-left', 
				style={"width":20,"padding":0, "margin-right":0, "height":20,"margin-top":3,"color":"#95999F"}),
			
		], className="col-2",style={"padding-top":5,"margin-left":10}),	
	]),
	dbc.Row([
		dbc.Col([
			daq.BooleanSwitch(
			  id='ledGFP_switch',
			  on=False
			)
		], className="col-2",style={"padding-top":5}),
		
		dbc.Col([
			  	html.Button(id='btn-filterGFP', children='GFP',style={"color":"#C2E8B8","width":100}),
		], className="col-3"),
		
		dbc.Col([
			daq.Slider(
				id='filterGFP_slider',
				#marks={i: '{}'.format(10 ** i) for i in range(-2,2)},
				size=100,
				min=-2,
		       max=1,
		       value=.01,
		       step=0.005,
		       updatemode='drag',
			),
		], className="col-3",style={"padding-top":10}),
		
		dbc.Col([
			html.Div(id='exposureGFP')
		], className="col-1",style={"padding-top":5}),
		
		dbc.Col([
			
			html.Button(id='btn-set-GFP', className='fa fa-angle-double-left', 
				style={"width":20,"padding":0, "margin":0, "height":20,"margin-top":3,"color":"#95999F"}),
			
		], className="col-1",style={"padding-top":5,"margin-left":10}),	
	]),
	
	dbc.Row([
		dbc.Col([
			daq.BooleanSwitch(
			  id='ledRFP_switch',
			  on=False
			)
		], className="col-2",style={"padding-top":5}),
		
		dbc.Col([
			html.Button(id='btn-filterRFP', children='RFP',style={"color":"#F8A39D","width":100}),
		], className="col-3"),
		
		dbc.Col([
			daq.Slider(
				id='filterRFP_slider',
				#marks={i: '{}'.format(10 ** i) for i in range(-2,2)},
				size=100,
				min=-2,
		        max=1,
		        value=0.01,
		        step=0.005,
		        updatemode='drag'
			),
		], className="col-3",style={"padding-top":10}),
		dbc.Col([
			html.Div(id='exposureRFP'),
			
			
		], className="col-1",style={"padding-top":5}),	
		
		dbc.Col([
			
			html.Button(id='btn-set-RFP', className='fa fa-angle-double-left', 
				style={"width":20,"padding":0, "margin":0, "height":20,"margin-top":3,"color":"#95999F"}),
			
		], className="col-1",style={"padding-top":5,"margin-left":10}),	
	]),
	
	dbc.Row([
		dbc.Col([
			daq.BooleanSwitch(
			  id='ledCFP_switch',
			  on=False
			)
		], className="col-2",style={"padding-top":5}),
		
		dbc.Col([
			html.Button(id='btn-filterCFP', children='CFP',style={"color":"#A5C1DB","width":100}),
		], className="col-3"),
		
		dbc.Col([
			daq.Slider(
				id='filterCFP_slider',
				#marks={i: '{}'.format(10 ** i) for i in range(-2,2)},
				size=100,
				min=-2,
		       max=1,
		       value=0.01,
		       step=0.005,
		       updatemode='drag'
			),
		], className="col-3",style={"padding-top":10}),
		
		dbc.Col([
			html.Div(id='exposureCFP')
		], className="col-1",style={"padding-top":5}),
		dbc.Col([
			
			html.Button(id='btn-set-CFP', className='fa fa-angle-double-left', 
				style={"width":20,"padding":0, "margin":0, "height":20,"margin-top":3,"color":"#95999F"}),
			
		], className="col-1",style={"padding-top":5,"margin-left":10}),	
	]),
	
	dbc.Row([
		dbc.Col([
			daq.BooleanSwitch(
			  id='ledYFP_switch',
			  on=False
			)
		], width={"size": 2, "offset": 0},style={"padding-top":5}),
		
		dbc.Col([
			html.Button(id='btn-filterYFP', children='YFP',style={"color":"#FFFFA4","width":100}),
		], className="col-3", style={"float":"center"}),
		
		dbc.Col([
			daq.Slider(
				id='filterYFP_slider',
				#marks={i: '{}'.format(10 ** i) for i in range(-2,2)},
				size=100,
				min=-2,
		       max=1,
		       value=0.01,
		       step=0.005,
		       updatemode='drag'
			),
		], className="col-3",style={"padding-top":10}),
		dbc.Col([
			html.Div(id='exposureYFP')
		], className="col-1",style={"padding-top":5}),
		dbc.Col([
			
			html.Button(id='btn-set-YFP', className='fa fa-angle-double-left', 
				style={"width":20,"padding":0, "margin":0, "height":20,"margin-top":3,"color":"#95999F"}),
			
		], className="col-1",style={"padding-top":5,"margin-left":10}),	
	]),
],style={"background-color":"#13161D","padding":10,"margin-top":0,"padding-left":30}, fluid=True)

#################### CONTROL
body_timelapse = dbc.Container([

     dbc.Row([
			
        
        dbc.Col([
            
            html.Div([
                dcc.Interval(
                    id='interval_thermostat',
                    interval=5*1000, # in milliseconds
                    n_intervals=0
                )
            ]),
            
            dbc.Row([
                dbc.Col([		
                  daq.LEDDisplay(
                        id='current_temperature',
                        value="37.5"
                    ),

			
                 
				], className="col-8"),
                
                dbc.Col([	
                    html.Div([
                        
                        html.P("Heating "),
                        daq.Indicator(
                          id='incubator_on',
                          color="#00cc96",
                          value=False
                        ),

                        
                        daq.Slider(
                            id='target_temperature',
                            min=21, max=42, value=30,
                            handleLabel={"showCurrentValue": True,"label": "target"},
                            step=1,
                            marks={'30': '30C', '37': '37C'}
                        ),

                    ]),
                    
				], className="col-4"),
				
			]),
			

             
            
        ], className="col-6"),
        
         
         dbc.Col([
    
                html.P("Time before next cycle:", style={"padding-top":30}),
					daq.LEDDisplay(
					id='timer_display',
					value="88:88"
				),
        ], className="col-9"),
    
    
			]),

	dbc.Row([
		dbc.Col([		
			dbc.Row([
			
				dbc.Col([
					dcc.Checklist(
						id='incubator_checkbox',
					    options=[
					        {'label': ' Incubate', 'value': 'heatON'},
					    ],
					    style={"padding-left":15,"font-size":12,"display":"none"},
					    value=[]
					)
				], className="col-12"),
				
			]),
            dbc.Row([
			
				dbc.Col([
					dcc.Checklist(
						id='defrost_checkbox',
					    options=[
					        {'label': ' Defrost', 'value': 'defrostON'},
					    ],
					    style={"padding-left":15,"font-size":12,"display":"none"},
					    value=[]
					)
				], className="col-12"),
				
			]),
			
			
		], width={"size": 6, "offset": 0}),
		
		
		
		
	],style={"margin-bottom":0,"margin-top":10}),
	
],style={"background-color":"#13161D","padding":10,"margin-top":0}, fluid=True
)


body_buttons = dbc.Container([
   
    
    dbc.Row([
			
				dbc.Col([
					html.P("Interval (seconds):", style={"padding-left":15,"text-align":"right"}),
				], className="col-9"),
				
				dbc.Col([
                    dcc.Input(
								id='cycles_input',
								size="6",
                                value=1000,
                                style={'display': 'none'},
							),
                    
					dcc.Input(
						id='interval_input',
						size="6",
                        value='600',
				  		style={'background-color':'#23262A','color':'#95999F',"text-align":"right",'margin-right':'20px'}
					),
				], className="col-3"),
				
			]),

    
	dbc.Row([
			dbc.Col([
                
                #TABLE
                html.Div([

                    dash_table.DataTable(
                        id='tbl_opt_config',
                        columns=[{
                            'name': 'Optical Configurations',
                            'id': 'opt_config-{}'.format(i),
                            'deletable': True,
                            'renamable': True
                        } for i in range(1, 2)],
                        data=[
                        ],
                        style_as_list_view=True,
                        style_cell={
                            'padding': '5px',
                            'backgroundColor': '#13161D', 
                            'font-size':12,
                        },
                        style_header={
                            'backgroundColor': '#13161D',
                        },
                        editable=False,
                        row_deletable=True
                    ),

                    

                ]),
                
                html.Button('Add', id='add_config-button',style={"width":100}, n_clicks=0),
				html.Button(id='btn-runOne', children='Run 1',style={"width":100}),
				html.Button(id='btn-runtimelapse', children='Loop',style={"width":100}),
				html.Button(id='btn-stop', children='Stop',style={"width":100}),
				
				html.P("Progress:",style={"margin-top":10}),
					
				daq.GraduatedBar(
					id='ncycles_progressbar',
					value=4
				),
                html.Div(
				    id='runtimelapse_output',
					style={"padding":0,"margin":0,"font-size":10},
                ),
                
							
			
			], 
			style={"margin-bottom":20,"padding":15,"margin-top":0}, className="col-12")
		],no_gutters=True),


],style={"background-color":"#13161D","padding":10,"margin-top":0}, fluid=True,)



body_rgb = dbc.Container([
    
	dbc.Row([
          
            dbc.Col([
                
                
			], 
			style={"margin-top":20,"padding":0,"text-align":"left"}, className="col-2"),
            
        
			dbc.Col([
                
                dcc.RadioItems(
                    id='LEDsegment',
                    options=[
                        {'label': 'ALL', 'value': 'all'},
                        {'label': 'LED1', 'value': '1  '},
                        {'label': 'LED2', 'value': '2'},
                        {'label': 'LED3', 'value': '3'},
                        {'label': 'LED4', 'value': '4'},
                        {'label': 'LED5', 'value': '5'},
                        {'label': 'LED6', 'value': '6'},
                        {'label': 'LED7', 'value': '7'},
                        {'label': 'LED8', 'value': '8'}
                    ],
                    value='all',
                    style={'color':'#95999F', 'font-size':14},
                ), 
                
               
                
			], 
			style={"margin-top":20,"padding":0,"text-align":"left"}, className="col-2"),
            
            dbc.Col([
                daq.ColorPicker(
                    id='LEDcolor',
                    label='LED Color',
                    size=164,
                    value=dict(rgb=dict(r=255, g=255, b=255, a=1))
                )
            ], 
			style={"margin-bottom":0,"padding":0,"margin-top":0,"text-align":"center"}, className="col-8"),
		],no_gutters=True),
    


],style={"background-color":"#13161D","padding":10,"margin-top":-15,"margin-left":15}, fluid=True,)

body_hidden = dbc.Container([

	dbc.Row([
			dbc.Col([
				#html.P("Input:"),
				
				dbc.Row([
					dbc.Col([
						html.P("stepper (filter-pos)",style={"padding":0,"margin":0,"margin-top":4,"font-size":10,"display": "none"}),
					], width={"size": 7,"offset":0}),
					dbc.Col([
						html.Div(
							id='f_stepper_input',
                            children=['0'],
							style={'color':'#95999F', 'font-size':10,"display": "none"},
						),
					], width={"size": 3}),
					
				],style={"padding":0,"margin-top":0}),
			
				dbc.Row([
					dbc.Col([
						html.P("stepper (z-pos) ",style={"padding":0,"margin":0,"margin-top":4,"font-size":10,"display": "none"}),
					], width={"size": 7,"offset":0}),
					dbc.Col([
						html.Div(
							id='z_stepper_input',
                            children=['0'],
							style={'color':'#95999F', 'font-size':10,"display": "none"},
						),	
					], width={"size": 3}),
					
				],style={"padding":0,"margin-top":0}),
				
                
                
				dbc.Row([
					dbc.Col([
						html.P("Timer ",style={"padding":0,"margin":0,"margin-top":4,"font-size":10,"display": "none"}),
					], width={"size": 6,"offset":0}),
					dbc.Col([
						html.Div(
							id='timer_input',
						    children=[None],
							style={'color':'#95999F', 'font-size':10,"display": "none"},
						),	
					], width={"size": 3}),
					
				],style={"padding":0,"margin-top":0}),	
                
				dbc.Row([
					dbc.Col([
						html.P("Cycles ",style={"padding":0,"margin":0,"margin-top":4,"font-size":10,"display": "none"}),
					], width={"size": 6,"offset":0}),
					dbc.Col([
						html.Div(
							id='ncycles_input',
						    children=[None],
							style={'color':'#95999F', 'font-size':10,"display": "none"},
						),	
					], width={"size": 3}),
					
				],style={"padding":0,"margin-top":0}),	
                
                dbc.Row([
					dbc.Col([
						html.P("timelapse start ",style={"padding":0,"margin":0,"margin-top":4,"font-size":10,"display": "none"}),
					], width={"size": 6,"offset":0}),
					dbc.Col([
						html.Div(
							id='timelapse_start',
						    children=[-1],
							style={'color':'#95999F', 'font-size':10,"display": "none"},
						),	
					], width={"size": 3}),
					
				],style={"padding":0,"margin-top":0}),
                
                dbc.Row([
					dbc.Col([
						html.P("timelapse end ",style={"padding":0,"margin":0,"margin-top":4,"font-size":10,"display": "none"}),
					], width={"size": 6,"offset":0}),
					dbc.Col([
						html.Div(
							id='timelapse_end',
						    children=[-1],
							style={'color':'#95999F', 'font-size':10,'display': 'none'},
						),	
					], width={"size": 3}),
				],style={"padding":0,"margin-top":0}),

                dbc.Row([
					dbc.Col([
						html.P("timelapse stop ",style={"padding":0,"margin":0,"margin-top":4,"font-size":10,"display": "none"}),
					], width={"size": 6,"offset":0}),
					dbc.Col([
						html.Div(
							id='timelapse_stop',
						    children=[False],
							style={'color':'#95999F', 'font-size':10,'display': 'none'},
						),	
					], width={"size": 3}),
				],style={"padding":0,"margin-top":0}),
                    
                                
                dbc.Row([
					dbc.Col([
						html.P("timelapse click",style={"padding":0,"margin":0,"margin-top":4,"font-size":10,"display": "none"}),
					], width={"size": 6,"offset":0}),
					dbc.Col([
						html.Div(
							id='timelapse_click',
						    children=[False],
							style={'color':'#95999F', 'font-size':10,'display': 'none'},
						),	
					], width={"size": 3}),
				],style={"padding":0,"margin-top":0}),
				
				dbc.Row([
					dbc.Col([
						html.P("",style={"padding":0,"margin":0,"margin-top":2,"font-size":10,"display": "none"}),
					], width={"size": 5,"offset":1}),
					dbc.Col([
						html.Div(
							id='runOne_output',
							style={"padding":0,"margin":0,"font-size":10,"display": "none"},
							children=60,
						),
					], width={"size": 6}),
				],style={"padding":0,"margin-top":0}),
			
				
				
				
			], width={"size": 6, "offset": 0}),
			dbc.Col([	
				
				html.P("Presets:"),
				
                
				dbc.Row([
					dbc.Col([
						html.P("BRIGHT: ",style={"padding":0,"margin":0,"margin-top":2,"font-size":10,"display": "none"}),
					], width={"size": 5,"offset":1}),
					dbc.Col([
						html.Div(
							id='fpos_BRIGHT',
							style={"padding":0,"margin":0,"font-size":10,"display": "none"},
							children=60,
						),
					], width={"size": 6}),
				],style={"padding":0,"margin-top":0}),
                
				dbc.Row([
					dbc.Col([
						html.P("DARK: ",style={"padding":0,"margin":0,"margin-top":2,"font-size":10,"display": "none"}),
					], width={"size": 5,"offset":1}),
					dbc.Col([
						html.Div(
							id='fpos_DARK',
							style={"padding":0,"margin":0,"font-size":10,"display": "none"},
							children=60,
						),
					], width={"size": 6}),
				],style={"padding":0,"margin-top":0}),
				
				
				dbc.Row([
					dbc.Col([
						html.P("GFP: ",style={"padding":0,"margin":0,"margin-top":2,"font-size":10,"display": "none"}),
					], width={"size": 5,"offset":1}),
					dbc.Col([
						html.Div(
							id='fpos_GFP',
							style={"padding":0,"margin":0,"font-size":10,"display": "none"},
							children=20,
						),
					], width={"size": 6}),
				],style={"padding":0,"margin-top":0}),



				dbc.Row([
					dbc.Col([
						html.P("RFP: ",style={"padding":0,"margin":0,"margin-top":2,"font-size":10,"display": "none"}),
					], width={"size": 5,"offset":1}),
					dbc.Col([
						html.Div(
							id='fpos_RFP',
							style={"padding":0,"margin":0,"font-size":10,"display": "none"},
							children=40,
						),	
					], width={"size": 6}),
				],style={"padding":0,"margin-top":0}),


				dbc.Row([
					dbc.Col([
						html.P("CFP: ",style={"padding":0,"margin":0,"margin-top":2,"font-size":10,"display": "none"}),
					], width={"size": 5,"offset":1}),
					dbc.Col([
						html.Div(
							id='fpos_CFP',
							style={"padding":0,"margin":0,"font-size":10,"display": "none"},
							children=80,
						),
					], width={"size": 6}),
				],style={"padding":0,"margin-top":0}),


				dbc.Row([
					dbc.Col([
						html.P("YFP: ",style={"padding":0,"margin":0,"margin-top":2,"font-size":10,"display": "none"}),
					], width={"size": 5,"offset":1}),
					dbc.Col([
						html.Div(
							id='fpos_YFP',
							style={"padding":0,"margin":0,"font-size":10,"display": "none"},
							children=100,
						),
					], width={"size": 6}),
				],style={"padding":0,"margin-top":0}),
                
                dbc.Row([
					dbc.Col([
						html.P("color ",style={"padding":0,"margin":0,"margin-top":2,"font-size":10,"display": "none"}),
					], width={"size": 5,"offset":1}),
					dbc.Col([
						html.Div(
							id='LEDsegments_color',
							style={"padding":0,"margin":0,"font-size":10,"display": "none"},
							children='(255,255,255,128)',
						),
					], width={"size": 6}),
				],style={"padding":0,"margin-top":0}),
                            
			
			], style={"margin-bottom":20,"padding":5,"margin-top":0,"display": "none"}, width={"size": 4, "offset": 1})
        
        
        
        
		],no_gutters=True),
])
										
										
#############

body_layout = dbc.Container([

	dbc.Row([
		dbc.Col([
		 	html.Div(body_IO, style={"padding-left":30})
		],className="col-3",style={"padding":0}),
		dbc.Col([
		 	html.Div(body_stage)
		],className="col-9",style={"padding":0}),
	]),
	
	dbc.Row([
		dbc.Col([
		 	html.Div(body_control)
		],className="col-6",style={"padding-top":15,"margin-right":-15,"margin-left":15}),
		dbc.Col([
		 	html.Div(body_buttons)
		],className="col-6",style={"padding-top":15}),
	]),
	dbc.Row([
		dbc.Col([
		 	html.Div(body_rgb)
		],className="col-6",style={"padding-top":15}),
		dbc.Col([
		 	html.Div(body_timelapse)
		],className="col-6",style={"padding":15}),
	]),
	dbc.Row([
		dbc.Col([
		],className="col-6",style={"padding-top":15}),
		dbc.Col([
		 	html.Div(body_hidden)
		],className="col-6",style={"padding":15}),
	]),
	
])
	
	
#Dark mode
app.layout = html.Div(id='dark-theme-components', children=[
	daq.DarkThemeProvider(theme=theme, children=body_layout)
	])	
	
#app.layout = html.Div(body_layout)


############# INCUBATOR (THERMOSTAT)

@app.callback(Output('current_temperature', 'value'),
         [Input('interval_thermostat', 'n_intervals')])
        
def update_current(n):
    serial_data = str(arduino.readline(), "utf-8").split('/')
    serial_temperature=float(serial_data[0])
    serial_humidity=float(serial_data[1]) 
    print("%0.2fC / %0.2f%s  "%((serial_temperature), (serial_humidity), chr(37)))
    return serial_temperature

@app.callback(Output('incubator_on', 'value'),
         [Input('interval_thermostat', 'n_intervals')], [State('current_temperature', 'value'),  State('target_temperature', 'value'), State('interfaceKit_engaged','value')])
        
def update_incubator(n, current_temperature, target_temperature, interfaceKit_engaged):
    
    if interfaceKit_engaged:
        outputHEAT=df_params.loc[1,'output_incubator']
        #print(" %s : %s"%(current_temperature, target_temperature))
        if float(target_temperature)>float(current_temperature): #Turn on
            HEAT_turnON(interfaceKit_output, outputHEAT)
            return True

        HEAT_turnOFF(interfaceKit_output, outputHEAT)
        
    return False
    

############# TABLE OPTICAL CONFIGURATIONS
@app.callback(
    Output('tbl_opt_config', 'data'),
    [Input('add_config-button', 'n_clicks')],
    [State('tbl_opt_config', 'data'),
     State('tbl_opt_config', 'columns'), State('ledBRIGHT_switch', 'on'), State('ledDARK_switch', 'on'), State('ledGFP_switch', 'on'), State('ledRFP_switch', 'on'), State('ledCFP_switch', 'on'), State('ledYFP_switch', 'on'), State('filterBRIGHT_slider', 'value'), State('filterDARK_slider', 'value'), State('filterGFP_slider', 'value'), State('filterRFP_slider', 'value'), State('filterCFP_slider', 'value'), State('filterYFP_slider', 'value'), State('LEDcolor','value')])
def add_row(n_clicks, rows, columns, ledBRIGHT, ledDARK, ledGFP, ledRFP, ledCFP, ledYFP, exposureBRIGHT, exposureDARK, exposureGFP, exposureRFP, exposureCFP, exposureYFP, colorLED):
    if n_clicks > 0:
        str_opt_config=''
        if ledBRIGHT:
            str_opt_config+='BRIGHT (%gs)'%transform_value(exposureBRIGHT)
            
        if ledDARK:
            if str_opt_config!='':
                str_opt_config+=" / "
            strLED=' #%02x%02x%02x, a=%g' % (colorLED['rgb']['r'], colorLED['rgb']['g'], colorLED['rgb']['b'],colorLED['rgb']['a'])
            str_opt_config+='DARK (%gs,%s)'%(transform_value(exposureDARK),strLED)
            
        if ledGFP:
            if str_opt_config!='':
                str_opt_config+=" / "
            str_opt_config+='GFP (%gs)'%transform_value(exposureGFP)
        if ledRFP:
            if str_opt_config!='':
                str_opt_config+=" / "
            str_opt_config+='RFP (%gs)'%transform_value(exposureRFP)
        if ledCFP:
            if str_opt_config!='':
                str_opt_config+=" / "
            str_opt_config+='CFP (%gs)'%transform_value(exposureCFP)
        if ledYFP:
            if str_opt_config!='':
                str_opt_config+=" / "
            str_opt_config+='YFP (%gs)'%transform_value(exposureYFP)
        
        if str_opt_config!="":
            rows.append({c['id']: str_opt_config for c in columns})
            
        #else:
        #    rows.append({c['id']: 'N/A' for c in columns})
            
    return rows


#############  SWITCH LEDS ON/OFF
@app.callback(Output('ledDARK_isOn', 'children'),
              [Input('ledDARK_switch', 'on')], [State('interfaceKit_engaged','value'),State('LEDcolor','value'),State('LEDsegments_color','children')])
def toggle_switch(isOn, engaged, colorLED, LEDsegment_str):
    if engaged:
        
        strLED='DARK'
        outputLED=df_params.loc[1,'output_filterDARK']
        port=df_params.loc[1,'output_portDARK']
        ip=df_params.loc[1,'output_ipDARK']
        
        if isOn:
            isOn=LED_turnON(interfaceKit_output, strLED, colorLED, outputLED)
        
            #Here we communicate with protopixel
            for i in range(1,9):
                cmd_enable='/Program/segment%s/enabled/'%i
                client.send_message(cmd_enable, [1])
                
            #isOn=True
        else:
            isOn=LED_turnOFF(interfaceKit_output, strLED, colorLED, outputLED)
            for i in range(1,9):
                cmd_disable='/Program/segment%s/enabled/'%i
                client.send_message(cmd_disable, [0])
                
            isOn=False
    return isOn
    
    finished = False
    while not finished:
        osc_process()
    osc_terminate()
    
    


@app.callback(Output('LEDsegments_color', 'children'),
              [Input('LEDcolor', 'value')], [State('LEDsegment','value')])

def setValue(thisLEDcolor, thisLEDsegment):
    
    val_colorR=int(thisLEDcolor['rgb']['r'])
    val_colorG=int(thisLEDcolor['rgb']['b'])
    val_colorB=int(thisLEDcolor['rgb']['g'])
    val_colorA=int(255*float(thisLEDcolor['rgb']['a']))
    
    
    #Here we communicate with protopixel
    #print('\nUpdating color of segments: %s'%thisLEDsegment)
    for i in range(1,9):
        if thisLEDsegment == 'all' or (thisLEDsegment==str(i)):

            cmd_color='/Program/segment%s/params/color'%i
            val_color=[val_colorR,val_colorG,val_colorB,val_colorA]
            client.send_message(cmd_color, val_color)
    
    ret='(%s,%s,%s,%s)'%(val_colorR,val_colorG,val_colorB, val_colorA)
    
    return ret
    
    
@app.callback(Output('ledBRIGHT_isOn', 'children'),
              [Input('ledBRIGHT_switch', 'on')], [State('interfaceKit_engaged','value')])

def toggle_switch(isOn, engaged):
    if engaged:
        strLED='BRIGHT'
        outputLED=df_params.loc[1,'output_filterBRIGHT']
        if isOn:
            isOn=LED_turnON(interfaceKit_output, strLED, 'BRIGHT', outputLED)
        else:
            isOn=LED_turnOFF(interfaceKit_output, strLED, 'BRIGHT', outputLED)
    return isOn  
    
@app.callback(Output('ledGFP_isOn', 'children'),
              [Input('ledGFP_switch', 'on')], [State('interfaceKit_engaged','value')])

def toggle_switch(isOn, engaged):
    if engaged:
        strLED='GFP'
        outputLED=df_params.loc[1,'output_filterGFP']
        if isOn:
            isOn=LED_turnON(interfaceKit_output, strLED, 'GFP', outputLED)
        else:
            isOn=LED_turnOFF(interfaceKit_output, strLED, 'GFP', outputLED)
    return isOn
	
@app.callback(Output('ledCFP_isOn', 'children'),
              [Input('ledCFP_switch', 'on')], [State('interfaceKit_engaged','value')])
def toggle_switch(isOn, engaged):
    if engaged:
        strLED='CFP'
        outputLED=df_params.loc[1,'output_filterCFP']
        if isOn:
            isOn=LED_turnON(interfaceKit_output, strLED, 'CFP', outputLED)
        else:
            isOn=LED_turnOFF(interfaceKit_output, strLED, 'CFP', outputLED)
    return isOn
@app.callback(Output('ledRFP_isOn', 'children'),
              [Input('ledRFP_switch', 'on')], [State('interfaceKit_engaged','value')])
def toggle_switch(isOn, engaged):
    if engaged:
        strLED='RFP'
        outputLED=df_params.loc[1,'output_filterRFP']
        if isOn:
            isOn=LED_turnON(interfaceKit_output, strLED, 'RFP', outputLED)
        else:
            isOn=LED_turnOFF(interfaceKit_output, strLED, 'RFP', outputLED)
    return isOn
	
@app.callback(Output('ledYFP_isOn', 'children'),
              [Input('ledYFP_switch', 'on')], [State('interfaceKit_engaged','value')])
def toggle_switch(isOn, engaged):
    if engaged:
        strLED='YFP'
        outputLED=df_params.loc[1,'output_filterYFP']
        if isOn:
            isOn=LED_turnON(interfaceKit_output, strLED, 'YFP', outputLED)
        else:
            isOn=LED_turnOFF(interfaceKit_output, strLED, 'YFP', outputLED)
    return isOn

#############
def transform_value(value):
	val=10 ** value
	if val>=1.0:
		ret=round(val*10)/10
	else:
		ret=round(val*100)/100
	return ret

@app.callback(Output('exposureBRIGHT', 'children'),
              [Input('filterBRIGHT_slider', 'value')])
def display_value(value):
    val=transform_value(value)
    if val>=1.0:
    	ret='{:0.1f}s'.format(val)
    else:
    	ret='{:0.2f}s'.format(val)
    return ret
    
@app.callback(Output('exposureDARK', 'children'),
              [Input('filterDARK_slider', 'value')])
def display_value(value):
	val=transform_value(value)
	if val>=1.0:
		ret='{:0.1f}s'.format(val)
	else:
		ret='{:0.2f}s'.format(val)
	return ret

@app.callback(Output('exposureGFP', 'children'),
              [Input('filterGFP_slider', 'value')])
def display_value(value):
    val=transform_value(value)
    if val>=1.0:
    	ret='{:0.1f}s'.format(val)
    else:
    	ret='{:0.2f}s'.format(val)
    return ret
    
@app.callback(Output('exposureCFP', 'children'),
              [Input('filterCFP_slider', 'value')])
def display_value(value):
    val=transform_value(value)
    if val>=1.0:
    	ret='{:0.1f}s'.format(val)
    else:
    	ret='{:0.2f}s'.format(val)
    return ret
    
@app.callback(Output('exposureYFP', 'children'),
              [Input('filterYFP_slider', 'value')])
def display_value(value):
    val=transform_value(value)
    if val>=1.0:
    	ret='{:0.1f}s'.format(val)
    else:
    	ret='{:0.2f}s'.format(val)
    return ret
    
@app.callback(Output('exposureRFP', 'children'),
              [Input('filterRFP_slider', 'value')])
def display_value(value):
    val=transform_value(value)
    if val>=1.0:
    	ret='{:0.1f}s'.format(val)
    else:
    	ret='{:0.2f}s'.format(val)
    return ret
    
#############
@app.callback([Output('z_stepper_engaged','value'),Output('f_stepper_engaged','value'),Output('interfaceKit_engaged','value')], [Input('Z_STEPPER_engage', 'on')], [State('f_stepper_serial','value'), State('z_stepper_serial','value'), State('interfaceKit_serial','value')])
def engage(isOn, f_stepper_serial, z_stepper_serial, interfaceKit_serial): 
    ret_baffle=False
    ret_filter=False
    ret_interfaceKit=False
    if isOn==True:
        
        
        ret_baffle=Z_STEPPER_engage(int(z_stepper_serial))
        #sleep(1)
        
        ret_filter=F_STEPPER_engage(int(f_stepper_serial))
        #sleep(2)
        
        
        ret_interfaceKit=INTERFACEKIT_engage(int(interfaceKit_serial))
        #sleep(1)
        
        
        #if ret_filter:
        #    F_STEPPER_setHome()
            
        #if ret_baffle:
        #    Z_STEPPER_setHome()
        
    else:
        ret_baffle=Z_STEPPER_disengage() 
        ret_filter=F_STEPPER_disengage() 
        ret_interfaceKit=INTERFACEKIT_disengage() 
        

        f_stepper=Stepper() #??
        z_stepper=Stepper() #??
        
    
    print([ret_baffle, ret_filter, ret_interfaceKit])
    return [ret_baffle, ret_filter, ret_interfaceKit]

#############
@app.callback(Output('timer_display','value'), [Input('timer_input', 'children')])
def read_params(t_sec):
    t_str='88:88'
    if isinstance(t_sec, int):
        t_str=time.strftime('%M:%S', time.gmtime(t_sec))
    return t_str

#############
@app.callback(Output('zpos_tank','value'), [Input('zpos_var', 'children')])
def read_params(cached_data):
    cached_df = pd.read_json(cached_data)
    zpos=cached_df['zpos'][1]
    return zpos 
    
#############
@app.callback(Output('fpos_gauge','value'), [Input('fpos_var', 'children')])
def read_params(cached_data):
    fpos=0
    if with_f_stepper:
        cached_df = pd.read_json(cached_data)
        fpos=cached_df['fpos'][1]
        
    return fpos
    
    
############# 
@app.callback(Output('zpos_var', 'children'),
              [Input('btn-home', 'n_clicks'),
               Input('btn-up', 'n_clicks'),
               Input('btn-down', 'n_clicks'),
               Input('z_stepper_input', 'children')], [State('deltaJog_slider','value'), State("z_stepper_engaged", "value")])

def update(btn1, btn2, btn3, zpos_target, zpos_delta, engaged):
    
    if engaged and with_z_stepper:

        ctx = dash.callback_context

        min_zpos=df_params.loc[1,'zpos_min']
        max_zpos=df_params.loc[1,'zpos_max']
        current_zpos=df_params.loc[1,'zpos']
        next_zpos=current_zpos
            
        if not ctx.triggered:
            button_id = 'No clicks yet'
            next
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'btn-up':

            next_zpos=current_zpos+10*(10 ** (1+zpos_delta))
            print('jog up: next_zpos=',next_zpos)
            ##if next_zpos<min_zpos:
            #    next_zpos=min_zpos
            #    print('min_zpos!')

            Z_STEPPER_moveTo(next_zpos)


        elif button_id == 'btn-down':
            
            next_zpos=current_zpos-(10 ** (1+zpos_delta))
            
            print('jog down: next_zpos=',next_zpos)
            #if next_zpos>max_zpos:
            #    next_zpos=max_zpos
            #    print('max_zpos!')

            Z_STEPPER_moveTo(next_zpos)

        #elif button_id == 'btn-home':
        #    Z_STEPPER_setHome()  #this triggers at start?!!
            #df_params['zpos'][1]=0
        #else:
            #df_params['zpos'][1]=current_zpos

        
        df_params.loc[1,'zpos']=next_zpos
    return df_params.to_json() 
	
################
@app.callback(Output('fpos_var', 'children'),
              [Input('btn-home', 'n_clicks'),
               Input('btn-minus', 'n_clicks'),
               Input('btn-plus', 'n_clicks'),
               Input('btn-filterBRIGHT','n_clicks'),
               Input('btn-filterDARK','n_clicks'),
               Input('btn-filterGFP','n_clicks'),
               Input('btn-filterRFP','n_clicks'),
               Input('btn-filterCFP','n_clicks'),
               Input('btn-filterYFP','n_clicks'),
               Input('f_stepper_input', 'children')], [State('deltaJog_slider','value'), State("f_stepper_engaged", "value")])
def update(btn1, btn2, btn3, btnBRIGHT, btn4, btn5, btn6, btn7, btn8, fpos_target, fpos_delta, engaged):
    if engaged and with_f_stepper:
    
        try:
            
            min_fpos=df_params.loc[1,'fpos_min']
            max_fpos=df_params.loc[1,'fpos_max']
            current_fpos=df_params.loc[1,'fpos'] #
            #print("current_fpos: ",current_fpos)
            next_fpos=current_fpos
            
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = 'No clicks yet'
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

                
            if button_id == 'btn-minus':
                next_fpos=current_fpos+(10 ** fpos_delta)
                #print((next_fpos-df_params['fpos_min'][1]))
                #if (next_fpos-df_params['fpos_min'][1])>max_fpos:
                #    next_fpos=max_fpos
                print("jog- %s -> %s"%(int(10 ** fpos_delta), int(next_fpos*10)/10))

            elif button_id == 'btn-plus':
                
                next_fpos=current_fpos-(10 ** fpos_delta)
                #if next_fpos<min_fpos:
                #    next_fpos=min_fpos
                print("jog+ %s -> %s"%(int(10 ** fpos_delta), int(next_fpos*10)/10))


            elif button_id == 'btn-filterBRIGHT':
                next_fpos=df_params.loc[1,'fpos_filterBRIGHT']    
            elif button_id == 'btn-filterDARK':
                next_fpos=df_params.loc[1,'fpos_filterDARK']
            elif button_id == 'btn-filterGFP':
                next_fpos=df_params.loc[1,'fpos_filterGFP']
            elif button_id == 'btn-filterRFP':
                next_fpos=df_params.loc[1,'fpos_filterRFP']
            elif button_id == 'btn-filterCFP':
                next_fpos=df_params.loc[1,'fpos_filterCFP']
            elif button_id == 'btn-filterYFP':
                next_fpos=df_params.loc[1,'fpos_filterYFP']
                
            elif button_id == 'btn-home':
                fpos_home=F_STEPPER_setHome()
                next_fpos=current_fpos
            else:
                next_fpos=current_fpos

            
        except PhidgetException as e:
            print("Error in Detach Event:", e)
            return
        except Exception as e:
            return
  
        if next_fpos!=current_fpos:
            df_params.loc[1,'fpos']=next_fpos
            F_STEPPER_moveTo(next_fpos)  
            
    return df_params.to_json() 

	
############# 
@app.callback(Output('fpos_DARK', 'children'),
              [Input('btn-set-DARK', 'n_clicks')], [State('fpos_var','children')])
def update(btn, cached_data):
    if btn is not None:
        fpos_current=df_params['fpos'][1] #f_stepper.getPosition() #
        df_params.loc[1,'fpos_filterDARK']=fpos_current
        print("Set fpos_DARK to ",fpos_current)
    else:
        fpos_current=df_params.loc[1,'fpos_filterDARK']
    return fpos_current

############# 
@app.callback(Output('fpos_BRIGHT', 'children'),
              [Input('btn-set-BRIGHT', 'n_clicks')], [State('fpos_var','children')])
def update(btn, cached_data):
    if btn is not None:
        fpos_current=df_params['fpos'][1] #f_stepper.getPosition() #
        df_params.loc[1,'fpos_filterBRIGHT']=fpos_current
        print("Set fpos_BRIGHT to ",fpos_current)
    else:
        fpos_current=df_params.loc[1,'fpos_filterBRIGHT']
    return fpos_current
	
@app.callback(Output('fpos_GFP', 'children'),
              [Input('btn-set-GFP', 'n_clicks')], [State('fpos_var','children')])
def update(btn, cached_data):
	if btn is not None:
		fpos_current=df_params['fpos'][1] #f_stepper.getPosition() #
		df_params.loc[1,'fpos_filterGFP']=fpos_current
		print("Set fpos_GFP to ",fpos_current)
	else:
		fpos_current=df_params.loc[1,'fpos_filterGFP']
	return fpos_current
	
@app.callback(Output('fpos_RFP', 'children'),
              [Input('btn-set-RFP', 'n_clicks')], [State('fpos_var','children')])
def update(btn, cached_data):
	if btn is not None:
		fpos_current=df_params['fpos'][1] #f_stepper.getPosition() #
		df_params.loc[1,'fpos_filterRFP']=fpos_current
		print("Set fpos_RFP to ",fpos_current)
	else:
		fpos_current=df_params.loc[1,'fpos_filterRFP']
	return fpos_current
	
@app.callback(Output('fpos_CFP', 'children'),
              [Input('btn-set-CFP', 'n_clicks')], [State('fpos_var','children')])
def update(btn, cached_data):
	if btn is not None:
		fpos_current=df_params['fpos'][1] #f_stepper.getPosition() #
		df_params.loc[1,'fpos_filterCFP']=fpos_current
		print("Set fpos_CFP to ",fpos_current)
	else:
		fpos_current=df_params.loc[1,'fpos_filterCFP']
	return fpos_current
	
@app.callback(Output('fpos_YFP', 'children'),
              [Input('btn-set-YFP', 'n_clicks')], [State('fpos_var','children')])
def update(btn, cached_data):
	if btn is not None:
		fpos_current=df_params['fpos'][1] #f_stepper.getPosition() #
		df_params.loc[1,'fpos_filterYFP']=fpos_current
		print("Set fpos_YFP to ",fpos_current)
	else:
		fpos_current=df_params.loc[1,'fpos_filterYFP']
	return fpos_current
    
    
    
#######################################


@app.callback(Output('ncycles_progressbar', 'value'),
              [Input('ncycles_input', 'children')], [State('cycles_input', 'value'), State('timelapse_start','children')])
def update(ncycles, maxcycles, timelapse_start):
    ret=0
    if ncycles is not None:
        if maxcycles is not None:
            if isinstance(timelapse_start, list):
                timelapse_start=timelapse_start[0]
                
            if timelapse_start>0:
                ret=10*ncycles/int(maxcycles)
                if ret>10:
                    ret=10
    return ret

    

#######################################    
    
@app.callback(Output('runOne_output', 'children'),
              [Input('btn-runOne', 'n_clicks')], [State('tbl_opt_config', 'data'),
      State('filterBRIGHT_slider','value'), State('filterDARK_slider','value'), State('filterGFP_slider','value'), State('filterRFP_slider','value'), State('filterCFP_slider','value'), State('filterYFP_slider','value'), State('z_stepper_engaged','value'), State('f_stepper_engaged','value')])
def update(btn, list_opt_configs, exposureBRIGHT, exposureDARK, exposureGFP, exposureRFP, exposureCFP, exposureYFP, z_stepper_engaged, f_stepper_engaged):
    
    
    if btn is not None:
        
        for this_row in list_opt_configs:
            opt_configs=[]
            all_rows=this_row['opt_config-1'].split(' / ')
            for this_row in all_rows:
                opt_config=dict()
                
                
                st=this_row.split(' (')
                this_filter=st[0].strip()
                this_exposure=float(st[1].split('s')[0].strip())
                
                
            
                if this_filter == 'BRIGHT':
                    opt_config['channelID']='BRIGHT'
                    opt_config['ledOutput']=df_params.loc[1,'output_filterBRIGHT']
                    opt_config['ledColor']='BRIGHT'
                    opt_config['filterPos']=df_params.loc[1,'fpos_filterBRIGHT']
                    opt_config['exposure']=this_exposure #transform_value(exposureBRIGHT)
                    #shoot_single(opt_config)
                    opt_configs.append(opt_config)
            
                if this_filter == 'DARK':
                    
                    this_color=st[1].split('s')[1][1:].split(',')[0].strip()   
                    this_alpha=float(this_row.split(',')[2][3:-1])
                    #print("*%s*%s*"%(this_color,this_alpha))
                
                    
                    opt_config['channelID']='DARK'
                    opt_config['ledOutput']=df_params.loc[1,'output_filterDARK']
                    opt_config['ledColor']=this_color
                    opt_config['filterPos']=df_params.loc[1,'fpos_filterDARK']
                    opt_config['exposure']=this_exposure #transform_value(exposureDARK)
                    #shoot_single(opt_config)
                    opt_configs.append(opt_config)

                if this_filter == 'GFP':
                    opt_config['channelID']='GFP'
                    opt_config['ledOutput']=df_params.loc[1,'output_filterGFP']
                    opt_config['ledColor']='GREEN'
                    opt_config['filterPos']=df_params.loc[1,'fpos_filterGFP']
                    opt_config['exposure']=this_exposure #transform_value(exposureGFP)
                    #shoot_single(opt_config)
                    opt_configs.append(opt_config)

                if this_filter == 'RFP':
                    opt_config['channelID']='RFP'
                    opt_config['ledOutput']=df_params.loc[1,'output_filterRFP']
                    opt_config['ledColor']='RED'
                    opt_config['filterPos']=df_params.loc[1,'fpos_filterRFP']
                    opt_config['exposure']=this_exposure #transform_value(exposureRFP)
                    #shoot_single(opt_config)
                    opt_configs.append(opt_config)

                if this_filter == 'CFP':
                    opt_config['channelID']='CFP'
                    opt_config['ledOutput']=df_params.loc[1,'output_filterCFP']
                    opt_config['ledColor']='CYAN'
                    opt_config['filterPos']=df_params.loc[1,'fpos_filterCFP']
                    opt_config['exposure']=this_exposure #transform_value(exposureCFP)
                    #shoot_single(opt_config)
                    opt_configs.append(opt_config)

                if this_filter == 'YFP':
                    opt_config['channelID']='YFP'
                    opt_config['ledOutput']=df_params.loc[1,'output_filterYFP']
                    opt_config['ledColor']='YELLOW'
                    opt_config['filterPos']=df_params.loc[1,'fpos_filterYFP']
                    opt_config['exposure']=this_exposure #transform_value(exposureYFP)
                    #shoot_single(opt_config)
                    opt_configs.append(opt_config)
            
            #print(len(opt_configs),"*** ",opt_configs)
            if len(opt_configs)>1:
                shoot_multilight(opt_configs)  #Here we shoot!  
                
            elif len(opt_configs)==1:
                shoot_single(opt_configs[0])
        print("Run 1 finished")

            
@app.callback([Output('timelapse_start', 'children'), Output('timelapse_end', 'children')],
              [Input('btn-runtimelapse', 'n_clicks')], [State("timelapse_t", "n_intervals"),State("cycles_input", "value"),State('interval_input','value'),State('incubator_checkbox','value')  ])
def update(btn, t_start, ncycles_input, interval_input, incubate):
    ret_start=-1
    ret_end=-1
    
    if btn is not None:
        if isinstance(interval_input,str) and int(interval_input)>0:
            #if isinstance(ncycles_input,str) and int(ncycles_input)>0:

                #Here we turn-on incubator
                #if incubate:
                #    print('> Turning on Incubator')

                ret_start=t_start
                ret_end=t_start+(int(ncycles_input)-1)*int(interval_input)+2

    return ret_start, ret_end

@app.callback(Output('timelapse_stop', 'children'),
              [Input('btn-stop', 'n_clicks')], [State("timelapse_t", "n_intervals")])
def update(btn, t_stop):
    return int(t_stop)
        
    
@app.callback(Output('timelapse_click', 'children'),
              [Input('btn-click', 'n_clicks')], [State("interfaceKit_engaged", "value")])
def update(btn, engaged):
    texposure=1.00
    cameraOutput=df_params.loc[1,'output_camera']
    if engaged:
        CAMERA_trigger(interfaceKit_output, cameraOutput, texposure)
    return True

####################################### timelapse

 
@app.callback([Output('ncycles_input','children'), Output('timer_input', 'children')],
              [Input("timelapse_t", "n_intervals")],
              [State('tbl_opt_config', 'data'),
      State('filterBRIGHT_slider','value'),State('filterDARK_slider','value'), State('filterGFP_slider','value'), State('filterRFP_slider','value'), State('filterCFP_slider','value'), State('filterYFP_slider','value'), State("interval_input", "value"), State("interfaceKit_engaged", "value"), State("timelapse_start","children"), State("timelapse_end","children"), State("timelapse_stop","children"), State('incubator_checkbox','value')]) 
    
def listener_x(t_timelapse, list_opt_configs, exposureBRIGHT, exposureDARK, exposureGFP, exposureRFP, exposureCFP, exposureYFP, interval_timelapse, engaged, t_start, t_end, t_stop, incubate): 
    ti=0
    ncycles=0
    
    try:
        if isinstance(t_start,int) and t_start>0:
            if isinstance(t_end,int) and t_timelapse<t_end:
                if t_stop==(t_timelapse-1):
                    print('> Time-lapse stopped')
                    
                    
                    #ToDo. Here we turn off incubator
                    if incubate:
                        print('> Turning-off incubator')
                        
                elif t_stop<t_start:
                    
                    
                    #Here we do timelapse
                    t_timelapse_start=int(t_timelapse)-int(t_start)-2
                    if interval_timelapse is not None:
                        ncycles=int(t_timelapse_start/int(interval_timelapse))+1
                        if engaged:
                            ti=int(interval_timelapse)*ncycles-t_timelapse_start-1
                        else:
                            ti=int(interval_timelapse)*ncycles-t_timelapse_start-1 #Tmp (Should be 0)
                    else:
                        ti=0
                    
                    
                    #Define optical configurations
                    for this_row in list_opt_configs:
                        opt_configs=[]
                        all_rows=this_row['opt_config-1'].split(' / ')
                        for this_row in all_rows:
                            opt_config=dict()

                            st=this_row.split(' (')
                            this_filter=st[0].strip()
                            this_exposure=float(st[1].split('s')[0].strip())
                            this_color=st[1].split('s')[1][1:].split(')')[0].strip()

                            if this_filter == 'DARK':
                                opt_config['channelID']='DARK'
                                opt_config['ledOutput']=df_params.loc[1,'output_filterDARK']
                                opt_config['ledColor']=this_color
                                opt_config['filterPos']=df_params.loc[1,'fpos_filterDARK']
                                opt_config['exposure']=transform_value(exposureDARK)
                                #shoot_single(opt_config)
                                opt_configs.append(opt_config)
                                
                            if this_filter == 'BRIGHT':
                                opt_config['channelID']='BRIGHT'
                                opt_config['ledOutput']=df_params.loc[1,'output_filterBRIGHT']
                                opt_config['ledColor']='BRIGHT'
                                opt_config['filterPos']=df_params.loc[1,'fpos_filterBRIGHT']
                                opt_config['exposure']=transform_value(exposureBRIGHT)
                                #shoot_single(opt_config)
                                opt_configs.append(opt_config)

                            if this_filter == 'GFP':
                                opt_config['channelID']='GFP'
                                opt_config['ledOutput']=df_params.loc[1,'output_filterGFP']
                                opt_config['ledColor']='GREEN'
                                opt_config['filterPos']=df_params.loc[1,'fpos_filterGFP']
                                opt_config['exposure']=transform_value(exposureGFP)
                                #shoot_single(opt_config)
                                opt_configs.append(opt_config)

                            if this_filter == 'RFP':
                                opt_config['channelID']='RFP'
                                opt_config['ledOutput']=df_params.loc[1,'output_filterRFP']
                                opt_config['ledColor']='RED'
                                opt_config['filterPos']=df_params.loc[1,'fpos_filterRFP']
                                opt_config['exposure']=transform_value(exposureRFP)
                                #shoot_single(opt_config)
                                opt_configs.append(opt_config)

                            if this_filter == 'CFP':
                                opt_config['channelID']='CFP'
                                opt_config['ledOutput']=df_params.loc[1,'output_filterCFP']
                                opt_config['ledColor']='CYAN'
                                opt_config['filterPos']=df_params.loc[1,'fpos_filterCFP']
                                opt_config['exposure']=transform_value(exposureCFP)
                                #shoot_single(opt_config)
                                opt_configs.append(opt_config)

                            if this_filter == 'YFP':
                                opt_config['channelID']='YFP'
                                opt_config['ledOutput']=df_params.loc[1,'output_filterYFP']
                                opt_config['ledColor']='YELLOW'
                                opt_config['filterPos']=df_params.loc[1,'fpos_filterYFP']
                                opt_config['exposure']=transform_value(exposureYFP)
                                #shoot_single(opt_config)
                                opt_configs.append(opt_config)
                                
                            

                        if ti==int(interval_timelapse) or ti==0:  #Here we shoot!  
                            if len(opt_configs)>1:
                                shoot_multilight(opt_configs) 
                            else:
                                shoot_multichannel(opt_configs)    
                    if (t_timelapse+1)==int(t_end):
                        print('> Time-lapse finished')
                        print('> Turning-off incubator')
                

    except Exception as e:
        print("Error in timelapse:",e)
     
    return [ncycles, ti]
        
    
@app.callback(Output('f_stepper_input', 'children'),
              [Input("listener", "n_intervals")],
              [State("interfaceKit_engaged", "value"),State("fpos_var", "children")])
def listener_x(_, connection, cached_data):
    
    ret=df_params.loc[1,'fpos']
    
    return ret

    
    
    
        
#######################################

##################################### MAIN
if __name__ == '__main__':
    app.run_server(debug=True)