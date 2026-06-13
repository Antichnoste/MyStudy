package org.example.service;

import lombok.Setter;

import java.time.LocalTime;

@Setter
public class CheckResultService {

    private JpaService jpaService;
    private Geometry geometry;

    public void checkAndPersist(double x, double y, int r) {
        //boolean hit = hitCalculator.hit(x, y, r);
        boolean hit = geometry.hit(x,y,r);

        jpaService.insertResult(x, y, r, hit, LocalTime.now());
    }
}
