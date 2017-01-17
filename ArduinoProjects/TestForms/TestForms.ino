#include "HtmlForms.h"

FormText myText("msg", "my message");
FormRadio myRadio("radio", "radio msg");
FormSubmit mySubmit("Submit", "Submit");

HtmlForm myHtmlForm;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
    myHtmlForm.AddContent(myText);
    myHtmlForm.AddContent(myRadio);
    myHtmlForm.AddContent(mySubmit);
}

void loop() {
  // put your main code here, to run repeatedly:
//  myRadio.PrintHtmlString();
//  myText.PrintHtmlString();
//  mySubmit.PrintHtmlString();
  //myFormContent.PrintValues();
  myHtmlForm.PrintContentHtml();

  delay(1000);
}
