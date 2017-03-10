//
// For anyone interested, here is the touch-o-matic arcade game code 
// that I demo in the sensors 3 lecture

const bool POLL_RESPONSE = false;

const int LEFT_DIRECT = A0;
const int LEFT_1MEG = A4;
const int RIGHT_DIRECT = A2;
const int RIGHT_1MEG = A5;

const float MEAN_LENGTH = 20;

int calibrationLeft = 0;
int calibrationRight = 0;

// we change between live and waiting state if two players
// are touching.
// we change to waiting state if both players are no longer touching
int stateChangeCounter = 0;

int loopCount = 0;

float meanTotal = 0;
float varianceTotal = 0;
int numSamples = 0;

void calibrateCapacitive()
{
  pinMode(LEFT_DIRECT, INPUT);
  pinMode(LEFT_1MEG, INPUT);
  pinMode(RIGHT_1MEG, INPUT);
  pinMode(RIGHT_DIRECT, INPUT);
  calibrationLeft = readADCTouch(LEFT_DIRECT, 1000);
  calibrationRight = readADCTouch(RIGHT_DIRECT, 1000);
}


void setup() {
  Serial.begin(9600);
  calibrateCapacitive();
}


bool holding = false;
bool validResistance = false;
float mean; // resistance sensor mean
float var; // resistance sensor variance
int leftVal;// left capacitive touch value
int rightVal;// right capacitive touch value

void loop() {
  doCapacitiveSensing(); // capacitive sensing on each sensor
  senseBetweenPlayers(); // resistance sensing between sensors
  //showDebugData(); // uncomment this line to show debug information
  findTwoPeople();
  showTwoPeopleData();
  //
  //

}

int twoPersonAccumulator=0;
void findTwoPeople()
{
  // if someone is holding onto both sensors
  twoPersonAccumulator--;
  if(twoPersonAccumulator<0)twoPersonAccumulator=0;
  if(leftVal>100 && rightVal>100)
  {
    // but there is no contact in the middle
    if(sqrt(var)<100)
    {
      twoPersonAccumulator+=2;
      if(twoPersonAccumulator>16)
      {
        Serial.println("Found two people");
      }     
    }
  }
}

void showTwoPeopleData()
{
  Serial.print(leftVal);
  Serial.print("\t");
  Serial.print(rightVal);
  Serial.print("\t");
  Serial.print(int(sqrt(var)));
  Serial.print("\t");
  Serial.println(twoPersonAccumulator);  

}

void doCapacitiveSensing()
{
  // capacitive sensing
  // no pulldowns, just do single pin capacitive sensing
  pinMode(LEFT_DIRECT, INPUT);
  pinMode(LEFT_1MEG, INPUT);
  pinMode(RIGHT_1MEG, INPUT);
  pinMode(RIGHT_DIRECT, INPUT);
  leftVal = readADCTouch(LEFT_DIRECT, 50) - calibrationLeft;
  rightVal = readADCTouch(RIGHT_DIRECT, 50) - calibrationRight;;

  // if for some reason the calibration occurs
  // when someone is touching the metal,
  // or the capacitance level drifts,
  // this bit will re-center it slowly.
  if (leftVal > 2 && leftVal < 10)
  {
    calibrationLeft += 1;
  } else if (leftVal < -2)
  {
    calibrationLeft -= 1;
  }
  if (rightVal > 2 && rightVal < 10)
  {
    calibrationRight += 1;
  } else if (rightVal < -2)
  {
    calibrationRight -= 1;
  }

  if (leftVal > 100 && rightVal > 100)
  {
    holding = true;
  }
  if (leftVal < 100 && rightVal < 100)
  {
    holding = false;
  }
}


