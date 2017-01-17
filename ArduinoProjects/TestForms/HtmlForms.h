#ifndef HTMLFORMS_H
#define HTMLFORMS_H

#include <Arduino.h>
#include <StandardCplusplus.h> //if adding any of the standard c++ libraries need to add this
//#include <serstream>
//#include <string>
#include <vector>
//#include <iterator>

class HtmlFormContent
{
friend class HtmlForm;
protected:
  String _type;
  String _name;
  String _value;
  String _htmlString;
public:
  HtmlFormContent(String name, String value);
  virtual ~HtmlFormContent(){};
  virtual void UpdateHtmlString(String, String){};
  void PrintHtmlString()
  {
    Serial.println(_htmlString);
  };
  void PrintValues();
};

class FormText : public HtmlFormContent
{
public:
  FormText(String name, String value) : HtmlFormContent(name, value)
  {
    _type = "text";
    UpdateHtmlString();
  }

  void UpdateHtmlString(String name="", String value="") override;
  
  ~FormText() override {};
};

class FormRadio : public HtmlFormContent
{
  bool _checked;
public:
  FormRadio(String name, String value, bool checked = true) : HtmlFormContent(name, value)
  {
    _type = "radio";
    _checked = checked;
    UpdateHtmlString(checked);
  }

  ~FormRadio() override {};
  void UpdateHtmlString(String name="", String value="") override;
  void UpdateHtmlString(bool checked, String name="", String value="");
};

class FormSubmit : public HtmlFormContent
{
public:
  FormSubmit(String name, String value) : HtmlFormContent(name, value)
  {
    _type = "submit";
    UpdateHtmlString();
  }

  void UpdateHtmlString(String name="", String value="") override;
  
  ~FormSubmit() override {};
};

class HtmlForm
{
  String _action;
  std::vector<HtmlFormContent> _contentList;
public:
  HtmlForm();
  ~HtmlForm();

  void AddContent(HtmlFormContent content);
  void PrintContentHtml();
  void PrintContentValues();
};

#endif //HTMLFORMS_H

