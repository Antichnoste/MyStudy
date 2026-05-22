#include <array>
#include <cmath>
#include <fstream>
#include <functional>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

constexpr double EpsMin =
    1e-12; // погрешность нужная для устройчивочти алгоритмов (так как мы не можем делит на 0)
constexpr int MaxIters = 200;        // максимальное кол-во итераций для алгоритмов
constexpr int DefaultSamples = 2000; // на какое кол-во точек мы разбиваем интеравал [a,b]
constexpr double ZeroThreshold =
    1e-8; // точность после которой я считаю что значение функции неотличимо от 0 (нельзя
          // использовать EpsMin так как при такой жеской точности я могу пропустить 0, хотя он там
          // уже будет)
constexpr int MaxTauAttempts = 20000; // кол-во попыток для поиска параметра для МПИ для систем
constexpr double AsciiLevelThreshold = 0.03; // толщин границ для графика систем

struct Point {
    double x;
    double y;

    void operator*=(const double val) {
        x *= val;
        y *= val;
    }
};

struct ScalarEquation {
    string name;
    function<double(double)> f;
    function<double(double)> df;
    function<double(double)> d2f;
};

struct SystemDef {
    string name;
    function<Point(const Point&)> f;
    function<array<array<double, 2>, 2>(const Point&)> j;
};

struct ScalarResult {
    bool ok = false;
    string message;
    double root = 0.0;
    double f_at_root = 0.0;
    int iterations = 0;
    double lambda = 0.0;
    double q = 0.0;
};

struct SystemIterRow {
    int k = 0;
    double x = 0.0;
    double y = 0.0;
    double dx = 0.0;
    double dy = 0.0;
    double f1 = 0.0;
    double f2 = 0.0;
};

struct SystemResult {
    bool ok = false;
    string message;
    Point point{0.0, 0.0};
    Point residual{0.0, 0.0};
    int iterations = 0;
    double tau = 0.0;
    double q = 0.0;
    vector<SystemIterRow> rows;
};

vector<ScalarEquation> build_equations() {
    vector<ScalarEquation> eqs;

    eqs.push_back({
        "3x^3 + 1.7x^2 - 15.42x + 6.89",
        [](double x) { return 3.0 * x * x * x + 1.7 * x * x - 15.42 * x + 6.89; },
        [](double x) { return 9.0 * x * x + 3.4 * x - 15.42; },
        [](double x) { return 18.0 * x + 3.4; },
    });

    eqs.push_back({
        "sin(x) - 0.5x",
        [](double x) { return sin(x) - 0.5 * x; },
        [](double x) { return cos(x) - 0.5; },
        [](double x) { return -sin(x); },
    });

    eqs.push_back({
        "exp(-x) - x",
        [](double x) { return exp(-x) - x; },
        [](double x) { return -exp(-x) - 1.0; },
        [](double x) { return exp(-x); },
    });

    eqs.push_back({
        "x^3 - x - 1",
        [](double x) { return x * x * x - x - 1.0; },
        [](double x) { return 3.0 * x * x - 1.0; },
        [](double x) { return 6.0 * x; },
    });

    eqs.push_back({
        "cos(x) - x",
        [](double x) { return cos(x) - x; },
        [](double x) { return -sin(x) - 1.0; },
        [](double x) { return -cos(x); },
    });

    return eqs;
}

vector<SystemDef> build_systems() {
    vector<SystemDef> systems;

    systems.push_back({
        "{ tan(xy) = x^2 ; 0.8x^2 + 2y^2 = 1 }",
        [](const Point& p) {
            return Point{tan(p.x * p.y) - p.x * p.x, 0.8 * p.x * p.x + 2.0 * p.y * p.y - 1.0};
        },
        [](const Point& p) {
            double sec2 = 1.0 / (cos(p.x * p.y) * cos(p.x * p.y));
            return array<array<double, 2>, 2>{
                array<double, 2>{p.y * sec2 - 2.0 * p.x, p.x * sec2},
                array<double, 2>{1.6 * p.x, 4.0 * p.y},
            };
        },
    });

    systems.push_back({
        "{ x^2 + y^2 = 1 ; x - y = 0 }",
        [](const Point& p) { return Point{p.x * p.x + p.y * p.y - 1.0, p.x - p.y}; },
        [](const Point& p) {
            return array<array<double, 2>, 2>{
                array<double, 2>{2.0 * p.x, 2.0 * p.y},
                array<double, 2>{1.0, -1.0},
            };
        },
    });

    systems.push_back({
        "{ sin(x + y) - 1.2x = 0 ; x^2 + y - 1 = 0 }",
        [](const Point& p) { return Point{sin(p.x + p.y) - 1.2 * p.x, p.x * p.x + p.y - 1.0}; },
        [](const Point& p) {
            double c = cos(p.x + p.y);
            return array<array<double, 2>, 2>{
                array<double, 2>{c - 1.2, c},
                array<double, 2>{2.0 * p.x, 1.0},
            };
        },
    });

    return systems;
}

