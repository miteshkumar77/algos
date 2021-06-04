#include <bits/stdc++.h>
using namespace std;

vector<string> split(const string& s, char c) {
	size_t i = 0;
	size_t n = 0;
	size_t tmp;
	vector<string> ret;
	do {
		tmp = s.find(c, i);
		n = tmp == string::npos ? s.length() : tmp;
		ret.push_back(s.substr(i, n - i));
		i = n+1;
	} while(n < s.length());
	return ret;
}

class Solver {

private:
	const function<bool(const array<string, 2>& a, const array<string, 2>& b)> cmp_pq = [](const array<string, 2>& a, const array<string, 2>& b) -> bool {
		if (stoi(a[0]) > stoi(b[0])) return true;
		else if (stoi(a[0]) < stoi(b[0])) return false;
		else {
			return a[1] > b[1];
		}
	};

	const function<bool(const array<string, 4>& a, const array<string, 4>& b)> cmp_top = [](const array<string, 4>& a, const array<string, 4>& b) -> bool {
		if (stoi(a[0]) > stoi(b[0])) return true;
		else if (stoi(a[0]) < stoi(b[0])) return false;
		else {
			return a[1] + ":" + a[2] + ":" + a[3] < b[1] + ":" + b[2] + ":" + b[3];
		}
	};
	
	unordered_map<string, vector<array<string, 2>>> graph;
	bool hasMax = false;
	array<string, 4> curMax;

	void addEdge(string& node, array<string, 2> edge) {
		if (!graph.count(node)) graph[node] = vector<array<string, 2>>();
		bool added = false;
		for (auto& p : graph[node]) {
			if (p[1] == edge[1] && stoi(edge[0]) > stoi(p[0])) {
				added = true;
				p[1] = edge[1];
				break;
			}
		}
		if (!added) graph[node].push_back(edge);
		sort(graph[node].begin(), graph[node].end(), cmp_pq);
		while(graph[node].size() > 2) graph[node].pop_back();
	}
	void setMax(string& node) {
		if (graph[node].size() < 2) return;
		array<string, 4> t1{to_string(stoi(graph[node][0][0]) + stoi(graph[node][1][0])), graph[node][0][1], node, graph[node][1][1]};
		array<string, 4> t2{t1[0], t1[3], t1[2], t1[1]};
		if (!hasMax) curMax = t1;
		hasMax = true;
		if (cmp_top(t1, curMax)) curMax = t1;
		if (cmp_top(t2, curMax)) curMax = t2;
	}

public:
	string seq(string e) {
		auto edge = split(e, ':');
		addEdge(edge[0], {edge[2], edge[1]});
		addEdge(edge[1], {edge[2], edge[0]});
		setMax(edge[0]);
		setMax(edge[1]);
		return hasMax ? curMax[0] + ":" + curMax[1] + ":" + curMax[2] + ":" + curMax[3] : "NONE";
	}
};


bool test(const vector<string>& input, const vector<string>& output) {
	Solver solver;
	vector<string> calc;
	calc.reserve(input.size());
	transform(input.begin(), input.end(),
				    back_inserter(calc),
						[&](const string& inp_elem) { return solver.seq(inp_elem); });
	bool ok = true;
	for (int i = 0; i < input.size(); ++i) {
		if (calc[i] != output[i]) ok = false;
		break;
	}
	for (const string& s : calc) cout << s << ' ';
	cout << endl;
	for (const string& s : output) cout << s << ' ';
	cout << endl;
	return ok;
}


int main() {
	vector<string> i1{"CHI:NYC:719", "NYC:LA:2414", "NYC:SEATTLE:2448", "NYC:HAWAII:4924"};
	vector<string> o1{"NONE", "3133:CHI:NYC:LA", "4862:LA:NYC:SEATTLE", "7372:HAWAII:NYC:SEATTLE"};

	vector<string> i2{"CHI:NYC:3", "LA:SEATTLE:4", "CHI:SEATTLE:7", "LA:SEATTLE:5"};
	vector<string> o2{"NONE", "NONE", "11:CHI:SEATTLE:LA", "12:CHI:SEATTLE:LA"};

	test(i1, o1);
	test(i2, o2);
}




