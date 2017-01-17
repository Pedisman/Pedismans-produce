#ifndef HTMLFORMS_H
#define HTMLFORMS_H

#include <Arduino.h>
//#include <StandardCplusplus.h> //if adding any of the standard c++ libraries need to add this //For esp8266 nodemcu 1 build we have to exclude this library....
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
protected:
  virtual ~HtmlFormContent(){};
public:
  HtmlFormContent(String type, String name, String value);

  void PrintValues();
};

class HtmlForm
{
  String _action;
  std::vector<HtmlFormContent> _contentList;
public:
  HtmlForm();
  ~HtmlForm();

  void AddContent(HtmlFormContent content);
  void PrintContentValues();
};

#endif //HTMLFORMS_H

