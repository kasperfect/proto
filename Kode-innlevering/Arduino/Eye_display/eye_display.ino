//Author = Thomas Kaland

#include "pinlayout.h"
#include "eyes.h"
int nr = 0;
int digit = 0;
int serial;
bool mute = true;
double refreshrate = 100;//in Hz
int DisplaySize[] = {5,5};

int NrAno = DisplaySize[1];
int NrCat = DisplaySize[0];

void setup() {

  Serial.begin(115200);
  refreshrate = 1000/(refreshrate*8); //Setter opp en refreshrate på skjermene. Dette er egentlig ikke nødvendig, er bare jeg som geeker litt
  Serial.println(refreshrate);

   for (int i = 2; i <= 19; i++){
      pinMode(i, OUTPUT);
   }

   //start();

}

void start(){ //Dette er egentligt bare for gøy :P Får øynene til å lyse opp linje for linje. 
  for(int i = NrCat-1; i >= 0; i--){
    digitalWrite(cat[i], LOW);
    for (int j = 0; j < NrAno; j++){
      digitalWrite(ano[j], HIGH);
    }
    delay(500);
  }
}

void Blink(){ //Itererer raskt gjennom de tre midterste radene så det ser ut som ROBO 'blinker' eller får litt sånn støy i øynene
  for( int i = 1; i < (NrCat - 1); i++){
    digitalWrite(cat[i], LOW);
    for( int j = 0; j < NrAno; j++){
      digitalWrite(ano[j], HIGH);
    }
    delay(20);
    resetLeds();
  }  
}

void RandomLeds(){ //Itererer gjennom radene og skrur på tilfeldige leds i den randen.
  for( int i = 0; i < NrCat; i++){
    digitalWrite(cat[i], random(0,2));
    for( int j = 0; j < NrAno; j++){
      digitalWrite(ano[j], random(0,2));
    }
    delay(50); //Egen delay så blinkingen ikke blir for rask. 
    resetLeds();
  } 
} 

void resetLeds(){ //Skrur alle leds av og gjør de klare til å bli skrudd på igjen. (Til motsetning til Mute()) 
  
  for( int i = 0; i < NrAno; i++){
    digitalWrite(ano[i], LOW);
  }
  for( int i = 0; i < NrCat; i++){
    digitalWrite(cat[i], HIGH);
  }
}

void showeye(int nr){ //Itererer gjennom hver rad for seg og sjekker listen over øynelayout for å se hvilke leds som skal være på.

  for (int i = 0; i < NrAno; i++){
    digitalWrite(ano[i], HIGH);
    for (int j = 0; j < NrCat; j++){
      digitalWrite(cat[j], not(eyes[nr][j][i])); //Skrur led på hvis eyes listen sier at det punktet skal være på.
    }
    delay(refreshrate);
    resetLeds();
  }
}

int Delay = 2000;
float Time = 0;
bool Ledsoff = true;

void SlowBlink(){ //Får øynene til å blinke av og på.
  if (millis() > (Time + Delay)){ //Teller ned til ett sekund, så skrur den av øynene.
    Time = millis();
    Ledsoff = not(Ledsoff);
  }

  if (Ledsoff){
    delay(1000); // Hvis øynene allerede er av, venter programmet i ett sekund før øynene blir skrudd på igjen.
    Ledsoff = not(Ledsoff);
  }
  
}

void Mute(){ //Setter alle outputs til False så arduinoen ikke bruker strøm på dette om ROBO ikke kjører eller lignende
  for(int i = 2; i <= 19; i++){
    digitalWrite(i, LOW);
  }
}

//////////////////////////////FUNKSJON FOR 7-SEGMENT//////////////////////

int segmentports[] = {16, 13, 14, 15, 19, 18, 17};

void DisplayVolt(int volt){ //Denne funksjonen fungerer egentlig helt likt som funksjonen som viser øynene, bare litt enklere.
  #include "segmentchart.h"

  digitalWrite(segmentports, LOW); //Skrur av alle leds i displayet

  for(int i = 0; i < 7; i++){
    digitalWrite(segmentports[i], segments[volt][i]); //Skrur på de ledsene som skal på ved hvilket tall igølge segmentchart listen.
  }
}



bool slowblink = false;

////////////////////////////////////// HOVEDPROGRAM /////////////////////////////////////

void loop() {

  if (Serial.available()){ //Lagrer info som kommer fra seriell kom hvis dette finnes
    serial = int(Serial.read() - '0');
    //Serial.println(nr);
    if (serial >= 0 and serial < 8){
        Blink();
        nr = serial;
      }

    if (serial == 8){
      slowblink = not(slowblink);
      Time = millis();
    }

    if (serial > 9){
      digit = serial - 49;
      DisplayVolt(digit);
    }

    if (serial == 9){
      mute = not(mute);
    }
    }

  if (not(mute)){ //Hvis øynene ikke skal være av så forsetter programmet med å skrive ut ting til øynene og 7-segment.

    if(random(0,10000) == 0 and not(mute)){
        Blink();
    }
    
    if (slowblink){
        SlowBlink();
    }
  
    if (nr >= 0 and nr <= 5){
        showeye(nr);
    }
    
    if (nr == 6){
      start();
      nr = 7;
    }

    if (nr == 7){
      RandomLeds();
    }
  }

  else{
    Mute();
  }
}



