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
const int jogRepeatDelay = 500;
const int jogRepeatInterval = 200;

unsigned long lastButtonPress[6] = {0, 0, 0, 0, 0, 0};
byte previousButtons = 0xff;

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
  CheckButtonsDown();   //Check to see which buttons are down that weren't before.

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


  if(Button_Up && ~(previousButtons) & 4) {
    lastButtonPress[2] = millis();
    DrawPx(1,4,Blue);
    Serial.println("u");
  } else {
    DrawPx(1,4,Dark);
    if(Button_Up && millis() - lastButtonPress[2] > jogRepeatDelay) {
      DrawPx(1,4,Blue);
      Serial.println("u");
      lastButtonPress[2] = millis() + jogRepeatInterval - jogRepeatDelay;
    }
  }

  if(Button_Down && ~(previousButtons) & 8) {
    lastButtonPress[3] = millis();
    DrawPx(1,2,Blue);
    Serial.println("d");
  } else {
    DrawPx(1,2,Dark);
    if(Button_Down && millis() - lastButtonPress[3] > jogRepeatDelay) {
      DrawPx(1,2,Blue);
      Serial.println("d");
      lastButtonPress[3] = millis() + jogRepeatInterval - jogRepeatDelay;
    }
  }

  if(Button_Left  && ~(previousButtons) & 16) {
    lastButtonPress[4] = millis();
    DrawPx(0,3,Blue);
    Serial.println("l");
  } else {
    DrawPx(0,3,Dark);
    if(Button_Left && millis() - lastButtonPress[4] > jogRepeatDelay) {
      DrawPx(0,3,Blue);
      Serial.println("l");
      lastButtonPress[4] = millis() + jogRepeatInterval - jogRepeatDelay;
    }
  }

  if(Button_Right && ~(previousButtons) & 32) {
    lastButtonPress[5] = millis();
    DrawPx(2,3,Blue);
    Serial.println("r");
  } else {
    DrawPx(2,3,Dark);
    if(Button_Right && millis() - lastButtonPress[5] > jogRepeatDelay) {
      DrawPx(2,3,Blue);
      Serial.println("r");
      lastButtonPress[5] = millis() + jogRepeatInterval - jogRepeatDelay;
    }
  }

  if(millis() > lastColorChange + colorUpdateDelay && colorChanged) {
    colorChanged = 0;
    Serial.print("c:");
    Serial.println(currentColor);
  }

  DisplaySlate();      // Write the updated game buffer to the screen.

  previousButtons = Meg.GetButtons();

  delay(30);          // Wait 30 ms
}    




