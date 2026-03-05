#include <deque>
#include <iostream>
#include <queue>
#include <stack>
#include <string>
#include <vector>

#define INF INT_MAX
#define ll long long

using namespace std;

bool check(char a, char b) {
  return abs(a - b) == 32;
}

int main() {
  string s;
  cin >> s;

  deque<int> d;
  vector<int> ans((s.size() / 2) + 1, 0);

  vector<int> num_animals(s.size(), -1);
  vector<int> num_traps(s.size(), -1);
  int t = 1, a = 1;

  for (int i = 0; i < (int)s.size(); i++) {
    s[i] < 'a' ? num_traps[i] = t++ : num_animals[i] = a++;
  }

  for (int i = 0; i < (int)s.size(); i++) {
    if (!d.empty() && check(s[d.back()], s[i])) {
      int j = d.back();
      d.pop_back();

      if (s[j] < 'a') {
        ans[num_traps[j]] = num_animals[i];
      } else {
        ans[num_traps[i]] = num_animals[j];
      }
    } else {
      d.push_back(i);
    }
  }

  while (!d.empty()) {
    int front = d.front();
    d.pop_front();
    int back = d.back();
    d.pop_back();

    if (!check(s[front], s[back])) {
      cout << "Impossible";
      return 0;
    }

    if (s[front] < 'a') {
      ans[num_traps[front]] = num_animals[back];
    } else {
      ans[num_traps[back]] = num_animals[front];
    }
  }

  cout << "Possible\n";
  for (int i = 1; i < (int)ans.size(); i++) {
    cout << ans[i] << " ";
  }
}