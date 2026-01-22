#!/bin/false
# This file is part of Espruino, a JavaScript interpreter for Microcontrollers
#
# Copyright (C) 2013 Gordon Williams <gw@pur3.co.uk>
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
 'variables'                : 16383, # See note above
 'io_buffer_size'           : 4096, # How big is the input buffer (in bytes). Default on nRF52 is 1024
 'binary_name'              : 'espruino_%v_cardputer.bin',
 'build' : {
   'optimizeflags' : '-Og',
   'libraries' : [
     'BLUETOOTH',
     'CRYPTO', 'SHA256', 'SHA512',
     'ESP32',
     'FILESYSTEM',
     'GRAPHICS',
     'LCD_SPI_UNBUF',
     'NEOPIXEL',
     'NET',
     'TELNET',
     'TERMINAL',
     'TLS',
   ],
   'makefile' : [
     'DEFINES+=-DESP_PLATFORM -DESP32',
     'DEFINES+=-DESP_STACK_SIZE=25000',
     'DEFINES+=-DJSVAR_MALLOC', # Allocate space for variables at jsvInit time
     'DEFINES+=-DESPR_GRAPHICS_INTERNAL -DESPR_GRAPHICS_SELF_INIT', # ensure graphics instantiates itself
     'DEFINES+=-DUSE_FONT_6X8 -DSPISENDMANY_BUFFER_SIZE=1600 -DLCD_SPI_BITRATE=55000000 -DESPR_TERMNINAL_NO_SCROLL',
     'DEFINES+=-DUSE_LCD_SPI_UNBUF',
     'DEFINES+=-DESPR_USE_USB_SERIAL_JTAG', # See note above
     'ESP32_FLASH_MAX=1572864',
   ]
 }
};

chip = {
  'part'    : "ESP32S3",
  'family'  : "ESP32_IDF4",
  'package' : "QFN56",
  'ram'     : 512,
  'flash'   : 0, # 8192?
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
  'SD' :  { 'pin_cs' :  'D12',
            'pin_di' :  'D14',
            'pin_do' :  'D39',
            'pin_clk' : 'D40',
          },
  'BAT' : {
            'pin_voltage' : 'D10',
          },
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
  pins = pinutils.generate_pins(0,48)
  # TODO: we could delete 22..25 as ESP32-S3 doesn't seem to have those

  # I2C added for issue #2589 - all decided by user (not defined in specs)
  pinutils.findpin(pins, "PD8", True)["functions"]["I2C1_SDA"]=0;
  pinutils.findpin(pins, "PD9", True)["functions"]["I2C1_SCL"]=0;
  pinutils.findpin(pins, "PD18", True)["functions"]["I2C2_SDA"]=0;
  pinutils.findpin(pins, "PD19", True)["functions"]["I2C2_SCL"]=0;

  # SPI added for issue #2601
  #  - for SPI1 use pins that will bypass GPIO matrix (So Quicker) see esp-idf-4 /components/soc/esp32s3/include/soc/spi_pins.h
  pinutils.findpin(pins, "PD12", True)["functions"]["SPI1_SCK"]=0;
  pinutils.findpin(pins, "PD13", True)["functions"]["SPI1_MISO"]=0;
  pinutils.findpin(pins, "PD11", True)["functions"]["SPI1_MOSI"]=0;
  #  - SPI2 is decided by user
  pinutils.findpin(pins, "PD4", True)["functions"]["SPI2_SCK"]=0;
  pinutils.findpin(pins, "PD6", True)["functions"]["SPI2_MISO"]=0;
  pinutils.findpin(pins, "PD7", True)["functions"]["SPI2_MOSI"]=0;

  pinutils.findpin(pins, "PD43", True)["functions"]["USART1_TX"]=0;
  pinutils.findpin(pins, "PD44", True)["functions"]["USART1_RX"]=0;
  pinutils.findpin(pins, "PD17", True)["functions"]["USART2_TX"]=0;
  pinutils.findpin(pins, "PD18", True)["functions"]["USART2_RX"]=0;

  # everything is non-5v tolerant
  #for pin in pins:
  #  pin["functions"]["3.3"]=0;
  return pins
