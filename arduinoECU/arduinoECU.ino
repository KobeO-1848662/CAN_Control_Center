#include <SPI.h>

#define CAN_2515
// #define CAN_2518FD

// Set SPI CS Pin according to your hardware

#if defined(SEEED_WIO_TERMINAL) && defined(CAN_2518FD)
// For Wio Terminal w/ MCP2518FD RPi Hat：
// Channel 0 SPI_CS Pin: BCM 8
// Channel 1 SPI_CS Pin: BCM 7
// Interupt Pin: BCM25
const int SPI_CS_PIN  = BCM8;
const int CAN_INT_PIN = BCM25;
#else

// For Arduino MCP2515 Hat:
// the cs pin of the version after v1.1 is default to D9
// v0.9b and v1.0 is default D10
const int SPI_CS_PIN = 9;
const int CAN_INT_PIN = 2;
#endif


#ifdef CAN_2518FD
#include "mcp2518fd_can.h"
mcp2518fd CAN(SPI_CS_PIN); // Set CS pin
#endif

#ifdef CAN_2515
#include "mcp2515_can.h"
mcp2515_can CAN(SPI_CS_PIN); // Set CS pin
#endif

char length[1];
char receivedId[2];

void setup() {
    Serial.begin(115200);
    while(!Serial);
    CAN.begin(CAN_500KBPS);
}

void loop() {
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
  
  CAN.sendMsgBuf(id, 0, len, buf);
}
