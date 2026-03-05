#include <iostream>
#include <map>
#include <stack>
#include <string>
#include <vector>
#define INF INT_MAX
#define ll long long

using namespace std;

bool proigrali = false;

void dfs(int v, int c, vector<vector<int>>& g, vector<int>& color) {
  color[v] = c;
  for (int to : g[v]) {
    if (color[to] == 0) {
      dfs(to, 3 - c, g, color);
    } else if (color[to] == c) {
      proigrali = true;
    }
  }
}

int main() {
  int n, k;
  cin >> n >> k;
  int to, from;

  vector<vector<int>> graph(n);
  vector<int> color(n, 0);

  for (int i = 0; i < k; i++) {
    cin >> from >> to;
    graph[--from].push_back(--to);
    graph[to].push_back(from);
  }

  for (int i = 0; i < n; i++) {
    if (color[i] == 0) {
      dfs(i, 1, graph, color);
    }
  }

  cout << (proigrali ? "NO" : "YES");
}