#include <FastLED.h>

// How many leds are in the strip?
#define NUM_LEDS 3200

/*-----( Declare objects )-----*/
/*-----( Declare Variables )-----*/
// This is an array of leds.  One item for each led in your strip.
CRGB leds[NUM_LEDS];

uint8_t brightArray[NUM_LEDS/2];
uint8_t rgbArray[(NUM_LEDS/2)*3];

bool framePass = false;

void setup() {
  // put your setup code here, to run once:
  SerialUSB.begin(230400);
  SerialUSB.setTimeout(50);
  // sanity check delay - allows reprogramming if accidently blowing power w/leds
  delay(2000);
  LEDS.addLeds<WS2811_PORTD,8,RGB>(leds, 400).setCorrection(TypicalLEDStrip);
  leds[390]  = CRGB::Red;
  leds[391] = CRGB::Red;
  leds[790]  = CRGB::Red;
  leds[791] = CRGB::Red;
  leds[1193]  = CRGB::Red;
  leds[1194] = CRGB::Red;
  leds[1594]  = CRGB::Red;
  leds[1595] = CRGB::Red;
  leds[1987]  = CRGB::Red;
  leds[1988] = CRGB::Red;
  
  FastLED.show();  
}

void loop() {
  // put your main code here, to run repeatedly:
  // read incomming chars from USB Serial Connection
  if(SerialUSB.available()>0)
  {
    if(SerialUSB.read()=='B')
    {
      if(SerialUSB.read()=='E')
      {
        if(SerialUSB.read()=='E')
        {
          if(SerialUSB.read()=='F')
          {          
            for(int i=0; i<3000; i++)
            {
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
  if(framePass)
  {
   int k=0;
   int j=0;
   for(int i=0; i<NUM_LEDS; i+=2)
   {
      if(i==392)i=400;
      if(i==792)i=800;
      if(i==1194)i=1200;
      if(i==1596)i=1600;
     
      if(i==19*2 ||i==20*2-1 ||i==30*2-2 ||i==69*2-3||i==70*2-4
        || i==169*2-5 || i==179*2-6 || i==180*2-7 
        || i==200*2 || i==201*2-1|| i==210*2-2 || i==218*2-3 || i==219*2-4 || i==220*2-5
        || i==379*2-6 || i==380*2-7 
        || i==488*2 || i==489*2-1 || i==490*2-2
        || i==500*2-3 || i==580*2-4 || i==599*2-5
        || i==619*2 || i==620*2-1
        || i==779*2-2 || i==780*2-3
        || i==820*2 || i==839*2-1
        || i==910*2-2 || i==919*2-3 || i==920*2-4 || i==930*2-5 || i==931*2-6 || i==960*2-7 || i==979*2-8 || i==980*2-9 || i==990*2-10 )
      {
       leds[i] =  CRGB( rgbArray[k]*0.7 ,rgbArray[k+2], rgbArray[k+1]*0.60);
        i--;
      }
      else
      {
       leds[i]  =  CRGB( rgbArray[k] ,rgbArray[k+1], rgbArray[k+2]);
       leds[i+1]= CRGB( rgbArray[k] ,rgbArray[k+1], rgbArray[k+2]);
        }
      k+=3;          
     }
   }
   FastLED.show();
   framePass = false;
  }
