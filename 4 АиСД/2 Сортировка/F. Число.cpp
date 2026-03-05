#include <algorithm>
#include <deque>
#include <iostream>
#include <queue>
#include <stack>
#include <string>
#include <vector>

#define INF INT_MAX
#define ll long long

using namespace std;

bool comp(string a, string b) {
  return a + b > b + a;
}

int main() {
  vector<string> mas;
  string cur;

  while (cin >> cur) {
    mas.push_back(cur);
  }

  sort(mas.begin(), mas.end(), comp);

  for (string s : mas) {
    cout << s;
  }
}