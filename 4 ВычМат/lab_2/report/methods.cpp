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