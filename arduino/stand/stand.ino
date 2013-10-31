const int RED = 2;
const int GREEN = 4;
const int BUTTON = 6;

boolean _standing = false;
boolean _buttonBeingPressed = false;

void setStanding(boolean standing) {
  _standing = standing;
  digitalWrite(_standing ? RED : GREEN, LOW);
  digitalWrite(_standing ? GREEN : RED, HIGH);
}

void setup() {
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BUTTON, INPUT);
  Serial.begin(9600);
  
  setStanding(false);
}

void loop() {
  if(digitalRead(BUTTON) == HIGH) {
    if(!_buttonBeingPressed) {
      setStanding(!_standing);
      _buttonBeingPressed = true;
    }
  }
  else {
    _buttonBeingPressed = false;
  }
}
