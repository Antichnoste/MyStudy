#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <map>
#include <set>
#include <queue>
#include <deque>
#include <stack>
#include <math.h>
#include <Windows.h>

#define ll long long
const int INF = 1e9;

using namespace std;

int main() {


	cout << "прооаподап";


	vector <int> r;
	vector <int> inf;
	char a = 0;
	vector <char> start(7, 0);

	for (int i = 1; i <= 7; i++) {
		cin >> start[i - 1];

		if (start[i - 1] - 48 != 0 && start[i - 1] - 48 != 1) {
			cout << "Invalid input";
			return 0;
		}

		if (i && (!(i & (i - 1)))) {
			r.push_back(start[i - 1] - 48);
		}
		else {
			inf.push_back(start[i - 1] - 48);
		}
	}

	int s1 = r[0] ^ inf[0] ^ inf[1] ^ inf[3];
	int s2 = r[1] ^ inf[0] ^ inf[2] ^ inf[3];
	int s3 = r[2] ^ inf[1] ^ inf[2] ^ inf[3];

	int s = s3 * 4 + s2 * 2 + s1;

	if (s == 0) {
		cout << "No errors\n";
		for (int a : inf) {
			cout << a;
		}
	}
	else if (s && (!(s & (s - 1)))) {
		cout << "There are no errors in the information bits\nCorrect sequence: ";
		for (int i : inf) {
			cout << i;
		}
	}
	else {
		cout << "Error in " << s << "th bit\nCorrect sequence: ";
		for (int i = 0; i < 7; i++) {
			if (i + 1 == s) {
				start[i] = (start[i] - 48) ? 48 : 49;
			}

			if (!((i + 1) && (!((i + 1) & i)))) {
				cout << start[i];
			}
		}
	}
}
