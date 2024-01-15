# display single image
from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7 as DISPLAY  # 7.3"
import inky_frame
import jpegdec

IMAGE_A = "me-n-clio-small.jpg"

graphics = PicoGraphics(DISPLAY)
decoder = jpegdec.JPEG(graphics)

def display_image(filename):
    decoder.open_file(filename)
    decoder.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
    # Display the result
    graphics.update()

display_image(IMAGE_A)

while True:
  for button in [inky_frame.button_a, inky_frame.button_b, inky_frame.button_c, inky_frame.button_d, inky_frame.button_e]:
      button.led_off()

  # sleep if on battery
  inky_frame.turn_off()