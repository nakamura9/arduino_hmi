
const int ZESA_ON = 2;
const int GENERATOR_ON = 3;
const int LEVEL_FULL = 4;
const int LEVEL_HALF = 5;
const int LEVEL_LOW =6;
const int TEMPERATURE = 7;
const int COOLANT = 8;

// list of outputs to control
const int START =9;
const int STOP =10;
const int PUMP = 11;



void setup(){
  // list of inputs to monitor

pinMode(ZESA_ON, INPUT);
pinMode(GENERATOR_ON, INPUT);
pinMode(LEVEL_FULL, INPUT);
pinMode(LEVEL_HALF, INPUT);
pinMode(LEVEL_LOW, INPUT);

pinMode(START, OUTPUT);
pinMode(STOP, OUTPUT);
pinMode(PUMP, OUTPUT);
Serial.begin(9600);

}

void loop() {
  // check if in auto mode
  delay(500);
  Serial.println("Gone into auto check");
  manualMode();
}


void autoMode(){
  Serial.println("in auto mode");
  while(1){
      sendParameters();
      delay(200);
      char ch = Serial.read();
      Serial.flush();
      
      if(digitalRead(TEMPERATURE) == 1 || digitalRead(COOLANT) == 1){
      _stop();
      manualMode();
     }
      
      if(ch - '0' == 0){
        manualMode();
      }
      
      if(digitalRead(ZESA_ON != 1)){
      start();
      }else{
        _stop();
      }
      
     if(digitalRead(LEVEL_HALF)!= 1){
        startPump();
      // will implement timer based safeguard on the pump
     }
     if(digitalRead(LEVEL_FULL)){
        stopPump();  
     }
     
  }
    
  }
void manualMode(){
      sendParameters();
      Serial.println("In manual mode");
      _stop();
      stopPump();
      int val;
      while(1){
        delay(500);
        while(1){
        char ch = Serial.read();
        Serial.flush();
        if(isDigit(ch)){
          val = (ch -'0');
          break;
              }
          }
      
      
      switch(val){
        case 1:
          //the integer 1 will start go to auto
          autoMode();
          break;
        case 2:
          //the integer 2 will start the generator manually
          start();
          break;
        case 3:
          //3 stops the generator
          _stop();
          break;
        case 4:
          //4 starts the pump
          startPump();
          break;
        case 5:
          //5 stops the pump
          stopPump();
          break;
        case 6:
          sendParameters();
          break;
        default:
          // if no Serial data 
          Serial.println("NO data transmitted on manual mode");
          break;
                }
            }
        }

void start(){
  if(digitalRead(GENERATOR_ON) == 0){
    digitalWrite(START, HIGH);
    delay(200);
    digitalWrite(START, LOW);
    Serial.println("Generator started");
  }
}

void _stop(){
  if(digitalRead(GENERATOR_ON) == 1){
    digitalWrite(STOP, HIGH);
    delay(500);
    digitalWrite(STOP, LOW);
    Serial.println("Generator stopped");
  }
}

void startPump(){
    digitalWrite(PUMP, HIGH);
    Serial.println("Pump Started");
}

void stopPump(){
    digitalWrite(PUMP, LOW);
    Serial.println("Pump stopped");
  }

int autoCheck(){
  if(Serial.available()){
    while(1){
      char resp = Serial.read();
      Serial.flush();
      if(isDigit(resp)){
          int val = (resp - '0'); 
          Serial.println(val);
          return val;
      }
    }
}
}

void sendParameters(){
    char temp = '0';
    char cool = '0';
    char levl = '0';
    char genr = '0';
    if(digitalRead(TEMPERATURE) == HIGH){
      temp = "1";
    }
    if(digitalRead(COOLANT) == HIGH){
      cool = "1";
    }
    if(digitalRead(LEVEL_LOW) == HIGH){
      levl = "1";
    }
    if(digitalRead(GENERATOR_ON) == HIGH){
      genr = "1";
    }
    Serial.write(temp);
    Serial.write(",");Serial.write(cool);
    Serial.write(",");Serial.write(levl);
    Serial.write(",");Serial.write(genr);
}
