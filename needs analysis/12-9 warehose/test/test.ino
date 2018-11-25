#define IN1 2
int state = 0;
void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
state = digitalRead(IN1);
if (state == HIGH)
{
  Serial.println("Success");  
}
else
{
 Serial.println("Fail");  
}

if (Serial.available() > 0)
{
int x = Serial.read();
Serial.print("Read  ");
Serial.println(x);  
}


}
