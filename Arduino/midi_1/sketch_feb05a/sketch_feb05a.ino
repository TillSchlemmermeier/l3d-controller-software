#include <Encoder.h>    // Verwendung der <Encoder.h> Bibliothek 
const int potiPin = A0;
const int CLK = 6;      // Definition der Pins. CLK an D6, DT an D5. 
const int DT = 5;
const int SW = 2;       // Der Switch wird mit Pin D2 Verbunden. ACHTUNG : Verwenden Sie einen interrupt-Pin!
long altePosition = -999;  // Definition der "alten" Position (Diese fiktive alte Position wird benötigt, damit die aktuelle Position später im seriellen Monitor nur dann angezeigt wird, wenn wir den Rotary Head bewegen)
int alterWert = 0;

Encoder meinEncoder(DT,CLK);  // An dieser Stelle wird ein neues Encoder Projekt erstellt. Dabei wird die Verbindung über die zuvor definierten Varibalen (DT und CLK) hergestellt.


void setup()   // Beginn des Setups

{
  Serial.begin(9600); 
    
  pinMode(SW, INPUT);   // Hier wird der Interrupt installiert.
  
  attachInterrupt(digitalPinToInterrupt(SW), Interrupt, CHANGE); // Sobald sich der Status (CHANGE) des Interrupt Pins (SW = D2) ändern, soll der Interrupt Befehl (onInterrupt)ausgeführt werden.
}



void loop()

{


    int neuerWert = analogRead(A0);
    neuerWert >>=5;
    neuerWert <<=5;

    if (neuerWert != alterWert){
      alterWert = neuerWert;
      Serial.print("01:");
      Serial.println(neuerWert);       
    }


  //  delay(10);

}


void Interrupt() // Beginn des Interrupts. Wenn der Rotary Knopf betätigt wird, springt das Programm automatisch an diese Stelle. Nachdem...

{
    long neuePosition = meinEncoder.read();  // Die "neue" Position des Encoders wird definiert. Dabei wird die aktuelle Position des Encoders über die Variable.Befehl() ausgelesen. 

        if (neuePosition != altePosition)  // Sollte die neue Position ungleich der alten (-999) sein (und nur dann!!)...
        {
        altePosition = neuePosition;   
        Serial.print("00:");
        Serial.println(neuePosition);      // ...soll die aktuelle Position im seriellen Monitor ausgegeben werden.
        }

     delay(10);

}
