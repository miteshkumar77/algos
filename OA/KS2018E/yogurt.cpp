#include <bits/stdc++.h>


using namespace std;


int solve(vector<int> A, int K) {
	priority_queue<int, vector<int>, less<int>> minq(A.begin(), A.end());
	int day = 0;
	int ans = 0;
	while(!minq.empty()) {
		if (minq.top() <= day) {
			minq.pop();
		} else {
			for (int i = 0; !minq.empty() && i < K; ++i) {
				minq.pop();
				++ans;
			}
		}
		++day;
	}
	return ans;
}

int main() {
	int T,N,K,C;
	scanf("%d", &T);
	C = 0;
	while(T--) {
		++C;
		scanf("%d%d", &N, &K);
		vector<int> A(N);
		int j = 0;
		while(N--) scanf("%d", &A[j++]);
		printf("Case #%d: %d\n", C, solve(A, K));
	}
	return 0;
}
