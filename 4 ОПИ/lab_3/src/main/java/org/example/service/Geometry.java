package org.example.service;

public class Geometry {

    public Geometry() {}

    public boolean hit(double x, double y, int r) {
        if (!(r > 0)) {
            return false;
        }

        final double EPSILON = 1e-12;

        final double rr = r / 2.0;

        final boolean rect = (x <= 0.0) && (x >= -r)
                && (y <= 0.0) && (y >= -r);

        final boolean tri = (x <= 0.0) && (y >= 0.0)
                && (y <= x / 2.0 + r / 2.0 + EPSILON);

        final boolean sec = (x >= 0.0) && (y <= 0.0)
                && (x * x + y * y <= rr * rr + EPSILON);

        return rect || tri || sec;
    }

    //public static boolean hit(double x, double y, int r) {
    //    if (!(r > 0)) {
    //        return false;
    //    }

    //    final double EPSILON = 1e-12;

    //    final double rr = r / 2.0;

    //    final boolean rect = (x <= 0.0) && (x >= -r)
    //            && (y <= 0.0) && (y >= -r);

    //    final boolean tri = (x <= 0.0) && (y >= 0.0)
    //            && (y <= x / 2.0 + r / 2.0 + EPSILON);

    //    final boolean sec = (x >= 0.0) && (y <= 0.0)
    //            && (x * x + y * y <= rr * rr + EPSILON);

    //    return rect || tri || sec;
    //}
}
