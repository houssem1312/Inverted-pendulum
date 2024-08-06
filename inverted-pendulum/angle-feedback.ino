
volatile int temp, counter = 0; // Using 'int' for counter and temp is sufficient

void setup() {
  Serial.begin(9600);

  pinMode(2, INPUT_PULLUP); // Setting pin 2 as input with internal pull-up
  pinMode(3, INPUT_PULLUP); // Setting pin 3 as input with internal pull-up
  
  attachInterrupt(digitalPinToInterrupt(2), ai0, RISING); // Attaching ISR ai0 to interrupt 0 (pin 2)
  attachInterrupt(digitalPinToInterrupt(3), ai1, RISING); // Attaching ISR ai1 to interrupt 1 (pin 3)
}

void loop() {
  // Send the value of counter if it has changed
  if (counter != temp) {
    float degrees = abs(static_cast<float>(counter % 800) * 360.0 / 800.0);
    Serial.println(degrees);
    temp = counter;
  }
}

void ai0() {
  // ISR for interrupt 0 (pin 2), called when pin 2 goes from LOW to HIGH
  // Check pin 3 to determine the direction
  if (digitalRead(3) == LOW) {
    counter++;
  } else {
    counter--;
  }
}

void ai1() {
  // ISR for interrupt 1 (pin 3), called when pin 3 goes from LOW to HIGH
  // Check pin 2 to determine the direction
  if (digitalRead(2) == LOW) {
    counter--;
  } else {
    counter++;
  }
}

