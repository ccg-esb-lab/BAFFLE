/*
    Demo name   : TH02_dev demo
    Usage       : DIGITAL I2C HUMIDITY AND TEMPERATURE SENSOR
    Author      : Oliver Wang from Seeed Studio
    Version     : V0.1
*/

#include <TH02_dev.h>
#include "Arduino.h"
#include "Wire.h"

void setup() {
    Serial.begin(9600);        // start serial for output
    /* Power up,delay 150ms,until voltage is stable */
    delay(150);
    /* Reset HP20x_dev */
    TH02.begin();
    delay(100);
}


void loop() {
    float temper = TH02.ReadTemperature();
    //Serial.println("Temperature: ");
    Serial.print(temper);
    Serial.print("/");

    float humidity = TH02.ReadHumidity();
    Serial.print(humidity);
    Serial.println("\r");
    delay(1000);
}
