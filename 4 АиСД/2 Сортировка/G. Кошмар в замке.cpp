#include <algorithm>
#include <deque>
#include <iostream>
#include <map>
#include <queue>
#include <stack>
#include <string>
#include <vector>

#define INF INT_MAX
#define ll long long

using namespace std;

struct Letter {
  char letter;
  int weight;
  int cnt;

  Letter() : cnt(0) {
  }

  Letter(int weight, int cnt) : weight(weight), cnt(cnt) {
  }

  bool operator<(const Letter& other) const {
    return weight > other.weight;
  }
};

int main() {
  string s;
  cin >> s;

  vector<Letter> bukovki(26, {-1, 0});

  for (int i = 0; i < (int)s.size(); i++) {
    if (bukovki[s[i] - 'a'].cnt == 0) {
      bukovki[s[i] - 'a'].letter = s[i];
    }

    bukovki[s[i] - 'a'].cnt++;
  }

  for (int i = 0; i < 26; i++) {
    cin >> bukovki[i].weight;
  }

  sort(bukovki.begin(), bukovki.end());

  string begin, mid, end;

  for (int i = 0; i < 26; i++) {
    if (bukovki[i].cnt > 1) {
      begin += bukovki[i].letter;
      bukovki[i].cnt -= 2;

      while (bukovki[i].cnt != 0) {
        mid += bukovki[i].letter;
        bukovki[i].cnt--;
      }

    } else if (bukovki[i].cnt == 1) {
      mid = mid + bukovki[i].letter;
      bukovki[i].cnt--;
    }
  }

  cout << begin + mid;

  for (int i = (int)begin.size() - 1; i >= 0; i--) {
    cout << begin[i];
  }
}