#include <algorithm>
#include <deque>
#include <iostream>
#include <map>
#include <queue>
#include <stack>
#include <string>
#include <vector>

#define INF 1e9
#define ll long long

using namespace std;

int n;
int component = 0;

void dfs(int v, int x, vector<vector<int>>& g, vector<bool>& used) {
  used[v] = true;

  for (int to = 0; to < n; to++) {
    if (!used[to] && g[v][to] <= x) {
      dfs(to, x, g, used);
    }
  }
}

void dfs_revers(int v, int x, vector<vector<int>>& g, vector<bool>& used) {
  used[v] = true;

  for (int from = 0; from < n; from++) {
    if (!used[from] && g[from][v] <= x) {
      dfs_revers(from, x, g, used);
    }
  }
}

bool check(int x, vector<vector<int>>& g) {
  vector<bool> used(n, false);
  dfs(0, x, g, used);
  for (int i = 0; i < n; i++) {
    if (!used[i]) {
      return false;
    }
  }

  for (int i = 0; i < (int)used.size(); i++) {
    used[i] = false;
  }

  dfs_revers(0, x, g, used);
  for (int i = 0; i < n; i++) {
    if (!used[i]) {
      return false;
    }
  }

  return true;
}

void bin_search(ll l, ll r, vector<vector<int>>& g) {
  if (r - l < 2) {
    cout << r;
    return;
  }

  int mid = (l + r) / 2;
  check(mid, g) ? bin_search(l, mid, g) : bin_search(mid, r, g);
}

int main() {
  cin >> n;
  vector<vector<int>> g(n, vector<int>(n, 0));

  ll minim = INF;
  ll maxim = 0;

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      cin >> g[i][j];
      if (i != j) {
        minim = min(minim, (ll)g[i][j]);
        maxim = max(maxim, (ll)g[i][j]);
      }
    }
  }

  bin_search(minim, maxim, g);
}