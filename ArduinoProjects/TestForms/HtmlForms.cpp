#include "HtmlForms.h"

//////////////////// Html Form Stuff
HtmlFormContent::HtmlFormContent(String name, String value)
{
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

////////////////// Text Form
void FormText::UpdateHtmlString(String name="", String value="")
{
  _name = name == "" ? _name : name;
  _value = name == "" ? _name : name;

  _htmlString = "<input type='submit' name='" + _name + "' value='" + _value + "'>";
}

/////////////////// Radio Form
void FormRadio::UpdateHtmlString(String name="", String value="")
{
  _name = name == "" ? _name : name;
  _value = name == "" ? _name : name;

  _htmlString = "<input type='radio' name='" + _name + "' value='" + _value;
  if (_checked)
  {
    _htmlString = _htmlString + "' checked>";
  }
  else
  {
    _htmlString = _htmlString + "'>";
  }
}

void FormRadio::UpdateHtmlString(bool checked, String name="", String value="")
{
  _name = name == "" ? _name : name;
  _value = name == "" ? _name : name;
  _checked = checked;

  _htmlString = "<input type='radio' name='" + _name + "' value='" + _value;
  if (_checked)
  {
    _htmlString = _htmlString + "' checked>";
  }
  else
  {
    _htmlString = _htmlString + "'>";
  }
}

////////////////// Submit Form
void FormSubmit::UpdateHtmlString(String name="", String value="")
{
  _name = name == "" ? _name : name;
  _value = name == "" ? _name : name;

  _htmlString = "<input type='submit' name='" + _name + "' value='" + _value + "'>";
}

////////////////// Html Form

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

void HtmlForm::PrintContentHtml()
{
  for (int i; i < _contentList.size() ; i++)
  {
    _contentList[i].PrintHtmlString();
  }
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

