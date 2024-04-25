#include <same51_can.h>

SAME51_CAN can;

const byte numChars = 20;
char receivedChars[numChars];
unsigned char buf[8];

void setup()
{
  Serial.begin(115200);
  while(!Serial);
    
  uint8_t ret;
  ret = can.begin(MCP_ANY, CAN_500KBPS, MCAN_MODE_CAN);
}

void loop()
{
  // put your main code here, to run repeatedly: 
  while(!Serial.available());
  Serial.readBytes(receivedChars, sizeof(receivedChars));

  byte a = digit_to_binary(receivedChars[0]);
  byte b = digit_to_binary(receivedChars[1]);
  byte c = digit_to_binary(receivedChars[2]);

  int id = a * 256 + b * 16 + c;

  int z = 0;
  for (int i = 4; i < 21; i+=2){
    byte A = digit_to_binary(receivedChars[i]);
    byte B = digit_to_binary(receivedChars[i+1]);
    byte ds = A * 16 + B;

    buf[z++] = ds;
  }

  can.sendMsgBuf(id, 0, 8, buf);
}

byte digit_to_binary(char a){
  if ( 'A' <= a && a <= 'F') {
    return a - 'A' + 10;
  } else if ( 'a' <= a && a <= 'f') {
    return a - 'a' + 10;
  } else if ( '0' <= a && a <= '9') {
    return a - '0';
  } else {
    return a=0;
  } 
}