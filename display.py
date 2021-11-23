from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
import requests
import pandas as pd

# Set the stop and top results remover
stop_code = '<Add a bus ATCO code>'
remove_top = 1

# Set the URL
url = 'http://yorkshire.acisconnect.com/Text/WebDisplay.aspx?stopRef=' + stop_code

#Set the display parameters
inky_display = auto()
white = inky_display.WHITE
black = inky_display.BLACK
inky_display.set_border(white)
tab_1 = 5
tab_2 = 45
tab_3 = 180

# Flip the display
inky_display.v_flip = True
inky_display.h_flip = True
# Set two font types
font_1 = ImageFont.truetype(FredokaOne, 16)
font_2 = ImageFont.truetype(FredokaOne, 18)
# Wipe the screen
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)
# Get the bus times
try:
        request = requests.get(url, timeout=3)
        request.raise_for_status()
except requests.exceptions.Timeout:
        # If it fails then print message
        draw.text((tab_1,y, 1,1), 'Oh no! No interwebs!', black, font_2)
        inky_display.set_image(img)
        inky_display.show()
        exit()

html_content = request.text

# Get the table
tables = pd.read_html(html_content)
# Get the first and only table
df = tables[0]

# Extract the bus times
# Draw the times on the screen
y = 30
for i in range(4):
        try:
                draw.text((tab_1,y, 1,1), df['Service'][i+remove_top], black, font_2)
                draw.text((tab_2,y, 1,1), df['To'][i+remove_top][:12], black, font_2)
                draw.text((tab_3,y, 1,1), df['Time'][i+remove_top], black, font_2)
        except KeyError:
                x = i + remove_top
                print('KeyError: no bus at key ' + str(x))
        y = y + 22

# Format the current time
time = datetime.today().strftime('Updated on %d/%m/%Y, %H:%M')

# Draw the update banner on the screen
draw.rectangle((1,25, 260,1), fill=1, outline=None)
draw.text((5,1, 1,1), time, white, font_1)

# Display the ouput on the screen
inky_display.set_image(img)
inky_display.show()