bool read_int(const string& prompt, int& value) {
    cout << prompt;
    string line;
    if (!getline(cin, line)) {
        return false;
    }
    istringstream in(line);
    return (in >> value) ? true : false;
}

bool read_double(const string& prompt, double& value) {
    cout << prompt;
    string line;
    if (!getline(cin, line)) {
        return false;
    }
    istringstream in(line);
    return (in >> value) ? true : false;
}

bool read_interval_and_eps_keyboard(double& a, double& b, double& eps) {
    return read_double("Введите a: ", a) && read_double("Введите b: ", b) &&
           read_double("Введите epsilon: ", eps);
}

bool read_interval_and_eps_file(double& a, double& b, double& eps) {
    cout << "Путь к файлу (формат: a b eps в первой строке): ";
    string path;
    if (!getline(cin, path)) {
        return false;
    }

    ifstream file(path);
    if (!file.is_open()) {
        cout << "Не удалось открыть файл." << endl;
        return false;
    }

    if (!(file >> a >> b >> eps)) {
        cout << "Некорректный формат файла." << endl;
        return false;
    }

    return true;
}

double sign(double val) {
    return (val >= 0.0) ? 1.0 : -1.0;
}

int cnt_roots_on_interval(const function<double(double)>& f, double a, double b,
                          int samples = DefaultSamples) {
    int changes = 0;
    double prev = f(a);
    bool prev_was_zero = fabs(prev) < ZeroThreshold;

    for (int i = 1; i <= samples; i++) {
        double x = a + (b - a) * i / samples;
        double cur = f(x);
        bool cur_is_zero = fabs(cur) < ZeroThreshold;

        if (cur_is_zero && !prev_was_zero) {
            ++changes;
        } else if (!cur_is_zero && !prev_was_zero) {
            if ((prev < 0.0 && cur > 0.0) || (prev > 0.0 && cur < 0.0)) {
                ++changes;
            }
        }

        prev_was_zero = cur_is_zero;
        prev = cur;
    }

    return changes;
}

double max_abs_df(const function<double(double)>& df, double a, double b,
                  int samples = DefaultSamples) {
    double m = 0.0;
    for (int i = 0; i <= samples; i++) {
        double x = a + (b - a) * i / samples;
        m = max(m, fabs(df(x)));
    }
    return m;
}

ScalarResult bisection(const ScalarEquation& eq, double a, double b, double eps) {
    ScalarResult res;
    double fa = eq.f(a);
    double fb = eq.f(b);

    if (fa * fb > 0.0) {
        res.message = "Для метода половинного деления требуется смена знака на [a,b].";
        return res;
    }

    double left = a;
    double right = b;
    double mid = 0.5 * (left + right);
    double fmid = eq.f(mid);

    for (int k = 1; k <= MaxIters; k++) {
        mid = 0.5 * (left + right);
        fmid = eq.f(mid);

        if (fabs(fmid) < eps || fabs(right - left) < eps) {
            res.ok = true;
            res.root = mid;
            res.f_at_root = fmid;
            res.iterations = k;
            res.message = "OK";
            return res;
        }

        if (eq.f(left) * fmid < 0.0) {
            right = mid;
        } else {
            left = mid;
        }
    }

    res.message = "Достигнуто максимальное число итераций.";
    return res;
}

