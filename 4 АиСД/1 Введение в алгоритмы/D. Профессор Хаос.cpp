#include <iostream>
#include <string>
#include <vector>
#define INF INT_MAX
#define ll long long

using namespace std;

ll a, b, c, d, k;

ll f(ll x) {
  x *= b;
  x -= c;
  if (x < 0) {
    return 0;
  } else if (x > d) {
    return d;
  }

  return x;
}

int main() {
  cin >> a >> b >> c >> d >> k;

  vector<ll> seq;
  vector<int> jumps(d + 1, -1);

  ll cur = a;

  while (jumps[cur] == -1) {
    jumps[cur] = seq.size();
    seq.push_back(cur);

    cur = f(cur);
  }

  int s = jumps[cur];
  int len = seq.size() - s;

  if (k < s) {
    cout << seq[k] << endl;
  } else {
    cout << seq[s + (k - s) % len] << endl;
  }
}