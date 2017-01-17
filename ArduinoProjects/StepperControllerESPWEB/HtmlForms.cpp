#include "HtmlForms.h"

HtmlFormContent::HtmlFormContent(String type, String name, String value)
{
  _type = type;
  _name = name;
  _value = value;
}

void HtmlFormContent::PrintValues()
{
  Serial.print("Type: ");
  Serial.println(_type);
  Serial.print("Name: ");
  Serial.println(_name);
  Serial.print("Value: ");
  Serial.println(_value);
}

HtmlForm::HtmlForm()
{
  
}

HtmlForm::~HtmlForm()
{
  
}

void HtmlForm::AddContent(HtmlFormContent content)
{
  _contentList.push_back(content);
}

void HtmlForm::PrintContentValues()
{
  for (int i = 0; i < _contentList.size(); i++)
  {
    Serial.print("Type: ");
    Serial.println(_contentList[i]._type);
    Serial.print("Name: ");
    Serial.println(_contentList[i]._name);
    Serial.print("Value: ");
    Serial.println(_contentList[i]._value); 
  }
}

