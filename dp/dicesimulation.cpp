#include <vector>
#include <algorithm>
#include <stdio.h>


using namespace std;


int main() {
	int n;
	int M = 1e9 + 7;
	scanf("%d", &n);
	vector<int> dp(n + 1, -1);
	dp[0] = 1;
	for (int i = 1; i <= n; ++i) {
		for (int j = 1; j <= 6; ++j) {
			if (i - j >= 0 && dp[i-j] != -1) {
				dp[i] = max(dp[i], 0);
				dp[i] += dp[i-j];
				dp[i] %= M;
			}
		}
	}
	printf("%d", dp[n]);
	return 0;
}
