#!/bin/false
# This file is part of Espruino, a JavaScript interpreter for Microcontrollers
#
# Copyright (C) 2026 Joakim Stai
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# ----------------------------------------------------------------------------------------
# This file contains information for a specific board - the available pins, and where LEDs,
# Buttons, and other in-built peripherals are. It is used to build documentation as well
# as various source and header files for Espruino.
# ----------------------------------------------------------------------------------------
#
# Cardputer
# * Graphics initialised as 'g'
# * FAT Filesystem via require("fs")

import pinutils;
info = {
 'name'                     : 'CARDPUTER',
 'espruino_page_link'       : '',
 'default_console'          : 'EV_SERIAL1',
 'default_console_baudrate' : '115200',
 'variables'                : 16383,
 'io_buffer_size'           : 4096,
 'binary_name'              : 'espruino_%v_cardputer.bin',
 'build' : {
   'optimizeflags' : '-Og',
   'libraries' : [
     'ESP32',
     'BLUETOOTH',
     'NET',
     'TERMINAL',
     'GRAPHICS',
     'LCD_SPI_UNBUF',
     'CRYPTO','SHA256','SHA512',
     'TLS',
     'TELNET',
     'NEOPIXEL',
     'FILESYSTEM',
   ],
   'makefile' : [
     'DEFINES+=-DESP_PLATFORM -DESP32',
     'DEFINES+=-DESP_STACK_SIZE=25000',
     'DEFINES+=-DJSVAR_MALLOC', # Allocate space for variables at jsvInit time
     'DEFINES+=-DDUMP_IGNORE_VARIABLES=\'"g\\0"\'',
     'DEFINES+=-DESPR_GRAPHICS_INTERNAL',
     'DEFINES+=-DESPR_GRAPHICS_SELF_INIT',
     'DEFINES+=-DUSE_LCD_SPI_UNBUF',
     'DEFINES+=-DSPISENDMANY_BUFFER_SIZE=1600', # 4096 for ESP32-S3?
     'DEFINES+=-DUSE_FONT_6X8',
     'DEFINES+=-DLCD_SPI_BITRATE=40000000',
     'DEFINES+=-DESPR_TERMNINAL_NO_SCROLL',
     'DEFINES+=-DESPR_USE_USB_SERIAL_JTAG',
     'ESP32_FLASH_MAX=1572864',
   ]
 }
};

chip = {
  'part'    : "ESP32S3",
  'family'  : "ESP32_IDF4",
  'package' : "QFN56",
  'ram'     : 512,
  'flash'   : 8192,
  'speed'   : 240,
  'usart'   : 3,
  'spi'     : 2,
  'i2c'     : 2,
  'adc'     : 2,
  'dac'     : 0,
  'saved_code' : {
    'address' : 0x320000,
    'page_size' : 4096,
    'pages' : 224, # 896kb - see partitions_espruino.csv
    'flash_available' : 1344, # firmware can be up to this size - see partitions_espruino.csv
  },
};

devices = {
  'LED1' : { 'pin' : 'D2' },
  'BTN1' : { 'pin' : 'D0', "inverted": 1, 'pinstate' : 'IN_PULLUP' },
  'LCD' : {
            'width' : 240, 'height' : 135, 'bpp' : 16,
            'controller' : 'st7789v',
            'pin_dc' : 'D34',
            'pin_cs' : 'D37',
            'pin_rst' : 'D33',
            'pin_sck' : 'D36',
            'pin_mosi' : 'D35',
            'pin_bl' : 'D38',
            'spi_device' : 'EV_SPI1',
          },
#   'SD' :  { 'pin_cs' :  'D12',
#             'pin_di' :  'D14',
#             'pin_do' :  'D39',
#             'pin_clk' : 'D40',
#           },
#   'BAT' : {
#             'pin_voltage' : 'D10',
#           },
};

# left-right, or top-bottom order
board_esp32 = {
   'top' : ['GND','D23','D22','D1','D3','D21','D20','D19','D18','D5','D17','D16','D4','D0'],
   'bottom' : ['D12','D14','D27','D26','D25','D33','D32','D35','D34','D39','D36','EN','3V3','GND'],
   'right' : [ 'GND','D13','D9','D10','D11','D6','D7','D8','D15','D2']
};
board_esp32["bottom"].reverse()
board_esp32["right"].reverse()
board_esp32["_css"] = """
#board {
  width:  600px;
  height: 435px;
  left: 50px;
  top: 170px;
  background-image: url(img/ESP32.jpg);
}
#boardcontainer {
  height: 700px;
}
#board #right {
  top: 80px;
  left: 600px;
}
#board #top {
  bottom: 440px;
  left: 155px;
}
#board #bottom  {
  top: 435px;
  left: 155px;
}
#board .rightpin {
  height: 28px;
}
#board .toppin, #board .bottompin {
  width: 24px;
}
""";

boards = [ board_esp32 ];

def get_pins():
  # ESP32-S3 has 45 Physical GPIO pins Numbered 0->21 and 26->48
  # see https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf
  # Cardputer has 0->21 and 33->48
  # see https://github.com/m5stack/M5Unified?tab=readme-ov-file#esp32s3-gpio-list
  pins = pinutils.generate_pins(0,48)
  # TODO: we could delete 22..32 as Cardputer doesn't seem to have those

  # I2C (Grove)
#   pinutils.findpin(pins, "PD1", True)["functions"]["I2C1_SCL"]=0;
#   pinutils.findpin(pins, "PD2", True)["functions"]["I2C1_SDA"]=0;

  # SPI1, used by the display
  pinutils.findpin(pins, "PD36", True)["functions"]["SPI1_SCK"]=0;
  pinutils.findpin(pins, "PD37", True)["functions"]["SPI1_MISO"]=0;

  # SPI2, used by the microSD slot
#   pinutils.findpin(pins, "PD40", True)["functions"]["SPI2_SCK"]=0;
#   pinutils.findpin(pins, "PD39", True)["functions"]["SPI2_MISO"]=0;
#   pinutils.findpin(pins, "PD14", True)["functions"]["SPI2_MOSI"]=0;

  # everything is non-5v tolerant
  #for pin in pins:
  #  pin["functions"]["3.3"]=0;
  return pins
