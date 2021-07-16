#include <vector>
#include <iostream>
#include <stack>
#include <limits.h>
#include <unordered_set>

using namespace std;

int solveSlow(vector<int>& nums) {
  int n = nums.size();
  int ans = 0;
  int mx;
  for (int i = 0; i < n; ++i) {
    mx = INT_MIN;
    for (int j = i+1; j < n; ++j) {
      ans += (nums[i] > mx && nums[j] > mx);
      mx = max(mx, nums[j]);
    }
  }
  return ans;
}

int solveFast(vector<int>& nums) {
  if (nums.size() <= 1) return nums.size();
  vector<int> stk;
  int n = nums.size();
  int ans = nums.size()-1;
  for (int i = 0; i < n; ++i) {
    if (!stk.empty() && nums[i] > nums[stk.back()]) stk.pop_back();
    while(!stk.empty() && nums[i] > nums[stk.back()]) {
      stk.pop_back();
      ++ans;
    }
    if (!stk.empty() && stk.back() + 1 < i) ++ans;
    stk.push_back(i);
  }
  return ans;
}

void printans(int s, int f) {
  cout << "slow: " << s << endl;
  cout << "fast: " << f << endl;
}

[[nodiscard]] vector<int> randUnique(int n, int M) {
  unordered_set<int> unique;
  while(unique.size() < n) {
    unique.insert(rand() % M);
  }
  vector<int> ret(unique.begin(), unique.end());
  for (int i = 0; i < n; ++i) {
    swap(ret[i], ret[rand() % (n - i) + i]);
  }
  return ret;
}

int main() {
  
  for (int i = 0; i < 1000; ++i) {
    auto v = randUnique(1000, INT_MAX);
    int s = solveSlow(v);
    int f = solveFast(v);
    if (s != f) {
      for (int i : v) cout << i << ' ';
      cout << endl;
      printans(s, f);
    }
  }
  return 0;
}

