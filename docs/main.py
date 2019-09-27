import bokeh
from bokeh.layouts import column, widgetbox
from bokeh.models.widgets import Dropdown, Slider, TextInput, CheckboxButtonGroup, RadioButtonGroup, Button
from bokeh.io import curdoc, show
from os.path import dirname, join
from bokeh.plotting import curdoc


json_out = 'selection.json'

def update_data(event):
    print(f'{event}')
    bldg_data = {
        'Neighborhood': str(nbhd.value),
        'Building Type Custom': density.value,
        'Fixtures': fixtures.value,
        'Exterior Wall': wall.value,
        'Year Built': str(yearbuilt.value),
        'Building Grade': segment.value,
        'SqFt Improved': squarefootage.value,
        'Renovation': reno_new.active}
    print(f'{bldg_data}')
    with open(json_out, 'w') as out:
        json.dump(bldg_data, out)
    pps_regressor.prediction(json_out)
    
# def make_menu():
#Create some widgets
nbhd = TextInput(value="4-digit #", title="Neighborhood Code:")
densities = [("Single-Family Detached", "item_1"), ("Plex", "item_2"), ("Mid-Rise", "item_3"), ("High-Rise", "item_4")]
density = Dropdown(label="Density", button_type="primary", menu=densities)
reno_new = RadioButtonGroup(labels=["Renovation", "New Build"])
#If renovation, select year built of the property:
yearbuilt = TextInput(value="4-digit #", title="Year of the original structure (if renovation):")
squarefootage = Slider(start=500, end=3500, value=500, step=10, title="Square Footage")
segments = [("Affordable", "item_1"), ("Mid-Range", "item_2"), ("High-End", "item_3"), ("Ultra-Lux", "item_4")]
segment = Dropdown(label="Market Segment", button_type="primary", menu=segments)
fixtures = Slider(start=3, end=20, value=3, step=1, title="Water Fixtures")
wall_types = [("Wood or Vinyl", "item_1"), ("Brick or Stucco", "item_2"), ("Glass", "item_3"), ("Concrete", "item_4")]
wall = Dropdown(label="Exterior Wall (optional)", button_type="primary", menu=wall_types)

calculate = Button(label="Get Price", button_type="success")
calculate.on_click(update_data)
box = widgetbox([nbhd, density, reno_new, yearbuilt, squarefootage, segment, fixtures, wall, calculate])
# show(box)

def show_box(doc):
    doc.add_root(box)
    show(show_box)
    
# box = make_menu()

# show_box
curdoc().add_root(box)
