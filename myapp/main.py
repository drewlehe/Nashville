import bokeh
from bokeh.layouts import column, widgetbox
from bokeh.models.widgets import Button, Paragraph, Dropdown, Slider, TextInput, CheckboxButtonGroup, Select, RadioButtonGroup, RadioGroup
from bokeh.plotting import curdoc, show, figure
from bokeh.embed import file_html, components
import json
import pps_regressor

def update_data(event):
    bldg_data = {
        'Neighborhood': str(float(nbhd.value_input)),
        'Building-Type-Custom': density.active,
        'Fixtures': fixtures.value,
        'Year Built': int(yearbuilt.value_input),
        'Building-Grade': segment.active,
        'Square Footage': squarefootage.value,
        'Renovation': reno_new.active,
        'Quarter': quarter.active,
        'Year': 2019}
    
    price_pred = pps_regressor.prediction(bldg_data)
    p.text = '$' + str(price_pred[0] * bldg_data['Square Footage'])

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
fixtures = Slider(start=3, end=20, value = 4, step=1, title="Water Fixtures")
calculate = Button(label="Get Price", button_type="success")
calculate.on_click(update_data)
# p = Paragraph(text="{}".format(price_pred * bldg_data['Square Footage']))
p = Paragraph(text="foobar")
box = widgetbox([density, nbhd, reno_new, yearbuilt, squarefootage, segment, fixtures, quarter, calculate, p])
curdoc().add_root(box)