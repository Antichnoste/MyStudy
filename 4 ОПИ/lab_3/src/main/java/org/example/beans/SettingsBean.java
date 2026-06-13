package org.example.beans;

import lombok.Getter;
import lombok.Setter;

import java.util.Arrays;
import java.util.List;

@Getter
@Setter
public class SettingsBean {

    private final List<Double> xOptions = Arrays.asList( -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5 );
    private final List<Integer> rOptions = Arrays.asList( 1, 2, 3, 4, 5 );
    private double yMin = -5;
    private double yMax = 5;
    private int clockPeriodSec = 9;

    private String studentFio = "Караганов Павел";
    private String group = "P3210";
    private String variant = "8765";

}