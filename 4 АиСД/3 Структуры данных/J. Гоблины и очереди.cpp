#include <iostream>
#include <map>
#include <stack>
#include <string>
#include <vector>
#define INF INT_MAX
#define ll long long

using namespace std;

deque<int> d1, d2;

void central() {
  if (d1.size() + 1 == d2.size()) {
    d1.push_back(d2.front());
    d2.pop_front();
  }
}

void push_back(int num) {
  d2.push_back(num);
  central();
}

void push_mid(int num) {
  d2.push_front(num);
  central();
}

void pop() {
  cout << d1.front() << '\n';
  d1.pop_front();
  central();
}

int main() {
  int t;
  string s;

  cin >> t;

  for (; t > 0; t--) {
    cin >> s;

    if (s[0] == '+') {
      cin >> s;
      push_back(stoi(s));
    } else if (s[0] == '*') {
      cin >> s;
      push_mid(stoi(s));
    } else {
      pop();
    }
  }
}