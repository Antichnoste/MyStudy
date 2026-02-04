#ifdef _WIN32
    #define DLLEXPORT __declspec(dllexport)
#else
    #define DLLEXPORT
#endif

DLLEXPORT long long fib_c(int n) {
    if (n <= 1) return n;
    return fib_c(n - 1) + fib_c(n - 2);
}


DLLEXPORT long long fib_c_iterative(int n) {
    if (n <= 1) return n;
    long long a = 0, b = 1, temp;
    for (int i = 2; i <= n; i++) {
        temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

typedef struct {
    int x;
    int y;
} Point;

DLLEXPORT void process_point(Point* p) {
    p->x *= 10;
    p->y *= 10;
}