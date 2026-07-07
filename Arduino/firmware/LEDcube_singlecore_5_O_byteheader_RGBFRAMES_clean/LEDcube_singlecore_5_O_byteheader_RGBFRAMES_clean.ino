// we need FastLED v. 3.3.3 or older to be compatible with arduino Due
#include <FastLED.h>

// 8 parallel lanes x 400 LEDs each (WS2811_PORTD below) — FastLED reads all 3200
// even though only 5 lanes are physically populated (ACTIVE_LEDS)
#define NUM_LEDS 3200
#define ACTIVE_LEDS 2000
// This is an array of leds.  One item for each led in your strip.
CRGB leds[NUM_LEDS];

// sized past the 3000 received bytes: strand 5's replaced LEDs make the draw
// loop read ~6 voxels beyond voxel 1000 (into the zeroed tail, shown on
// nonexistent LEDs past the physical strand end)
uint8_t rgbArray[(NUM_LEDS/2)*3];

bool framePass = false;

// USE position_mask_generator.py TO GENERATE BINARY LOOKUP TABLE
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
    0b00000000, 0b00000000, 0b00000000, 0b01100000, 0b00000000, 0b00000000, 0b00000010, 0b00000000,
    0b00000000, 0b00000000, 0b00000000,
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
              rgbArray[i] = min(rgbArray[i], 200); // Limit RGB values to 200
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
    for(int i=0; i<ACTIVE_LEDS; i+=2) {
      switch(i) {
        case 392: i = 400; break;
        case 792: i = 800; break;
        case 1194: i = 1200; break;
        case 1586: i = 1600; break;
      }

      if(replacedLedPosition(i)) {
        leds[i] =  CRGB( rgbArray[k]*0.7 ,rgbArray[k+2], rgbArray[k+1]*0.60);
        i--;
        k+=3;
        continue;
      } else {
        leds[i]  =  CRGB( rgbArray[k] ,rgbArray[k+1], rgbArray[k+2]);
        leds[i+1]= CRGB( rgbArray[k] ,rgbArray[k+1], rgbArray[k+2]);
      }
      k+=3;
    }
    FastLED.show();
  }
  framePass = false;
}
