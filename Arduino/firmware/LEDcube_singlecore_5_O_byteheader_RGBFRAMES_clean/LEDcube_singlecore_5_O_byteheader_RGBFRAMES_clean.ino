// we need FastLED v. 3.3.3 or older to be compatible with arduino Due
#include <FastLED.h>

// How many leds are in the strip?
#define NUM_LEDS 3200
// This is an array of leds.  One item for each led in your strip.
CRGB leds[NUM_LEDS];

uint8_t rgbArray[(NUM_LEDS/2)*3];

bool framePass = false;

// USE position_mask_generator.py TO GENERATE POSITION_MASK ARRAY
const uint8_t PROGMEM POSITION_MASK[] = {
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b11000000, 0b00000000, 0b00000000, 0b00000100,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b10000000, 0b00000001, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00100000, 0b00000000, 0b00000000, 0b00000011, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000011, 0b00000000, 0b00000100, 0b00000000, 0b00001110, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000011, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000111, 0b00000000, 0b00100000, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b00010000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000010, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b11000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00110000, 0b00000000, 0b00000000, 0b11111111, 0b00000011, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000001, 0b00000000, 0b00000000,
    0b00000000, 0b00100000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b01000000, 0b00000000, 0b00000000, 0b00000010, 0b00000000, 0b00001100, 0b00000000, 0b11000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000001,
    0b00000000, 0b00000000, 0b00000000, 0b01100000, 0b00000000, 0b00000000, 0b00000010,
};

// Position check using bit operations
inline bool replacedLedPosition(uint16_t pos) {
  return pgm_read_byte(&POSITION_MASK[pos >> 3]) & (1 << (pos & 7));
}

void setup() {
  // put your setup code here, to run once:
  SerialUSB.begin(230400);
  SerialUSB.setTimeout(50);
  // sanity check delay - allows reprogramming if accidently blowing power w/leds
  delay(2000);
  LEDS.addLeds<WS2811_PORTD,8,RGB>(leds, 400).setCorrection(TypicalLEDStrip);

  // Red LEDs at the end of each strand
  const uint16_t redPositions[] = {390, 790, 1192, 1584, 1987};
  for(uint8_t i = 0; i < 5; i++) {
    leds[redPositions[i]] = CRGB::Red;
    leds[redPositions[i] + 1] = CRGB::Red;
  }
  FastLED.show();
}

void loop() {
  // read incomming chars from USB Serial Connection
  if(SerialUSB.available()>0) {
    if(SerialUSB.read()=='B') {
      if(SerialUSB.read()=='E') {
        if(SerialUSB.read()=='E') {
          if(SerialUSB.read()=='F') {
            for(int i=0; i<3000; i++) {
              rgbArray[i]=SerialUSB.read();
              if(rgbArray[i]>200)rgbArray[i]=200;// Lichtbremse
            }
            framePass=true;
          }
        }
      }
    }
  }
  //draw frame if fully transmitted
  if(framePass) {
    int k=0;
    for(int i=0; i<NUM_LEDS; i+=2) {
      if(i==392)i=400;
      if(i==792)i=800;
      if(i==1194)i=1200;
      if(i==1586)i=1600;

      if(replacedLedPosition(i)) {
        leds[i] =  CRGB( rgbArray[k]*0.7 ,rgbArray[k+2], rgbArray[k+1]*0.60);
        i--;
        continue;
      } else {
        leds[i]  =  CRGB( rgbArray[k] ,rgbArray[k+1], rgbArray[k+2]);
        leds[i+1]= CRGB( rgbArray[k] ,rgbArray[k+1], rgbArray[k+2]);
      }
      k+=3;
    }
  }
  FastLED.show();
  framePass = false;
}
