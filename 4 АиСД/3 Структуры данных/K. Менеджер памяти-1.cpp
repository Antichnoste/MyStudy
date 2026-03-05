#include <algorithm>
#include <deque>
#include <iostream>
#include <map>
#include <queue>
#include <stack>
#include <string>
#include <vector>

#define INF 1e9
#define ll long long
#define ui unsigned int

const int MAX_NODES = 2100000;

using namespace std;

ui n;
int m;

struct Node {
  ui max, pref, suff;
  int l_c, r_c;
  signed char busy;
} tree[MAX_NODES];

int nodes_cnt = 1;

int build(ui len) {
  if (nodes_cnt + 1 >= MAX_NODES){
    return 0;
  }
  int v = ++nodes_cnt;
  tree[v].max = tree[v].pref = tree[v].suff = len;
  tree[v].l_c = tree[v].r_c = 0;
  tree[v].busy = -1;
  return v;
}

void apply(int v, ui len, int type) {
  tree[v].busy = (signed char)type;
  tree[v].max = tree[v].pref = tree[v].suff = (type == 1 ? len : 0);
}

void push(int v, ui tl, ui tr) {
  if (tl == tr) {
    return;
  }

  ui mid = tl + (tr - tl) / 2;
  if (!tree[v].l_c) {
    tree[v].l_c = build(mid - tl + 1);
  }
  if (!tree[v].r_c) {
    tree[v].r_c = build(tr - mid);
  }

  if (tree[v].busy != -1) {
    apply(tree[v].l_c, mid - tl + 1, tree[v].busy);
    apply(tree[v].r_c, tr - mid, tree[v].busy);
    tree[v].busy = -1;
  }
}

void recalculate(int v, ui tl, ui tr) {
  ui mid = tl + (tr - tl) / 2;
  int l = tree[v].l_c, r = tree[v].r_c;

  tree[v].pref = tree[l].pref;
  if (tree[l].pref == (mid - tl + 1)) {
    tree[v].pref += tree[r].pref;
  }

  tree[v].suff = tree[r].suff;
  if (tree[r].suff == (tr - mid)) {
    tree[v].suff += tree[l].suff;
  }

  tree[v].max = max({tree[l].max, tree[r].max, tree[l].suff + tree[r].pref});
}

void update(int v, ui tl, ui tr, ui l, ui r, int type) {
  if (l <= tl && tr <= r) {
    apply(v, tr - tl + 1, type);
    return;
  }

  push(v, tl, tr);

  ui mid = tl + (tr - tl) / 2;
  if (l <= mid) {
    update(tree[v].l_c, tl, mid, l, r, type);
  }
  if (r > mid) {
    update(tree[v].r_c, mid + 1, tr, l, r, type);
  }
  recalculate(v, tl, tr);
}

int get_start(int v, ui tl, ui tr, ui k) {
  if (tree[v].max < k) {
    return -1;
  }
  if (tree[v].max == (tr - tl + 1)) {
    return tl;
  }

  push(v, tl, tr);
  ui mid = tl + (tr - tl) / 2;

  if (k <= tree[tree[v].l_c].max) {
    return get_start(tree[v].l_c, tl, mid, k);
  }

  if (k <= tree[tree[v].l_c].suff + tree[tree[v].r_c].pref) {
    return mid - tree[tree[v].l_c].suff + 1;
  }

  return get_start(tree[v].r_c, mid + 1, tr, k);
}

struct Delete {
  ui start, finish;
  bool success = false;
};

int main() {
  cin >> n >> m;
  int cur;

  tree[1].max = tree[1].pref = tree[1].suff = n;
  tree[1].busy = -1;

  vector<Delete> history(m + 1);

  for (int i = 1; i <= m; i++) {
    cin >> cur;
    if (cur > 0) {
      ui k = (ui)cur;
      int res = get_start(1, 1, n, k);
      cout << res << '\n';
      if (res != -1) {
        update(1, 1, n, (ui)res, (ui)res + k - 1, 0);
        history[i] = {(ui)res, (ui)res + k - 1, true};
      }
    } else {
      int idx = -cur;
      if (history[idx].success) {
        update(1, 1, n, history[idx].start, history[idx].finish, 1);
        history[idx].success = false;
      }
    }
  }
}