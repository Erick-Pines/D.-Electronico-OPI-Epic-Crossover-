int i=0;
bool boton[] = {0, 0, 0, 0, 0};
bool anterior[] = {0, 0, 0, 0, 0};
int p=5;
bool rasgueo=0;
int notas[] = {5,6,7,8,11,12};
void setup() {
  Serial.begin(9600);
  for(int j=0; j<6; j++) pinMode(notas[j],OUTPUT);
}

void decode(int coding){
  if(coding<1) return;
  boton[i]= coding%2;
  if(anterior[i]==0 && boton[i++]) rasgueo=1;
  decode(coding/2);
}
void loop() {
  if(Serial.available()>0){
    int coding = Serial.read();
    decode(coding);
    for(int j=0; j<5; j++){
      boton[j]==1? digitalWrite(notas[j],HIGH) : digitalWrite(notas[j],LOW);
      anterior[j] = boton[j];
      boton[j]=0;
    }
    if(rasgueo) digitalWrite(notas[5],HIGH); 
    i=0, rasgueo=0;
    delay(10);
    digitalWrite(notas[5],LOW);
  }
  
}