ScalarResult newton_scalar(const ScalarEquation& eq, double a, double b, double eps) {
    ScalarResult res;

    double x = 0.5 * (a + b);
    if (eq.f(a) * eq.d2f(a) > 0.0) {
        x = a;
    } else if (eq.f(b) * eq.d2f(b) > 0.0) {
        x = b;
    }

    for (int k = 1; k <= MaxIters; k++) {
        double dfx = eq.df(x);
        if (fabs(dfx) < EpsMin) {
            res.message = "Производная близка к нулю: метод Ньютона остановлен.";
            return res;
        }

        double x1 = x - eq.f(x) / dfx;
        if (x1 < a || x1 > b) {
            x1 = max(a, min(b, x1));
        }

        if (fabs(x1 - x) < eps || fabs(eq.f(x1)) < eps) {
            res.ok = true;
            res.root = x1;
            res.f_at_root = eq.f(x1);
            res.iterations = k;
            res.message = "OK";
            return res;
        }
        x = x1;
    }

    res.message = "Достигнуто максимальное число итераций.";
    return res;
}

ScalarResult simple_iteration_scalar(const ScalarEquation& eq, double a, double b, double eps) {
    ScalarResult res;

    double max_df = max_abs_df(eq.df, a, b);
    if (max_df < EpsMin) {
        res.message = "max|f'(x)| слишком мал, нельзя выбрать lambda.";
        return res;
    }

    // Находим знак производной на интервале для корректного определения лямбды
    double df_sign = 0.0;
    for (int i = 0; i <= DefaultSamples; i++) {
        double x = a + (b - a) * i / double(DefaultSamples);
        double df_val = eq.df(x);
        if (fabs(df_val) > EpsMin) {
            df_sign = sign(df_val);
            break;
        }
    }

    double lambda = -df_sign / max_df;

    double q = 0.0;
    for (int i = 0; i <= DefaultSamples; i++) {
        double x = a + (b - a) * i / double(DefaultSamples);
        q = max(q, fabs(1.0 + lambda * eq.df(x)));
    }

    res.lambda = lambda;
    res.q = q;

    if (q >= 1.0) {
        res.message = "Условие сходимости простой итерации не выполнено: q >= 1.";
        return res;
    }

    double x = 0.5 * (a + b);
    for (int k = 1; k <= MaxIters; k++) {
        double x1 = x - lambda * eq.f(x);
        if (!isfinite(x1)) {
            res.message = "Итерации разошлись (иррациональное значение).";
            return res;
        }

        if (fabs(x1 - x) < eps || fabs(eq.f(x1)) < eps) {
            res.ok = true;
            res.root = x1;
            res.f_at_root = eq.f(x1);
            res.iterations = k;
            res.message = "OK";
            return res;
        }
        x = x1;
    }

    res.message = "Достигнуто максимальное число итераций.";
    return res;
}

SystemResult simple_iteration_system(const SystemDef& s, Point p0, double eps) {
    SystemResult res;

    array<array<double, 2>, 2> j0 = s.j(p0);
    double norm_inf = max(fabs(j0[0][0]) + fabs(j0[0][1]), fabs(j0[1][0]) + fabs(j0[1][1]));
    double tau = (norm_inf > EpsMin) ? 1.0 / norm_inf : 1.0;
    double q = 2.0;

    for (int t = 0; t < MaxTauAttempts; t++) {
        double a11 = fabs(1.0 - tau * j0[0][0]) + fabs(-tau * j0[0][1]);
        double a22 = fabs(-tau * j0[1][0]) + fabs(1.0 - tau * j0[1][1]);
        q = max(a11, a22);
        if (q <= 1.0) {
            break;
        }
        tau *= 0.5;
    }

    res.tau = tau;
    res.q = q;

    if (q >= 1.0) {
        res.message =
            "Недостаточное условие сходимости для простой итерации системы не выполнено (q >= 1).";
        return res;
    }

    Point p = p0;
    for (int k = 1; k <= MaxIters; k++) {
        Point f = s.f(p);
        Point next = {p.x - tau * f.x, p.y - tau * f.y};

        double dx = next.x - p.x;
        double dy = next.y - p.y;

        res.rows.push_back({k, p.x, p.y, dx, dy, f.x, f.y});

        if (!isfinite(next.x) || !isfinite(next.y)) {
            res.message = "Итерации разошлись (иррациональное значение).";
            return res;
        }

        p = next;
        if (max(fabs(dx), fabs(dy)) < eps) {
            res.ok = true;
            res.point = p;
            res.residual = s.f(p);
            res.iterations = k;
            res.message = "OK";
            return res;
        }
    }

    res.message = "Достигнуто максимальное число итераций.";
    return res;
}

