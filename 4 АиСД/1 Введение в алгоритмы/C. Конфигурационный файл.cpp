#include <iostream>
#include <map>
#include <stack>
#include <string>
#include <vector>
#define INF INT_MAX
#define ll long long

using namespace std;

pair<string, string> parse(string s) {
  string var1, var2;
  bool f = false;

  for (char cur : s) {
    if (cur == '=') {
      f = true;
      continue;
    }

    if (!f) {
      var1 += cur;
    } else {
      var2 += cur;
    }
  }

  return {var1, var2};
}

int main() {
  string cur;
  map<string, stack<string>> variables;
  stack<vector<string>> blocks;
  blocks.push({});

  while (cin >> cur) {
    if (cur == "{") {
      blocks.push({});
    } else if (cur == "}") {
      for (string a : blocks.top()) {
        variables[a].pop();
      }
      blocks.pop();
    } else {
      pair<string, string> res = parse(cur);
      string value;

      if (res.second[0] > '9') {
        if (variables[res.second].empty()) {
          value = "0";
        } else {
          value = variables[res.second].top();
        }

        cout << value + "\n";
      } else {
        value = res.second;
      }

      variables[res.first].push(value);
      blocks.top().push_back(res.first);
    }
  }
}