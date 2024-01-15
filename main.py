# inky frame launcher
import gc
import time
from machine import reset
import inky_helper as ih
from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7 as DISPLAY  # 7.3"

# A short delay to give USB chance to initialise
time.sleep(0.5)

# Setup for the display.
graphics = PicoGraphics(DISPLAY)
WIDTH, HEIGHT = graphics.get_bounds()
Y_OFFSET = 35
graphics.set_font("bitmap8")

def maybe_launch(button, program_name):
    if button.read():
        button.led_on()
        ih.update_state(program_name)
        time.sleep(0.5)
        reset()

def launcher():
    # Draws the menu
    graphics.set_pen(1)
    graphics.clear()
    graphics.set_pen(0)

    graphics.set_pen(graphics.create_pen(255, 215, 0))
    graphics.rectangle(0, 0, WIDTH, 50)
    graphics.set_pen(0)
    title = "launcher"
    title_len = graphics.measure_text(title, 4) // 2
    graphics.text(title, (WIDTH // 2 - title_len), 10, WIDTH, 4)

    def launcher_box(pen, y, x, text):
        graphics.set_pen(pen)
        graphics.rectangle(30, HEIGHT - (y + Y_OFFSET), WIDTH - x, 50)
        graphics.set_pen(1)
        text_y = y - 15
        graphics.text(text, 35, HEIGHT - (text_y + Y_OFFSET), 600, 3)

    launcher_box(4, 340, 100, "a. nasa picture of the day")
    launcher_box(6, 280, 150, "b. word clock")
    launcher_box(2, 220, 200, "c. daily activity")
    launcher_box(3, 160, 250, "d. headlines")
    launcher_box(0, 100, 300, "e. random joke")

    graphics.set_pen(graphics.create_pen(220, 220, 220))
    graphics.rectangle(WIDTH - 100, HEIGHT - (340 + Y_OFFSET), 70, 50)
    graphics.rectangle(WIDTH - 150, HEIGHT - (280 + Y_OFFSET), 120, 50)
    graphics.rectangle(WIDTH - 200, HEIGHT - (220 + Y_OFFSET), 170, 50)
    graphics.rectangle(WIDTH - 250, HEIGHT - (160 + Y_OFFSET), 220, 50)
    graphics.rectangle(WIDTH - 300, HEIGHT - (100 + Y_OFFSET), 270, 50)

    graphics.set_pen(0)
    note = "hold a & e, then reset to return to the launcher ^-^"
    note_len = graphics.measure_text(note, 2) // 2
    graphics.text(note, (WIDTH // 2 - note_len), HEIGHT - 30, 600, 2)

    ih.led_warn.on()
    graphics.update()
    ih.led_warn.off()

    # watch for button press and launch appropriate program
    while True:
        maybe_launch(ih.inky_frame.button_a, "nasa_apod")
        maybe_launch(ih.inky_frame.button_b, "word_clock")
        maybe_launch(ih.inky_frame.button_c, "daily_activity")
        maybe_launch(ih.inky_frame.button_d, "news_headlines")
        maybe_launch(ih.inky_frame.button_e, "random_joke")


# Turn any LEDs off that may still be on from last run.
ih.clear_button_leds()
ih.led_warn.off()

if ih.inky_frame.button_a.read() and ih.inky_frame.button_e.read():
    launcher()

ih.clear_button_leds()

if ih.file_exists("state.json"):
    # Loads the JSON and launches the app
    ih.load_state()
    ih.launch_app(ih.state['run'])

    # Passes the the graphics object from the launcher to the app
    ih.app.graphics = graphics
    ih.app.WIDTH = WIDTH
    ih.app.HEIGHT = HEIGHT
else:
    launcher()

try:
    from secrets import WIFI_SSID, WIFI_PASSWORD
    ih.network_connect(WIFI_SSID, WIFI_PASSWORD)
except ImportError:
    print("Create secrets.py with your WiFi credentials")

# Get some memory back, we really need it!
gc.collect()

file = ih.file_exists("state.json")

print(file)

while True:
    ih.app.update()
    ih.led_warn.on()
    ih.app.draw()
    ih.led_warn.off()
    ih.sleep(ih.app.UPDATE_INTERVAL)

