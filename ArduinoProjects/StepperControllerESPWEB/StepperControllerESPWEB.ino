#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include "HtmlForms.h"

HtmlFormContent("text", "name", "Hello");

// Initialize the input state
int powerState = 0;
int dirState = 0;
int stepperState = 0;

// Raw form appearance (helps for visualisation)
String form = 
  "<p>"
  "<center>"
  "<h1>Stepper Controller</h1>"
  "<p>"
  "<img src='https://store.arduino.cc/includes/images/stickers_logo_text.png'<br>"
  "<form action='power'>"
  "Direction<br>"
  "<input type='radio' name='enabled' value='0' checked> On<br>"
  "<input type='radio' name='enabled' value='1'> Off<br>"
  "<input type='submit' value='Set Power'>"
  "</form>"
  "<p>"
  "<form action='direction'>"
  "Direction<br>"
  "<input type='radio' name='dir' value='0' checked> Forward<br>"
  "<input type='radio' name='dir' value='1'> Reverse<br>"
  "<input type='submit' value='Set Direction'>"
  "</form>"
  "<p>"
  "<form action='stepper'>"
  "Type of Stepper<br>"
  "<input type='radio' name='stepperType' value='0' checked> Wave<br>"
  "<input type='radio' name='stepperType' value='1'> Full<br>"
  "<input type='radio' name='stepperType' value='2'> Half<br>"
  "<input type='submit' value='Set Stepper'>"
  "</form>"
  "<p>"
  "<form action='msg'>"
  "Input command<br>"
  "<input type='text' name='msg'><br>"
  "<input type='submit' value='Submit Message'>"
  "</form>";

// Radio state holder functions
String UpdatePower(int state)
{
  String checked1;
  String checked2;

  switch(state)
  {
    case 0:
      checked1 = "checked";
      checked2 = "";
      break;
    case 1:
      checked1 = "";
      checked2 = "checked";
      break;  
  }

  return   "<form action='power'>"
  "Direction<br>"
  "<input type='radio' name='enabled' value='0' " + checked1 + "> On<br>"
  "<input type='radio' name='enabled' value='1' " + checked2 + "> Off<br>"
  "<input type='submit' value='Set Power'>"
  "</form>";
}

String UpdateDirection(int state)
{
  String checked1;
  String checked2;

  switch(state)
  {
    case 0:
      checked1 = "checked";
      checked2 = "";
      break;
    case 1:
      checked1 = "";
      checked2 = "checked";
      break;  
  }

  return   "<form action='direction'>"
  "Direction<br>"
  "<input type='radio' name='dir' value='0' " + checked1 + "> Forward<br>"
  "<input type='radio' name='dir' value='1' " + checked2 + "> Reverse<br>"
  "<input type='submit' value='Set Direction'>"
  "</form>";
}

String UpdateStepper(int state)
{
  String checked1;
  String checked2;
  String checked3;

  switch(state)
  {
    case 0:
      checked1 = "checked";
      checked2 = "";
      checked3 = "";
      break;
    case 1:
      checked1 = "";
      checked2 = "checked";
      checked3 = "";
      break;  
    case 2:
      checked1 = "";
      checked2 = "";
      checked3 = "checked";
      break;
  }

  return   "<form action='stepper'>"
  "Stepper<br>"
  "<input type='radio' name='stepperType' value='0' " + checked1 + "> Wave<br>"
  "<input type='radio' name='stepperType' value='1' " + checked2 + "> Full<br>"
  "<input type='radio' name='stepperType' value='2' " + checked3 + "> Half<br>"
  "<input type='submit' value='Set Stepper'>"
  "</form>";
}


String UpdateForm()
{
  return "<p>"
    "<center>"
    "<h1>Stepper Controller</h1>"
    "<p>"
    "<img src='https://store.arduino.cc/includes/images/stickers_logo_text.png'<br>"
    + UpdatePower(powerState) +
    "<p>"
    + UpdateDirection(dirState) +
    "<p>"
    + UpdateStepper(stepperState) +
    "<p>"
    "<form action='msg'>"
    "Input command<br>"
    "<input type='text' name='msg'><br>"
    "<input type='submit' value='Submit Message'>"
    "</form>";
}

//Define network constants
const char* const ssid = "Tenda_077400";
const char* const password = "3512028atkm";

//Instantiate server class
ESP8266WebServer server(80);

// Define page handler functions

void HandlePower()
{
  powerState = server.arg("enabled").toInt();

  form = UpdateForm();

  server.send(200, "text/html", form);
}

void HandleDirection()
{
  dirState = server.arg("dir").toInt();

  form = UpdateForm();
  
  server.send(200, "text/html", form);
}

void HandleStepper()
{
  stepperState = server.arg("stepperType").toInt();
  
  form = UpdateForm();
  
  server.send(200, "text/html", form);
}

void HandleMsg()
{
  String msg = server.arg("msg");
  msg.trim(); //always remember to strip spaces for comparison
  msg = msg + "!";
  Serial.println(msg);
  
  form = UpdateForm();
  
  server.send(200, "text/html", form);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("");

  // connect to Wifi network
  WiFi.begin(ssid, password);

  // wait for connection print dots to indicate connection attempts
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  // Display network 
  Serial.println("");
  Serial.print("Conneted to: ");
  Serial.println(ssid);
  Serial.print("IP Adress: ");
  Serial.println(WiFi.localIP());

  // Set endpoints for HTTP server
  // These can be written as inline functions
  server.on("/", []()
  {
    server.send(200, "text/html", form);
  });  

  server.on("/power", HandlePower);
  server.on("/direction", HandleDirection);
  server.on("/stepper", HandleStepper);
  server.on("/msg", HandleMsg);

  server.begin();
  Serial.println("HTTP server started"); 
}

void loop() {
  // put your main code here, to run repeatedly:
  server.handleClient();
}
