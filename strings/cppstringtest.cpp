#include <vector>
#include <string>
#include "cppstring.h"
#include <iostream>



using namespace std;

int main() {
  
  string A("Hello World");
  string B(A);
  A.push_back('_');
  cout << A << ' ' << B << endl;
  return 0;
}
