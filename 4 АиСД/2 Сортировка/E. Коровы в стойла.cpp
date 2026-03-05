#include <deque>
#include <iostream>
#include <queue>
#include <stack>
#include <string>
#include <vector>

#define INF INT_MAX
#define ll long long

using namespace std;

int n, k;
vector<int> mas;

bool check(int dist) {
  int cnt = 1;
  int past = mas[0];

  for (int i = 0; i < (int)mas.size(); i++) {
    if (mas[i] - past >= dist) {
      cnt++;
      past = mas[i];
    }
  }

  return k > cnt;
}

void bin_search(int l, int r) {
  if (r - l < 2) {
    cout << l;
    return;
  }

  int mid = (l + r) / 2;
  check(mid) ? bin_search(l, mid) : bin_search(mid, r);
}

int main() {
  cin >> n >> k;

  for (int i = 0; i < n; i++) {
    int cur;
    cin >> cur;
    mas.push_back(cur);
  }

  bin_search(0, mas[mas.size() - 1] - mas[0] + 1);
}