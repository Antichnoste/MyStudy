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

struct Segment_tree {
  struct Node {
    ll value;
    ll l, r;

    Node* parent = nullptr;
    Node* left_child = nullptr;
    Node* right_child = nullptr;

    Node() {
      this->value = 0;
      this->l = -1;
      this->r = INF;
    }

    Node(ll l, ll r) : Node() {
      this->l = l;
      this->r = r;
    }
  };

  ll size;
  Node* root;

  Segment_tree(vector<ll>& a) {
    this->size = a.size();
    this->root = build(a, 0, size - 1, nullptr);
  }

  Node* build(vector<ll>& a, ll l, ll r, Node* parent) {
    Node* node = new Node(l, r);
    node->parent = parent;

    if (l == r) {
      node->value = a[l];
    } else {
      ll mid = (l + r) / 2;
      node->left_child = build(a, l, mid, node);
      node->right_child = build(a, mid + 1, r, node);
      node->value = min(node->left_child->value, node->right_child->value);
    }
    return node;
  }

  ll print(ll l, ll r) { return print(root, l, r); }

  ll print(Node* node, ll l, ll r) {
    if (node == nullptr || r < node->l || node->r < l) {
      return INF;
    }

    if (l <= node->l && node->r <= r) {
      return node->value;
    }

    ll min_left = print(node->left_child, l, r);
    ll min_right = print(node->right_child, l, r);

    return min(min_left, min_right);
  }
};

int main() {
  ll n, k;
  cin >> n >> k;

  vector<ll> mas(n, 0);
  for (int i = 0; i < n; i++) {
    cin >> mas[i];
  }

  Segment_tree tree(mas);

  for (ll i = 0; i < n - k + 1; i++) {
    cout << tree.print(i, i + k - 1) << ' ';
  }
}