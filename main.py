import bokeh
from bokeh.layouts import column, widgetbox
from bokeh.models.widgets import Button, Paragraph, Dropdown, Slider, TextInput, CheckboxButtonGroup, Select, RadioButtonGroup, RadioGroup
from os.path import dirname, join
from bokeh.plotting import curdoc, show, output_file, figure
from bokeh.embed import file_html, components
import json
from bokeh.resources import CDN
import pps_regressor


json_out = 'selection.json'

def update_data(event):
    print(f'{event}')
    bldg_data = {
        'Neighborhood': str(nbhd.value_input),
        'Building-Type-Custom': density.active,
        'Fixtures': fixtures.value,
        'Year Built': int(yearbuilt.value_input),
        'Building-Grade': segment.active,
        'Square Footage': squarefootage.value,
        'Renovation': reno_new.active,
        'Quarter': quarter.active,
        'Year': 2019}
    with open(json_out, 'w') as out:
        json.dump(bldg_data, out)
    price_pred = pps_regressor.prediction(json_out)
    total = float(price_pred) * bldg_data['Square Footage']
    with open('prediction.json', 'w') as file:
        json.dump(total, file)

    
# Create some widgets
nbhd = TextInput(placeholder="4-digit #", title="Neighborhood Code:")
densities = {"Single-Family":"SINGLE FAM", "Plex": "PLEX", "Mid-Rise": "CONDO", "High-Rise": "HRISE CONDO"}
density = RadioButtonGroup(labels=['Single-Family', 'Plex', 'Mid-Rise', 'High-Rise'])
reno_new = RadioButtonGroup(labels=["Renovation", "New Build"])
#If renovation, select year built of the property:
yearbuilt = TextInput(placeholder="4-digit #", title="Year of the original structure (if renovation):")
squarefootage = Slider(start=500, end=3500, value=500, step=10, title="Square Footage")
segments = {"Affordable": "C", "Mid-Range":"B", "High-End":"A", "Ultra-Lux":"X"}
segment = RadioButtonGroup(
        labels=["Affordable", "Mid-Range", "High-End", "Luxury"])
quarters = [("One", 1), ("Two", 2), ("Three", 3), ("Four", 4)]
quarter = RadioGroup(labels = ['First', 'Second', 'Third', 'Fourth'])
fixtures = Slider(start=3, end=20, value=3, step=1, title="Water Fixtures")
calculate = Button(label="Get Price", button_type="success")
calculate.on_click(update_data)
box = widgetbox([density, nbhd, reno_new, yearbuilt, squarefootage, segment, fixtures, quarter, calculate])

curdoc().add_root(box)

with open('prediction.json', 'r') as file:
    pred = json.load(file)
p = Paragraph(text="{}".format(pred))
curdoc().add_root(p)