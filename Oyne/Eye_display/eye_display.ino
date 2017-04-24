
#include "pinlayout.h"
#include "eyes.h"
int nr = 0;
double refreshrate = 100;//in Hz

void setup() {

  Serial.begin(9600);
  refreshrate = 1000/(refreshrate*8);
  Serial.println(refreshrate);

   for (int i = 2; i <= 17; i++){
      pinMode(i, OUTPUT);
   }

}

void resetLeds(){
  
  for( int i = 0; i < 8; i++){
    digitalWrite(cat[i], HIGH);
    digitalWrite(ano[i], LOW);
  }
}

void showeye(int nr){
  for (int i = 0; i < 8; i++){
    digitalWrite(ano[i], HIGH);
    for (int j = 0; j < 8; j++){
      digitalWrite(cat[j], not(eyes[nr][i][j]));
    }
    delay(refreshrate);
    resetLeds();
  }
}

void loop() {

  if (Serial.available()){
    nr = Serial.read();
    
  }
  showeye(nr);

}



