'''Create the widget and feed a dictionary of selected values to pps_regressor.py when the "Get Price" button is clicked'''
import bokeh
from bokeh.layouts import widgetbox
from bokeh.models.widgets import *
from bokeh.plotting import curdoc, show, figure
import json
import pps_regressor
import pandas as pd

with open('meanpps.json', 'r') as nbhdpps:
        nbhd_dict = json.load(nbhdpps)
meanpps = pd.DataFrame(nbhd_dict, index=None)
hoods = [str(int(float(i))) for i in meanpps.index]


def update_data(event):
    '''Create a dictionary of selected values in the widget when the "Get Price" button is pressed'''
    bldg_data = {
        'Neighborhood': str(nbhd.value),
        'Building-Type-Custom': density.active,
        'Year Built': int(yearbuilt.value_input),
        'Building-Grade': segment.active,
        'Square Footage': squarefootage.value,
        'Renovation': reno_new.active,
        'Quarter': quarter.active,
        'Year': 2019}
    if reno_new.active == 1:
        bldg_data['Year Built'] = 2019
    else:
        bldg_data['Year Built'] = int(yearbuilt.value_input)
    pps_pred = pps_regressor.prediction(bldg_data)
    result = pps_pred[0] * bldg_data['Square Footage']
    p.text = "${:,.2f}".format(result)

# Create some widgets
nbhd = Select(title="Neighborhood:", options=hoods)
density = RadioButtonGroup(labels=['Single-Family', 'Multi-Family'])
reno_new = RadioButtonGroup(labels=["Renovation", "New Build"])
yearbuilt = TextInput(placeholder="4-digit #", title="Year of the original structure (if renovation):")
squarefootage = Slider(start=500, end=3500, value=500, step=10, title="Square Footage")
segment = RadioButtonGroup(labels=["Affordable", "Mid-Range", "High-End"])
quarter = RadioGroup(labels = ['First Quarter Sale', 'Second Quarter Sale', 'Third Quarter Sale', 'Fourth Quarter Sale'])
fixtures = Slider(start=3, end=20, value=3, step=1, title="Water Fixtures")
calculate = Button(label="Get Price", button_type="success")
calculate.on_click(update_data)
p = Paragraph(text="Price here")
box = widgetbox([density, nbhd, reno_new, yearbuilt, squarefootage, segment, quarter, calculate, p])
curdoc().add_root(box)
    