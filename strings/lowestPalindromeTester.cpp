#include <string>
#include <iostream>
#include "lowestPalindrome.cpp"
#include <chrono> 
#define SLEN 500000
#define ITERATIONS 3
#define BRUTEFORCE 0

string randString() {
  string ans;
  ans.reserve(SLEN); 
  while(ans.length() < SLEN) {
    ans.push_back(rand() % 26 + 'a'); 
  }
  return ans;
}

bool checkPal(const string& s) {
  int l = 0; int r = s.length() - 1;
  while(l < r) {
    if (s[l++] != s[r--]) return false;
  }
  return true;
}

string bruteForce(string s) {
  while(!checkPal(s)) {
    increment(s, s.length() - 1); 
  }
  return s;
}

int main() {
  string badString = string('z', SLEN); 
  string random;
  string actual;
  string expected;
  for (int i = 0; i < ITERATIONS; ++i) {
    random = randString();
    if (BRUTEFORCE) {
      while(random == badString) {
        random = randString();
      }
      expected = bruteForce(random); 
      actual = smallestPalindrome(random);
      if (actual != expected) {
        cout << "Expected: " << expected << " but got: " << actual << " for input: " << random << endl;
      } else {
        cout << "Input: " << random << " Result: " << actual << endl;
      }
    } else {
      auto start = chrono::high_resolution_clock::now();
      auto longRes = smallestPalindrome(random);
      auto stop = chrono::high_resolution_clock::now();
      auto duration = chrono::duration_cast<chrono::milliseconds>(stop - start); 
      cout << "time taken ms: " << duration.count() << endl;
      cout << "is palindrome: " << checkPal(longRes) << endl;
    }
  }
  return 0;
}