
#define ENCODER_DO_NOT_USE_INTERRUPTS
#include <Encoder.h>

Encoder Enc3(6, 7);
Encoder Enc2(4, 5);
Encoder Enc1(2, 3);

int Enc1_pos = 0;
int Enc2_pos = 0;
int Enc3_pos = 0;

int Enc1_pot = 0;
int Enc2_pot = 0;
int Enc3_pot = 0;

int temp = 0;

void setup() {
  Serial.begin(9600);
}


void loop() {

  // Encoders 
  temp = Enc1.read();
  if (temp > Enc1_pos+4) {
    Enc1_pos += 1;
    Enc1.write(Enc1_pos);
    Serial.print(0);
    Serial.print(0);    
    Serial.println(temp);
   }
   else if (temp < Enc1_pos-4) {
    Enc1_pos -= 1;
    Enc1.write(Enc1_pos);
    Serial.print(0);
    Serial.print(0);    
    Serial.println(temp);
   }

  temp = Enc2.read();
  if (temp > Enc2_pos+4) {
    Enc2_pos += 1;
    Enc2.write(Enc2_pos);
    Serial.print(1);
    Serial.print(0);    
    Serial.println(temp);
   }
   else if (temp < Enc2_pos-4) {
    Enc2_pos -= 1;
    Enc2.write(Enc2_pos);
    Serial.print(1);
    Serial.print(0);    
    Serial.println(temp);
   }

  temp = Enc3.read();
  if (temp > Enc3_pos+4) {
    Enc3_pos += 1;
    Enc3.write(Enc3_pos);
    Serial.print(2);
    Serial.print(0);    
    Serial.println(temp);
   }
   else if (temp < Enc3_pos-4) {
    Enc3_pos -= 1;
    Enc3.write(Enc3_pos);
    Serial.print(2);
    Serial.print(0);    
    Serial.println(temp);
   }

  // Potis
  temp = analogRead(A5)/10.23;
  if (temp != Enc1_pot) {
    Enc1_pot = temp;
    Serial.print(0);
    Serial.print(1);    
    Serial.println(temp);
  }
  temp = analogRead(A6)/10.23;
  if (temp != Enc2_pot) {
    Enc2_pot = temp;
    Serial.print(1);
    Serial.print(1);    
    Serial.println(temp);
  }
  temp = analogRead(A7)/10.23;
  if (temp != Enc3_pot) {
    Enc3_pot = temp;
    Serial.print(2);
    Serial.print(1);    
    Serial.println(temp);
  }  
}