bool ask_yes_no(const string& prompt) {
    cout << prompt << " (y/n): ";
    string line;
    getline(cin, line);
    return !line.empty() && (line[0] == 'y' || line[0] == 'Y');
}

void plot_scalar_ascii(const ScalarEquation& eq, double a, double b, int width = 81,
                       int height = 25) {
    vector<string> canvas(height, string(width, ' '));

    double y_min = numeric_limits<double>::infinity();
    double y_max = -numeric_limits<double>::infinity();
    vector<double> ys(width);

    for (int col = 0; col < width; col++) {
        double x = a + (b - a) * col / (width - 1.0);
        double y = eq.f(x);
        ys[col] = y;
        y_min = min(y_min, y);
        y_max = max(y_max, y);
    }

    if (!isfinite(y_min) || !isfinite(y_max)) {
        cout << "Невозможно построить ASCII-график (нечисловые значения)." << endl;
        return;
    }

    if (fabs(y_max - y_min) < EpsMin) {
        y_max += 1.0;
        y_min -= 1.0;
    }

    // риусем ось X
    int axis_row = -1;
    if (y_min <= 0.0 && 0.0 <= y_max) {
        axis_row = round((y_max - 0.0) / (y_max - y_min) * (height - 1));
        // axis_row = max(0, min(axis_row, height - 1));

        if (0 <= axis_row || axis_row < height) {
            for (int c = 0; c < width; c++) {
                canvas[axis_row][c] = '-';
            }
        }
    }

    // рисуем ось Y
    int axis_col = -1;
    if (a <= 0.0 && 0.0 <= b) {
        axis_col = round((0.0 - a) / (b - a) * (width - 1));
        //axis_col = max(0, min(axis_col, width - 1));

        if (0 <= axis_col && axis_col < width){
            for (int r = 0; r < height; r++) {
                canvas[r][axis_col] = '|';
            }
        }
    }

    if (axis_row >= 0 && axis_col >= 0) {
        canvas[axis_row][axis_col] = '+';
    }

    for (int col = 0; col < width; col++) {
        int row = round((y_max - ys[col]) / (y_max - y_min) * (height - 1));
        row = max(0, min(row, height - 1));
        canvas[row][col] = '*';
    }

    cout << "\nASCII-график f(x) на [" << a << "; " << b << "]\n";
    for (const string& line : canvas) {
        cout << line << '\n';
    }
    cout << "x_min=" << a << ", x_max=" << b << ", y_min=" << y_min << ", y_max=" << y_max << "\n";
    cout << "Обозначения: '*' - график, '-'/'|' - оси\n";
}

void plot_system_ascii(const SystemDef& s, double xmin, double xmax, double ymin, double ymax,
                       int width = 81, int height = 33) {
    vector<string> canvas(height, string(width, ' '));

    const double e1 = AsciiLevelThreshold;
    const double e2 = AsciiLevelThreshold;

    for (int row = 0; row < height; row++) {
        double y = ymax - (ymax - ymin) * row / (height - 1.0);
        for (int col = 0; col < width; col++) {
            double x = xmin + (xmax - xmin) * col / (width - 1.0);
            Point f = s.f(Point{x, y});
            bool on1 = fabs(f.x) < e1;
            bool on2 = fabs(f.y) < e2;

            if (on1 && on2) {
                canvas[row][col] = 'X';
            } else if (on1) {
                canvas[row][col] = '1';
            } else if (on2) {
                canvas[row][col] = '2';
            } else {
                canvas[row][col] = '.';
            }
        }
    }

        // рисуем ось X
    if (ymin <= 0.0 && 0.0 <= ymax) {
        int axis_row = round((ymax - 0.0) / (ymax - ymin) * (height - 1));
        if (0 <= axis_row && axis_row < height) {
            for (int c = 0; c < width; c++) {
                canvas[axis_row][c] = '-';
            }
        }
    }

    // рисуем ось Y
    if (xmin <= 0.0 && 0.0 <= xmax) {
        int axis_col = round((0.0 - xmin) / (xmax - xmin) * (width - 1));
        if (0 <= axis_col && axis_col < width) {
            for (int r = 0; r < height; r++) {
                canvas[r][axis_col] = '|';
            }
        }
    }

    cout << "\nASCII-график системы на области x:[" << xmin << "; " << xmax << "] y:[" << ymin
         << "; " << ymax << "]\n";
    for (const string& line : canvas) {
        cout << line << '\n';
    }
    cout << "Обозначения: '1' -> F1=0, '2' -> F2=0, 'X' -> пересечение\n";
}

