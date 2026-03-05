#include <iostream>
#include <string>
#include <vector>
#define INF INT_MAX
#define ll long long

using namespace std;

void dfs(int v, vector<vector<int>>& graph, vector<bool>& used) {
  used[v] = true;

  for (int to : graph[v]) {
    if (!used[to]) {
      dfs(to, graph, used);
    }
  }
}

int main() {
  int n;
  cin >> n;

  int component = 0;

  int edge;

  vector<vector<int>> graph(n);
  vector<bool> used(n, false);

  for (int i = 0; i < n; i++) {
    cin >> edge;

    edge--;
    graph[i].push_back(edge);
    graph[edge].push_back(i);
  }

  for (int i = 0; i < n; i++) {
    if (!used[i]) {
      dfs(i, graph, used);
      component++;
    }
  }

  cout << component;
}
