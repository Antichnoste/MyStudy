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

bool comp(int a, int b) {
  return a > b;
}

int main() {
  int n, k;
  cin >> n >> k;
  int sum = 0;

  vector<int> mas(n, 0);
  for (int i = 0; i < n; i++) {
    cin >> mas[i];
    sum += mas[i];
  }

  sort(mas.begin(), mas.end(), comp);

  for (int i = k - 1; i < n; i += k) {
    sum -= mas[i];
  }

  cout << sum;
}