void senseBetweenPlayers()
{
  validResistance = false;
  if (holding)
  {
    pinMode(LEFT_DIRECT, INPUT);
    pinMode(LEFT_1MEG, OUTPUT);
    pinMode(RIGHT_1MEG, OUTPUT);
    pinMode(RIGHT_DIRECT, INPUT);
    digitalWrite(LEFT_1MEG, 0); // pulldown
    digitalWrite(RIGHT_1MEG, 0); //pulldown

    // then 10 times the normal sensing
    for (int repeat = 0; repeat < 10; repeat++)
    {
      {
        pinMode(LEFT_DIRECT, INPUT);
        pinMode(RIGHT_DIRECT, OUTPUT);
        for (int c = 0; c < MEAN_LENGTH / 4; c++)
        {
          digitalWrite(RIGHT_DIRECT, c & 1);
  //        delayMicroseconds(1700);
          float sensorValue = analogRead(LEFT_DIRECT);
          if (numSamples >= MEAN_LENGTH)
          {
            meanTotal = meanTotal * ((float)(MEAN_LENGTH - 1)) / (float)MEAN_LENGTH;
            varianceTotal = varianceTotal * ((float)(MEAN_LENGTH - 1)) / (float)MEAN_LENGTH;
          }
          else
          {
            numSamples += 1;
          }
          varianceTotal += ((float)sensorValue) * ((float)sensorValue);
          meanTotal += (float)sensorValue;
        }
        pinMode(RIGHT_DIRECT, INPUT);
        pinMode(LEFT_DIRECT, OUTPUT);
        for (int c = 0; c < MEAN_LENGTH / 4; c++)
        {
          digitalWrite(LEFT_DIRECT, c & 1);
//          delayMicroseconds(1700);
          float sensorValue = analogRead(RIGHT_DIRECT);
          if (numSamples >= MEAN_LENGTH)
          {
            meanTotal = meanTotal * ((float)(MEAN_LENGTH - 1)) / (float)MEAN_LENGTH;
            varianceTotal = varianceTotal * ((float)(MEAN_LENGTH - 1)) / (float)MEAN_LENGTH;
          }
          else
          {
            numSamples += 1;
          }
          varianceTotal += ((float)sensorValue) * ((float)sensorValue);
          meanTotal += (float)sensorValue;
        }

        if (numSamples >= MEAN_LENGTH)
        {
          mean = meanTotal / MEAN_LENGTH;
          var = (varianceTotal - (MEAN_LENGTH * mean * mean)) / MEAN_LENGTH;
          validResistance = true;
        }
      }
    }
  } 

}

void showDebugData()
{
  if (validResistance)
  {
    if (shouldDisplay())
    {
      Serial.print(int(leftVal));
      Serial.print(" ");
      Serial.print(int(rightVal));
      Serial.print(" ");
      Serial.print(int(mean));
      Serial.print(" ");
      Serial.print(long(var));
      Serial.print(" ");
      Serial.println(int(sqrt(var)));
    }
  } else
  {
    if (shouldDisplay())
    {
      Serial.print(int(leftVal));
      Serial.print(" ");
      Serial.print(int(rightVal));
      Serial.println(" 0 0 0");
    }
  }

}


boolean shouldDisplay()
{
  if (!POLL_RESPONSE)
  {
    return true;
  } else
  {
    int availBytes = Serial.available();
    if (availBytes > 0)
    {
      for (int c = 0; c < availBytes; c++)
      {
        Serial.read();
      }
      return true;
    }
  }
  return false;
}

int readADCTouch(byte ADCChannel, int samples)
{
  long _value = 0;
  for (int _counter = 0; _counter < samples; _counter ++)
  {
    pinMode(ADCChannel, INPUT_PULLUP);

    ADMUX |=   0b11111;
    ADCSRA |= (1 << ADSC); //start conversion
    while (!(ADCSRA & (1 << ADIF))); //wait for conversion to finish
    ADCSRA |= (1 << ADIF); //reset the flag

    pinMode(ADCChannel, INPUT);
    _value += analogRead(ADCChannel);
  }
  return _value / samples;
}