void save_answer(const string& text) {
    if (!ask_yes_no("Сохранить результат в файл")) {
        return;
    }

    cout << "Путь к файлу результатов: ";
    string path;
    getline(cin, path);
    ofstream out(path, ios::app);
    if (!out.is_open()) {
        cout << "Не удалось открыть файл для записи." << endl;
        return;
    }
    out << "\n==============================\n";
    out << text;
    cout << "Результат добавлен в " << path << endl;
}

void solve_scalar_ui(const vector<ScalarEquation>& equations) {
    cout << "\n--- Решение нелинейного уравнения ---\n";
    for (size_t i = 0; i < equations.size(); i++) {
        cout << (i + 1) << ") f(x) = " << equations[i].name << '\n';
    }

    int eq_idx = 0;
    if (!read_int("Выберите уравнение [1-5]: ", eq_idx) || eq_idx < 1 ||
        eq_idx > (int)equations.size()) {
        cout << "Некорректный номер уравнения." << endl;
        return;
    }

    cout << "Доступные методы:\n";
    cout << "1) Метод половинного деления\n";
    cout << "3) Метод Ньютона\n";
    cout << "5) Метод простой итерации\n";

    int method = 0;
    if (!read_int("Выберите метод [1/3/5]: ", method) ||
        (method != 1 && method != 3 && method != 5)) {
        cout << "Некорректный номер метода." << endl;
        return;
    }

    cout << "Источник входных данных:\n1) Клавиатура\n2) Файл\n";
    int source = 0;
    if (!read_int("Выберите [1/2]: ", source) || (source != 1 && source != 2)) {
        cout << "Некорректный выбор источника." << endl;
        return;
    }

    double a = 0.0, b = 0.0, eps = 0.0;
    bool ok = (source == 1 ? read_interval_and_eps_keyboard(a, b, eps)
                           : read_interval_and_eps_file(a, b, eps));
    if (!ok) {
        cout << "Не удалось считать входные данные." << endl;
        return;
    }

    if (a >= b || eps <= 0.0) {
        cout << "Требуется a < b и epsilon > 0." << endl;
        return;
    }

    const ScalarEquation& eq = equations[eq_idx - 1];

    int roots_est = cnt_roots_on_interval(eq.f, a, b);
    if (roots_est == 0) {
        cout << "На интервале не обнаружено смены знака (возможны отсутствующие корни)." << endl;
        return;
    }
    if (roots_est > 1) {
        cout << "На интервале обнаружено несколько смен знака (возможно несколько корней): "
             << roots_est << endl;
        cout << "Выберите более узкий интервал изоляции одного корня." << endl;
        return;
    }

    ScalarResult res;
    if (method == 1) {
        res = bisection(eq, a, b, eps);
    } else if (method == 3) {
        res = newton_scalar(eq, a, b, eps);
    } else {
        res = simple_iteration_scalar(eq, a, b, eps);
    }

    ostringstream report;
    report << fixed << setprecision(10);
    report << "Уравнение: " << eq.name << "\n";
    report << "Метод: " << method << "\n";
    report << "Интервал: [" << a << "; " << b << "]\n";
    report << "epsilon: " << eps << "\n";

    if (!res.ok) {
        report << "Статус: ошибка\n";
        report << "Причина: " << res.message << "\n";
    } else {
        report << "Статус: успешно\n";
        report << "Корень: " << res.root << "\n";
        report << "f(корень): " << res.f_at_root << "\n";
        report << "Итераций: " << res.iterations << "\n";

        if (method == 5) {
            report << "lambda: " << res.lambda << "\n";
            report << "q = max|phi'(x)|: " << res.q << "\n";
        }
    }

    cout << "\n" << report.str() << endl;
    save_answer(report.str());

    if (ask_yes_no("Показать ASCII-график функции в терминале")) {
        plot_scalar_ascii(eq, a, b);
    }
}

