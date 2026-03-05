#include <algorithm>
#include <deque>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <stack>
#include <string>
#include <vector>

#define INF 1e9
#define ll long long

using namespace std;

struct Point {
  int x;
  int y;

  Point() {
    this->x = 0;
    this->y = 0;
  }

  Point(int x, int y) {
    this->x = x;
    this->y = y;
  }

  bool operator!=(const Point& o) const {
    return !(x == o.x && y == o.y);
  }

  bool operator==(const Point& o) const {
    return x == o.x && y == o.y;
  }

  bool operator<(const Point& o) const {
    if (x != o.x)
      return x < o.x;
    return y < o.y;
  }

  Point& operator--() {
    --x;
    --y;
    return *this;
  }

  Point operator--(int) {
    Point cur = *this;
    --x;
    --y;
    return cur;
  }
};

int weight(char x) {
  if (x == '.') {
    return 1;
  } else if (x == 'W') {
    return 2;
  } else {
    return INF;
  }
}

int main() {
  int n, m;
  Point s, f;

  cin >> n >> m >> s.x >> s.y >> f.x >> f.y;

  --s;
  --f;

  vector<vector<char>> g(n, vector<char>(m, 0));

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++) {
      cin >> g[i][j];
    }
  }

  vector<vector<int>> d(n, vector<int>(m, INF));
  vector<vector<Point>> p(n, vector<Point>(m, {-1, -1}));
  set<pair<int, Point>> set;

  d[s.x][s.y] = 0;
  set.insert({0, s});

  while (!set.empty()) {
    Point v = (*set.begin()).second;
    set.erase(set.begin());

    if (v == f) {
      break;
    }

    if (v.x - 1 >= 0 &&
        d[v.x][v.y] + weight(g[v.x - 1][v.y]) < d[v.x - 1][v.y]) {  // можно ли идти вверх
      set.erase({d[v.x - 1][v.y], Point(v.x - 1, v.y)});
      d[v.x - 1][v.y] = d[v.x][v.y] + weight(g[v.x - 1][v.y]);
      p[v.x - 1][v.y] = v;
      set.insert({d[v.x - 1][v.y], Point(v.x - 1, v.y)});
    }

    if (v.y + 1 < m &&
        d[v.x][v.y] + weight(g[v.x][v.y + 1]) < d[v.x][v.y + 1]) {  // можно ли идти вправо
      set.erase({d[v.x][v.y + 1], Point(v.x, v.y + 1)});
      d[v.x][v.y + 1] = d[v.x][v.y] + weight(g[v.x][v.y + 1]);
      p[v.x][v.y + 1] = v;
      set.insert({d[v.x][v.y + 1], Point(v.x, v.y + 1)});
    }

    if (v.x + 1 < n &&
        d[v.x][v.y] + weight(g[v.x + 1][v.y]) < d[v.x + 1][v.y]) {  // можно ли идти вниз
      set.erase({d[v.x + 1][v.y], Point(v.x + 1, v.y)});
      d[v.x + 1][v.y] = d[v.x][v.y] + weight(g[v.x + 1][v.y]);
      p[v.x + 1][v.y] = v;
      set.insert({d[v.x + 1][v.y], Point(v.x + 1, v.y)});
    }

    if (v.y - 1 >= 0 &&
        d[v.x][v.y] + weight(g[v.x][v.y - 1]) < d[v.x][v.y - 1]) {  // можно ли идти влево
      set.insert({d[v.x][v.y - 1], Point(v.x, v.y - 1)});
      d[v.x][v.y - 1] = d[v.x][v.y] + weight(g[v.x][v.y - 1]);
      p[v.x][v.y - 1] = v;
      set.insert({d[v.x][v.y - 1], Point(v.x, v.y - 1)});
    }
  }

  if (d[f.x][f.y] == INF) {
    cout << -1;
    return 0;
  } else {
    cout << d[f.x][f.y] << '\n';

    vector<Point> path;
    Point to, from;

    for (Point v = f; v != s; v = p[v.x][v.y]) {
      path.push_back(v);
    }

    path.push_back(s);

    for (int i = (int)path.size() - 1; i > 0; i--) {
      from = path[i];
      to = path[i - 1];

      if (from.y == to.y && from.x - 1 == to.x) {
        cout << 'N';
      } else if (from.x == to.x && from.y + 1 == to.y) {
        cout << 'E';
      } else if (from.y == to.y && from.x + 1 == to.x) {
        cout << 'S';
      } else {
        cout << 'W';
      }
    }
  }
}