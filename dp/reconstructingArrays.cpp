#include <vector>
#include <iostream>

using namespace std;

vector<vector<vector<int>>> dp(55, vector<vector<int>>(105, vector<int>(55, 0)));
vector<vector<vector<int>>> dp2(55, vector<vector<int>>(105, vector<int>(55, 0)));





int main() {
	/*
	 * dp[i][j][k] : number of arrays of length i, with maximum element j, and total cost k
	 *
	 */
	int  Mod = 1e9 + 7;
	int M = 104; int N = 54; int C = 54;
	for (int j = 1; j <= M; ++j) {
		dp[1][j][0] = 1;
		dp2[1][j][0] = j;
	}

	for (int i = 2; i <= N; ++i) {
		for (int j = 1; j <= M; ++j) {
			for (int k = 0; k < i; ++k) {
				dp[i][j][k] = (((j * dp[i-1][j][k]) % Mod) + dp2[i-1][j-1][k-1]) % Mod;
				dp2[i][j][k] = (dp2[i][j-1][k] + dp[i][j][k]) % Mod;
			}
		}
	}

	int Q;
	scanf("%d", &Q);
	vector<int> m(Q), n(Q), cost(Q);
	for (int& i : m) scanf("%d", &i);
	for (int& i : n) scanf("%d", &i);
	for (int& i : cost) scanf("%d", &i);
	for (int i = 0; i < Q; ++i)
		printf("%d\n", dp2[m[i]][n[i]][cost[i]]);
	
	return 0;
}
