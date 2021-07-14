#include <vector>
#include <stdio.h>
#include <iostream>

using namespace std;
typedef signed long long sll;

void solve(vector<sll> & a) {
	sll ans = 0;
	a.insert(a.begin(), 0);
	sll n = a.size();
	for (sll i = 1; i < n; ++i) {
		sll start = (2 * i + a[i] - 1)/a[i];
		start = a[i] * start - i;
		for (sll j = start; j < n; j += a[i]) {
			if (j > i && a[i] * a[j] == i + j) ++ans;
		}
	}
	printf("%lld\n", ans);
}

int main() {
	sll t;
	sll n;
	scanf("%lld", &t);
	while(t--) {
		scanf("%lld", &n);
		vector<sll> a(n);
		for (sll & i : a) scanf("%lld", &i);
		solve(a);
	}
}
