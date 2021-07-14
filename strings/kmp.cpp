#include <vector>
#include <string>
#include <stdio.h>
#include <iostream>

using namespace std;

vector<int> solve(string a, string b) {

	if (a.length() < b.length()) {
		return {};
	}
	int m = b.length();
	vector<int> lpa(m+1, -1);
	int j = 1;
	for (int i = 1; i <= m; ++i) {
		if (b[i-1] == b[j-1]) {
			lpa[i] = j++;
		} else {
			j = 1;
			lpa[i] = 0;
		}
	}
}


int main() {
	
	return 0;
}
