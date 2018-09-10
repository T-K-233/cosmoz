#include <SPI.h>
#include <Ethernet.h>

IPAddress server(192,168,1,66);
IPAddress ip(192,168,1,166);
static byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
static String team_token = "00010205";  // teamcode + password

EthernetClient client;

int timer = 0;

void servoWrite(int pin,int angle){
  int mapper=map(angle, 0, 180, 500, 2480);
  digitalWrite(pin, HIGH);     // 将舵机接口电平至高
  delayMicroseconds(mapper);   // 延时脉宽值的微秒数
  digitalWrite(pin, LOW);      // 将舵机接口电平至低
}

void stop(){
  for(int i=0; i<14; i++) digitalWrite(i, 0);
}

void connect(){
  while(!client.connected()){
    delay(500);
    Ethernet.begin(mac, ip);
    Serial.println("Connecting ...");
    if (client.connect(server, 10001)){
      Serial.println("connected");
      client.print(team_token);
    }
  }
}

void setup() {
  Serial.begin(9600);
  connect();
}

void loop() {
  int commands[4] = {0};
  int index = 0;
  while (client.available()) {
    for(int i=0; i<4; i++){
      commands[i] = client.read();
    }
    switch(commands[0]){
      case 0x01:
        pinMode(commands[1], commands[2]); break;
      case 0x02:
        analogRead(commands[1]); break;
      case 0x03:
        analogWrite(commands[1], commands[2]); break;
      case 0x04:
        digitalRead(commands[1]); break;
      case 0x05:
        digitalWrite(commands[1], commands[2]); break;
      case 0x0c:
        servoWrite(commands[1], commands[2]); break;
      case 0x80:
        stop();
    }
    timer = 0;
  }
  if (!client.connected() || timer > 100000) {
    stop();
    Serial.println("disconnecting.");
    client.stop();
    delay(1000);
    connect();
  }
  client.write(0xff);
  timer ++;
}
