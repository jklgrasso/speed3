// Arduino nano NHD -- Boost,RPM

#include <Arduino.h>
#include <U8g2lib.h>

// Initialize the display
U8G2_SSD1322_NHD_256X64_2_4W_HW_SPI u8g2(U8G2_R2, /* cs=*/ 10, /* dc=*/ 9, /* reset=*/ 8);

// Add power saving loop?

void setup() {
  u8g2.begin();
  u8g2.setFont(u8g2_font_6x10_tr);
}

// Draw a curved bar
void drawCurvedBar(int centerX, int centerY, int startAngle, int endAngle, int radius, int value, int maxValue) {
  int barEndAngle = startAngle + (endAngle - startAngle) * value / maxValue;

  for (int r = radius; r > radius - 5; r--) { // Bar thickness of 5 pixels
    u8g2.drawArc(centerX, centerY, r, startAngle, barEndAngle);
  }
}

// needs numbers?
int boost(int boostValue, int maxBoost){
  // Bottom hori line
  u8g2.drawLine(169, 63, 191, 63);
  u8g2.drawLine(169, 62, 191, 62);
  // Right line
  u8g2.drawLine(255, 30, 255, 51);
  u8g2.drawLine(254, 30, 254, 51);
  // Top arc line
  u8g2.drawLine(255, 30, 215, 30);
  u8g2.drawLine(255, 31, 215, 31);
  // Top arc
  u8g2.drawArc(212, 75, 45, 60, 116);
  u8g2.drawArc(214, 77, 46, 60, 116);
  // Bottom arc Line
  u8g2.drawLine(255, 50, 215, 50);
  u8g2.drawLine(255, 51, 215, 51);
  // Bottom arc
  u8g2.drawArc(212, 75, 25, 60, 116);
  u8g2.drawArc(213, 76, 25, 60, 116);
  // Text
  u8g2.drawStr(205, 62, "Boost");

  // Dynamic curved bar
  drawCurvedBar(212, 75, 60, 116, 45, boostValue, maxBoost);
}

// needs numbers?
int rpm(int rpmValue, int maxRPM){
    // Bottom hori line
  u8g2.drawLine(49, 63, 71, 63);
  u8g2.drawLine(49, 62, 71, 62);
  // Right line
  u8g2.drawLine(145, 30, 145, 51);
  u8g2.drawLine(144, 30, 144, 51);
  // Top arc line
  u8g2.drawLine(145, 30, 95, 30);
  u8g2.drawLine(145, 31, 95, 31);
  // Top arc
  u8g2.drawArc(92, 75, 45, 60, 116);
  u8g2.drawArc(94, 77, 46, 60, 116);
  // Bottom arc Line
  u8g2.drawLine(145, 50, 95, 50);
  u8g2.drawLine(145, 51, 95, 51);
  // Bottom arc
  u8g2.drawArc(92, 75, 25, 60, 116);
  u8g2.drawArc(93, 76, 25, 60, 116);
  // Text
  u8g2.setFont(u8g2_font_6x10_tr);
  u8g2.drawStr(85, 62, "RPM x1000");

  // Dynamic curved bar
  drawCurvedBar(92, 75, 60, 116, 45, rpmValue, maxRPM);
}

void loop() {
  u8g2.firstPage();
  // I'll have to write a function pull data from the raspi 
  int currentBoost = 15; // Example value for boost
  int maxBoost = 30;     // Maximum boost value

  int currentRPM = 4500; // Example value for RPM
  int maxRPM = 8000;     // Maximum RPM value
  do {
      boost();
      rpm();
  } while (u8g2.nextPage());

  delay(500); // Refresh the bar every 500 ms
}