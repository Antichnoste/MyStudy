#include <iostream>
#include <string>
#include <vector>
#define ll long long

using namespace std;

int main() {
  int n;
  cin >> n;

  int best_l = 0, best_r = 0;

  vector<ll> threes;
  threes.push_back(0);

  vector<ll> flowers(n);

  for (int i = 0; i < n; i++) {
    cin >> flowers[i];

    if (i > 1 && flowers[i - 2] == flowers[i - 1] && flowers[i - 1] == flowers[i]) {
      threes.push_back(i - 1);
    }
  }

  threes.push_back(n - 1);

  for (int i = 1; i < (int)threes.size(); i++) {
    if (threes[i] - threes[i - 1] > best_r - best_l) {
      best_l = threes[i - 1];
      best_r = threes[i];
    }
  }

  cout << best_l + 1 << " " << best_r + 1;
}