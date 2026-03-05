//Это задача нужна для теста системы,
//она не идёт в обязательные задачи

#include <iostream>
#include <string>

using namespace std;

int main() {
  int t;
  string s = "";

  cin >> t;

  for (int i = 0; i < t; i++) {
    cin >> s;
    int mid = s.length() / 2;

    if (s.length() % 2 == 1) {
      cout << "NO\n";
    } else {
      bool flag = true;
      for (int k = 0; 2 * k < (int)s.length(); k++) {
        if (s[k] != s[mid + k]) {
          cout << "NO\n";
          flag = false;
          break;
        }
      }

      if (flag) {
        cout << "YES\n";
      }
    }
  }
}