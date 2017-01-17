const int readPin = A0;

void setup() {
  // put your setup code here, to run once:
  pinMode(readPin, INPUT);
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  long analogVal = analogRead(readPin);
  analogVal = 5000*analogVal/1023;
  
  Serial.println(analogVal);
  delay(500);
}
