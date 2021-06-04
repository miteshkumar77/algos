#include <bits/stdc++.h>
using namespace std;

/*
Given two arrays of size N each containing the elements 1 to N, find the minimum number of operations needed to transform the second array into the first.

An operation is defined as:
Taking any current value in an array and moving it to the beginning or end.

Example:
Turn Array2 into Array1

Array1 = [4,2,3,1,5,6]
Array2 = [3,1,4,6,5,2]

Returns 3:

Operation 1: Move 2 to beginning.
Array2 = [2,3,1,4,6,5]

Operation 2: Move 4 to beginning.
Array2 = [4,2,3,1,6,5]

Operation 3: Move 6 to end:
Array2 = [4,2,3,1,5,6]
*/

int solve(vector<int>& a1, vector<int>& a2) {
	int n = a1.size();
	unordered_map<int, int> idx;
	for (int i = 0; i < n; ++i) {
		idx[a2[i]] = i;
	}
	int ans = 1;
	int curr = 1;
	for (int i = 1; i < n; ++i) {
		if (idx[a1[i-1]] < idx[a1[i]]) {
			++curr;
		} else {
			curr = 1;
		}
		ans = max(ans, curr);
	}
	return n - ans;
}

int main() {
	vector<int> a1{3,4,1,2,6,5};
	vector<int> a2{4,3,5,1,2,6};
	cout << solve(a1, a2) << endl;
	a1 = vector<int>{4,2,3,1,5,6};
	a2 = vector<int>{3,1,4,6,5,2};
	cout << solve(a1, a2) << endl;
}
