#include <Bridge.h>
#include <HttpClient.h>
const int buttonPin = 2;     // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin

// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status
int lastButtonState = LOW;
int lastAnalogValue = 0;
int brightness;
int analogValue;


void setup() {
  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);
  Bridge.begin();
  Serial.begin(9600); 
}

void loop() {
  // read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);
  // read the state of the analog value
  analogValue = analogRead(A1);
  HttpClient client;
  if (abs(analogValue - lastAnalogValue) > 10) {
    digitalWrite(ledPin, HIGH);
    brightness = map(analogValue, 0, 1023, 0, 255);
    Serial.print(brightness);
    client.get("http://10.1.10.20:8080/allbrightness/" + String(brightness));
    client.get("http://10.1.10.20:8080/toggle");
    lastAnalogValue = analogValue;
    digitalWrite(ledPin, LOW);
  }
  
  // check if the pushbutton is pressed.
  // if it is, the buttonState is HIGH:
  if (buttonState == HIGH && lastButtonState == LOW) {
    // turn LED on:
    digitalWrite(ledPin, HIGH);
    client.get("http://10.1.10.20:8080/toggle");
    lastButtonState == HIGH;
  }
  else if (buttonState == LOW) {
    lastButtonState == LOW;
    digitalWrite(ledPin, LOW);
  }
}
