

## arduino-stm32

https://github.com/rogerclarkmelbourne/Arduino_STM32



## arduino测试代码

### 串口echo

```
// serial echo test
int incomingByte = 0;    // for incoming serial data

void setup() {
    Serial.begin(115200);
}

void loop() {
  // send data only when you receive data:
  if (Serial.available() > 0) {

    // read the incoming byte:
    incomingByte = Serial.read();

    // say what you got:
    Serial.print((char)incomingByte);
  }
```

