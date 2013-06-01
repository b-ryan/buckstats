int GREEN = 4;
int RED = 2;

void setup() {
  pinMode(GREEN, OUTPUT);
  pinMode(RED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(GREEN, HIGH);
  digitalWrite(RED, LOW);
  
  delay(500);
  
  digitalWrite(GREEN, LOW);
  digitalWrite(RED, HIGH);
  
  delay(500);
}
