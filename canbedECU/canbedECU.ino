#include <same51_can.h>

SAME51_CAN can;

char length[1];
char receivedId[2];

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
  Serial.readBytes(length, sizeof(length));
  byte len = length[0];

  Serial.readBytes(receivedId, sizeof(receivedId));
  byte id1 = receivedId[0];
  byte id2 = receivedId[1];
  int id = (id1 << 8) | (id2);
  
  char receivedChars[len];
  unsigned char buf[len]; 
  Serial.readBytes(receivedChars, sizeof(receivedChars));
  int z = 0;
  int last = len+1;
  for (int i = 0; i < last; i+=1){
    byte ds = receivedChars[i];
    buf[z++] = ds;
  }
  
  can.sendMsgBuf(id, 0, len, buf);
}