void solve_system_ui(const vector<SystemDef>& systems) {
    cout << "\n--- Решение системы нелинейных уравнений ---\n";
    for (size_t i = 0; i < systems.size(); ++i) {
        cout << (i + 1) << ") " << systems[i].name << '\n';
    }

    int sys_idx = 0;
    if (!read_int("Выберите систему [1-3]: ", sys_idx) || sys_idx < 1 ||
        sys_idx > (int)systems.size()) {
        cout << "Некорректный номер системы." << endl;
        return;
    }

    const int method = 7;
    cout << "Для систем используется только метод 7: простая итерация.\n";

    double eps = 0.01;
    if (!read_double("Введите epsilon: ", eps) || eps <= 0.0) {
        cout << "Некорректная epsilon." << endl;
        return;
    }

    Point p0;
    if (!read_double("Введите начальное x0: ", p0.x) ||
        !read_double("Введите начальное y0: ", p0.y)) {
        cout << "Не удалось считать начальное приближение." << endl;
        return;
    }

    const SystemDef& s = systems[sys_idx - 1];
    SystemResult res = simple_iteration_system(s, p0, eps);

    ostringstream report;
    report << fixed << setprecision(10);
    report << "Система: " << s.name << "\n";
    report << "Метод: " << method << "\n";
    report << "epsilon: " << eps << "\n";
    report << "Начальное приближение: (" << p0.x << ", " << p0.y << ")\n";

    if (!res.ok) {
        report << "Статус: ошибка\n";
        report << "Причина: " << res.message << "\n";
    } else {
        report << "Статус: успешно\n";
        report << "Решение: x = " << res.point.x << ", y = " << res.point.y << "\n";
        report << "Вектор невязки: (" << res.residual.x << ", " << res.residual.y << ")\n";
        report << "Итераций: " << res.iterations << "\n";

        report << "tau: " << res.tau << "\n";
        report << "q (в точке x0): " << res.q << "\n";

        report << "\nТаблица итераций\n";
        report << "k\tx_k\ty_k\t|dx|\t|dy|\tF1\tF2\n";
        for (const auto& row : res.rows) {
            report << row.k << '\t' << row.x << '\t' << row.y << '\t' << fabs(row.dx) << '\t'
                   << fabs(row.dy) << '\t' << row.f1 << '\t' << row.f2 << '\n';
        }
    }

    cout << "\n" << report.str() << endl;
    save_answer(report.str());

    if (ask_yes_no("Показать ASCII-график системы в терминале")) {
        double xmin = -2.0, xmax = 2.0, ymin = -1.0, ymax = 1.0;
        read_double("xmin (по умолчанию -2.0): ", xmin);
        read_double("xmax (по умолчанию 2.0): ", xmax);
        read_double("ymin (по умолчанию -1.0): ", ymin);
        read_double("ymax (по умолчанию 1.0): ", ymax);
        plot_system_ascii(s, xmin, xmax, ymin, ymax);
    }
}

int main() {
    const vector<ScalarEquation> equations = build_equations();
    const vector<SystemDef> systems = build_systems();

    while (true) {
        cout << "\n========== ЛР2: Нелинейные уравнения/системы ==========" << endl;
        cout << "1) Решить нелинейное уравнение\n";
        cout << "2) Решить систему нелинейных уравнений\n";
        cout << "0) Выход\n";

        int cmd = -1;
        if (!read_int("Ваш выбор: ", cmd)) {
            cout << "Ошибка чтения команды." << endl;
            return 0;
        }

        if (cmd == 0) {
            cout << "Выход." << endl;
            break;
        }

        if (cmd == 1) {
            solve_scalar_ui(equations);
        } else if (cmd == 2) {
            solve_system_ui(systems);
        } else {
            cout << "Неизвестная команда." << endl;
        }
    }

    return 0;
}