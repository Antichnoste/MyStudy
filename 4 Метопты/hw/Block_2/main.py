from objective import ProblemConfig
from model.analytics import find_stationary_points_analytic
from model.methods import (
    CoordinateDescentOptimizer,
    GradientDescentOptimizer,
    NewtonOptimizer2D,
    SteepestDescentOptimizer,
)
from model.report import build_report_text, save_report
from model.visualization import plot_contours_with_path


def run_all() -> None:
    cfg = ProblemConfig()

    methods = [
        CoordinateDescentOptimizer(),
        GradientDescentOptimizer(step=0.05),
        SteepestDescentOptimizer(),
    ]

    methods_results = [m.run(cfg.start_point, cfg.eps, cfg.max_iter) for m in methods]

    # ДЗ2.1: отдельный график для каждого метода.
    for r in methods_results:
        safe_name = r.method_name.lower().replace(" ", "_")
        plot_contours_with_path(r, f"outputs/{safe_name}_contours.png")

    # ДЗ2.2: численный Ньютон + аналитические стационарные точки.
    newton = NewtonOptimizer2D()
    newton_result = newton.run(cfg.start_point, cfg.eps, cfg.max_iter)
    plot_contours_with_path(newton_result, "outputs/newton_method_contours.png")
    stationary = find_stationary_points_analytic()

    report_text = build_report_text(methods_results, newton_result, stationary)
    save_report(report_text, "outputs/block_2_report.txt")

    print("Scaffold run complete.")


if __name__ == "__main__":
    run_all()
