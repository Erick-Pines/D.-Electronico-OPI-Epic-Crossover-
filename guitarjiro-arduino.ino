int i=0;
bool boton[] = {0, 0, 0, 0, 0};
//bool anterior[] = {0, 0, 0, 0, 0};
bool rasgueo=0;
int leds[] = {17,18,19,12,11,10};
int notas[] = {3,8,7,6,5,2}; //9
void setup() {
  Serial.begin(9600);
  for(int j=0; j<6; j++){
    pinMode(leds[j],OUTPUT);
    pinMode(notas[j],OUTPUT);
  }
}

void decode(int coding){
  if(coding<1) return;
  boton[i]= coding%2;
  if(boton[i++]) rasgueo=1;
  decode(coding/2);
}
void loop() {
  if(Serial.available()>0){
    int coding = Serial.read();
    decode(coding);
    for(int j=0; j<5; j++){
      boton[j]? digitalWrite(leds[j],HIGH) : digitalWrite(leds[j],LOW);
      boton[j]? digitalWrite(notas[j],HIGH) : digitalWrite(notas[j],LOW);
      //anterior[j] = boton[j];
      boton[j]=0;
    }
    /*if(rasgueo) digitalWrite(notas[5],HIGH); 
    else digitalWrite(notas[5],LOW);
    i=0, rasgueo=0;
    //delay(10);
    //digitalWrite(notas[5],LOW);*/
    i=0, rasgueo=0;
  }
  
}
