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

void setup() {
    Serial.begin(115200);
    while(!Serial);
    CAN.begin(CAN_500KBPS);
}

void loop() {
  // put your main code here, to run repeatedly: 
  while(!Serial.available());
  Serial.readBytes(length, sizeof(length));
  int len = digit_to_binary(length[0]);

  char receivedChars[3+2*len];
  unsigned char buf[len];
  Serial.readBytes(receivedChars, sizeof(receivedChars));

  byte a = digit_to_binary(receivedChars[0]);
  byte b = digit_to_binary(receivedChars[1]);
  byte c = digit_to_binary(receivedChars[2]);

  int id = a * 256 + b * 16 + c;

  int z = 0;
  int last = 3+(2*len)+1;
  for (int i = 3; i < last; i+=2){
    byte A = digit_to_binary(receivedChars[i]);
    byte B = digit_to_binary(receivedChars[i+1]);
    byte ds = A * 16 + B;

    buf[z++] = ds;

  }
  CAN.MCP_CAN::sendMsgBuf(id, 0, len, buf);
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