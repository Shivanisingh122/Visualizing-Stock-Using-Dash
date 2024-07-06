import dash 
from dash.dependencies import Input, Output
import datetime
from dash import Dash, dcc, html, Input, Output, State
import yfinance as yf
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import pandas as pd
import speech_recognition as sr 
import pyglet
import os
import time
from gtts import gTTS 
import webbrowser 

#code for speech recognition
say = gTTS(text=" Hi Welcome to the Stock Dash App please Input stock code ", 
lang='en')
convert =("1.mp3") 
say.save(convert)
music = pyglet.media.load(convert, streaming = False)
music.play()
time.sleep(music.duration)
os.remove(convert)

speech1 = sr.Recognizer()
with sr.Microphone() as source:
    speech1.adjust_for_ambient_noise(source,duration=1)
    print ("\t Please Input stock code :\n")
    speech2=speech1.listen(source)
    print ("\t\t\tCommand Accepted\n")

try:
    ticker=(speech1.recognize_google(speech2)).upper()
    print ("\t\tYou said : "+ ticker)
    
except sr.UnknownValueError:
    print("Can't Understand the command. Run Again")
     
except sr.RequestError as e:
    print("Could not Connect to the Internet; {0}".format(e))

#code for web app

app=dash.Dash(__name__)
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
server = app.server

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Welcome to the Stock Dash App !',className='start',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
html.Div(html.H2(children='Dash : A web application framework') , style={
        'textAlign': 'center',
       'color': colors['text']
    }),

html.H2(children="Input stock code : ",
    style={'color': colors['text']
    }),

    html.Div(
    dcc.Input(id='input_data', value= ticker , type='text')),
    html.Div(id="output-graph")
]
)

#call back for data input

@app.callback(
    Output("output-graph",'children'),
    Input("input_data","value"),
)
def update_value(input_data):
    start = datetime.datetime(2015,1,1)
    end = datetime.datetime.now()
    df = web.DataReader(input_data ,'yahoo', start , end)
    
    return dcc.Graph(id="example",
    figure={'data': [{'x': df.index, 'y': df.Close,'type':'line',
        'name': input_data},], 'layout':
        {'title': input_data}})

if __name__ == '__main__' :
    app.run_server()
    url='http://127.0.0.1:8050/'
    webbrowser.open_new_tab(url)
