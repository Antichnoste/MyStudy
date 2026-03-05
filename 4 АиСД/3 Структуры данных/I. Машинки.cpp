#include <algorithm>
#include <deque>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <stack>
#include <string>
#include <unordered_map>
#include <vector>

#define INF 1000000000
#define ll long long

using namespace std;

struct Car {
  int next;
  int val;
  int past;

  bool operator<(const Car& other) const {
    return next < other.next;
  }
};

int main() {
  int n, p, k;
  cin >> n >> k >> p;

  vector<int> parents(n + 1, -1);
  vector<Car> seq(p, {INF, 0, -1});

  for (int i = 0; i < p; i++) {
    cin >> seq[i].val;

    if (parents[seq[i].val] == -1) {
      parents[seq[i].val] = i;
    } else {
      seq[parents[seq[i].val]].next = i;
      seq[i].past = parents[seq[i].val];
      parents[seq[i].val] = i;
    }
  }

  set<Car> floor;
  vector<bool> playing(n + 1, false);
  int ans = 0;

  for (int i = 0; i < p; i++) {
    Car cur = seq[i];

    if (playing[cur.val]) {        // машинка уже на полу и Петя ей уже играет
      floor.erase(seq[cur.past]);  // тут и на слеудующей строке просто обновляем время появления
      floor.insert(cur);
    } else {  // машинки нет, надо узнать что удалить

      // удаляем самую дальнюю машинку (машинку с максимальным next)
      if ((int)floor.size() == k) {
        Car delet = floor.extract(--(floor.end())).value();
        floor.erase(delet);
        playing[delet.val] = false;
      }

      // добовляем текущую машинку
      floor.insert(cur);
      playing[cur.val] = true;

      ans++;
    }
  }

  cout << ans;
}