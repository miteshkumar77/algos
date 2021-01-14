/**
 * Find the lexicographically lowest palindrome string with length s0.length that is 
 * lexicographically larger than s0
 * */

#ifndef LOWESTPALINDROME_CPP
#define LOWESTPALINDROME_CPP

#include <string>

using namespace std;

void increment(string& s, int idx) {
  // Increment a string s starting from
  // a right side starting index idx
  int carry = 1;
  for (; idx >= 0 && carry; --idx) {
    if (s[idx] == 'z') {
      s[idx] = 'a';
    } else {
      ++s[idx];
      carry = 0;
    }
  }
}

string smallestPalindrome(string s0) {
    string tmp = s0;
    int l = 0;
    int r = s0.length() - 1;
    while(l < r) {
      s0[r--] = s0[l++];
    }
    
    // If copying the left side to the right side
    // made an equal or larger string, there is nothing we can
    // do to make the string lexicographically smaller and a palindrome
    // and still larger than the original s0
    if (s0 >= tmp) { 
        return s0;
    }
    
    ++r;
    --l;
    // If the string is even in length, increment the left half starting from 
    // left of center
    // If it is odd in length, increment the left half starting from the center
    if (s0.length() % 2 == 0) {
        increment(s0, l);
    } else {
        increment(s0, l + 1); 
    }
    
    // Copy the left side to the right side of the string
    while(l >= 0) {
        s0[r++] = s0[l--];
    }
    return s0;
}
#endif