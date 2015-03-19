/*
 This library is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this library.  If not, see <http://www.gnu.org/licenses/>.
 	  
 */

#include <MeggyJrSimple.h>    // Required code, line 1 of 2.

const byte colorPalette[8] = {
  CustomColor0, Red, Orange, Yellow, Green, Blue, Violet, DimOrange};

byte currentColor = 0;
byte colorChanged = 0;
byte currentBrushPos = 0; // 1 is down, 0 is up

unsigned long lastColorChange = 0;
const int colorChangeDelay = 500;

void setup()                    // run once, when the sketch starts
{
  MeggyJrSimpleSetup();      // Required code, line 2 of 2.

  EditColor(CustomColor0, 2, 2, 1);  // Black

  Serial.begin(115200);

  ClearSlate();
  for(byte i = 0; i < 8; i++) {
    DrawPx(i, 7, colorPalette[i]);
  }
  drawColor(currentColor);  
  DisplaySlate();
}  // End setup()

void drawColor(byte color) {
  for(byte i = 0; i < 8; i++) {
    if(i == color) {
      DrawPx(i, 6, colorPalette[color]);
    } 
    else {
      DrawPx(i, 6, Dark);
    }
  }
}

void drawBrushPos(byte brushPos) {
  for(byte i = 0; i < 8; i++) {
    if(i == currentColor && brushPos) {
      DrawPx(i, 5, colorPalette[currentColor]);
    } 
    else {
      DrawPx(i, 5, Dark);
    }
  }
}

void loop()                     // run over and over again
{
  CheckButtonsPress();   //Check to see which buttons are down that weren't before.

  if(Button_A) {
    currentBrushPos = !currentBrushPos;
    Serial.print("b:");
    Serial.println(currentBrushPos);
    drawBrushPos(currentBrushPos);
  }
  if(Button_B) {
    currentColor++;
    if(currentColor > 7) {
      currentColor = 0;
    }
    colorChanged = 1;
    drawColor(currentColor);
    drawBrushPos(currentBrushPos);
    lastColorChange = millis();
  }

  if(Button_Up) {
    DrawPx(1,4,Blue);
    Serial.println("u");
  } 
  else {
    DrawPx(1,4,Dark);
  }

  if(Button_Down) {
    DrawPx(1,2,Blue);
    Serial.println("d");
  } 
  else {
    DrawPx(1,2,Dark);
  }

  if(Button_Right) {
    DrawPx(2,3,Blue);
    Serial.println("r");
  } 
  else {
    DrawPx(2,3,Dark);
  }

  if(Button_Left) {
    DrawPx(0,3,Blue);
    Serial.println("l");
  } 
  else {
    DrawPx(0,3,Dark);
  }

  if(millis() > lastColorChange + colorChangeDelay && colorChanged) {
    colorChanged = 0;;
    Serial.print("c:");
    Serial.println(currentColor);
  }

  DisplaySlate();      // Write the updated game buffer to the screen.
  delay(30);          // Wait 30 ms
}    




