const int RED = 2;
const int GREEN = 4;
const int BUTTON = 6;

boolean _standing = false;
boolean _buttonBeingPressed = false;

void setStanding(boolean standing) {
  _standing = standing;

  int gVal = _standing ? HIGH : LOW; // value of the green pin
  digitalWrite(GREEN, gVal);
  digitalWrite(RED, (gVal + 1) % 2);

  Serial.println(_standing ? "standing" : "sitting");
}

void setup() {
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BUTTON, INPUT);

  Serial.begin(9600);

  setStanding(false);
}

void loop() {
  boolean standing = digitalRead(BUTTON) == HIGH;
  if(_standing != standing)
    setStanding(standing);
}
