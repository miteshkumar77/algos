#pragma once
#include <memory>
#include <vector>
#include <string.h>
#include <iostream>

class MyString {
  
private:
  typedef std::vector<char> dtype;
public:
  MyString() : data(std::make_shared<dtype>()) {}
  
  MyString(char * str_literal) {
    size_t len = strlen(str_literal);
    data = std::make_shared<dtype>(str_literal, str_literal + len);
  }

  MyString(MyString& m) {
    data = m.data;
  }

  MyString(MyString&& m) {
    data = m.data;
    m.data.reset();
  }

  void push_back(char c) {
    modify();
    (*data).push_back(c);
  }

  void pop_back() {
    modify();
    (*data).pop_back();
  }

  char at(size_t i) const {
    return (*data).at(i);
  }

  void set(size_t i, char c) {
    modify();
    (*data)[i] = c;
  }

  void swap(MyString& s) {
    MyString tmp(s);
    s.shallow_cpy(data);
    shallow_cpy(tmp.data);
  }

  size_t length() const {
    return (*data).size();
  }

private:

  void modify() {
    if (data.use_count() > 1) {
      deep_cpy(data);
    }
  }

  void deep_cpy(std::shared_ptr<dtype> ndata) {
    // assert(data.use_count() == 1)
    auto n = new std::vector<char>((*ndata).begin(), (*ndata).end());
    data.reset(n);
  }

  void shallow_cpy(std::shared_ptr<dtype> ndata) {
    data = ndata;
  }

  std::shared_ptr<dtype> data;
  friend std::ostream& operator<<(std::ostream& os, const MyString& s);
};



std::ostream& operator<<(std::ostream& os, const MyString& s) {
  int n = s.length();
  for (int i = 0; i < n; ++i) os << s.at(i);
  return os;
}
