// fix what chatgpt gave me 

#include <Arduino.h>
#include <U8g2lib.h>

// Initialize the display
U8G2_SSD1322_NHD_256X64_2_4W_HW_SPI u8g2(U8G2_R2, /* cs=*/ 10, /* dc=*/ 9, /* reset=*/ 8);

void setup() {
  u8g2.begin();
  u8g2.setFont(u8g2_font_6x10_tr);
}

// Function to draw the curved part of the bar
void drawCurvedBar(int centerX, int centerY, int startAngle, int endAngle, int radiusOuter, int radiusInner, float value, float maxValue) {
  // Calculate the angle for the current value (based on the arc's total angle range)
  float maxAngle = endAngle - startAngle;
  float valueAngle = (value / maxValue) * maxAngle;  // Proportional angle for the value

  // Draw the curved arc part (up to the value's corresponding angle)
  for (int r = radiusInner; r <= radiusOuter; r++) {
    u8g2.drawArc(centerX, centerY, r, startAngle, startAngle + valueAngle);
  }

  // If the value is larger than the max for the arc, draw the straight line for the remainder
  if (value > maxValue) {
    // Calculate where the arc stops (end of arc)
    int endX = centerX + radiusOuter * cos((startAngle + valueAngle) * 3.14159 / 360.0);
    int endY = centerY + radiusOuter * sin((startAngle + valueAngle) * 3.14159 / 360.0);

    // Draw the straight line starting from the end of the arc
    // Start of the line is at the end of the arc
    for (int i = 0; i < (int)(value - maxValue); i++) {
      // Draw line segments to the end of the gauge
      int x1 = centerX + radiusOuter * cos((startAngle + valueAngle + i) * 3.14159 / 360.0);
      int y1 = centerY + radiusOuter * sin((startAngle + valueAngle + i) * 3.14159 / 360.0);
      int x2 = centerX + radiusOuter * cos((startAngle + valueAngle + i + 1) * 3.14159 / 360.0);
      int y2 = centerY + radiusOuter * sin((startAngle + valueAngle + i + 1) * 3.14159 / 360.0);
      u8g2.drawLine(x1, y1, x2, y2);
    }
  }
}

// Boost gauge
void boost(float boostValue, float maxBoost) {
  // Static layout (same as before)
  u8g2.drawLine(169, 63, 191, 63); // Bottom horizontal line
  u8g2.drawLine(255, 30, 255, 51); // Right vertical line
  u8g2.drawLine(255, 30, 215, 30); // Top horizontal line
  u8g2.drawLine(255, 50, 215, 50); // Bottom arc line
  u8g2.drawArc(212, 75, 45, 60, 116); // Top arc outer
  u8g2.drawArc(212, 75, 25, 60, 116); // Bottom arc inner
  u8g2.drawStr(205, 62, "Boost");    // Label text

  // Dynamic curved bar for boost (start at 60 degrees and end at 116 degrees)
  drawCurvedBar(212, 75, 60, 116, 45, 25, boostValue, maxBoost);
}

// RPM gauge
void rpm(float rpmValue, float maxRPM) {
  // Static layout (same as before)
  u8g2.drawLine(49, 63, 71, 63); // Bottom horizontal line
  u8g2.drawLine(145, 30, 145, 51); // Right vertical line
  u8g2.drawLine(145, 30, 95, 30); // Top horizontal line
  u8g2.drawLine(145, 50, 95, 50); // Bottom arc line
  u8g2.drawArc(92, 75, 45, 60, 116); // Top arc outer
  u8g2.drawArc(92, 75, 25, 60, 116); // Bottom arc inner
  u8g2.drawStr(85, 62, "RPM x1000"); // Label text

  // Dynamic curved bar for RPM (start at 60 degrees and end at 116 degrees)
  drawCurvedBar(92, 75, 60, 116, 45, 25, maxRPM, rpmValue);
}

void loop() {
  //float minBoost = 30.0; // This will be the min psi ex. -8.5psi
  float minBoost = 30.0; // Example value for boost (dynamic input)
  float currentBoost =3.0;     // Maximum boost value

  float minRPM = 0;   // Always start at 0
  float currentRPM = 0.0;   // Example value for RPM (dynamic input)
  float maxRPM = 0.10;       // Maximum RPM value

  u8g2.firstPage();
  do {
    boost(minBoost, currentBoost);
    rpm(minRPM, currentRPM);
  } while (u8g2.nextPage());

  delay(500); // Refresh the bar every 500 ms
}
