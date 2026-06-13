package org.example.beans;

import lombok.Getter;
import lombok.Setter;
import org.example.service.CheckResultService;
import org.example.service.Geometry;
import org.example.service.JpaService;

import java.io.Serial;
import java.io.Serializable;
import java.time.LocalTime;
import java.util.Date;

@Setter
@Getter
public class FormBean implements Serializable {

    private Double x;
    private Double y;
    private Integer r;

    private Double graphX;
    private Double graphY;

    private CheckResultService checkResultService;
    private ResultsBean results;
    private SettingsBean settings;

    public void submit() {
        if (r == null || y == null) return;
        persistAndRefresh(x, y, r);
    }

    public void submitFromGraph() {
        if (graphX == null || graphY == null || r == null || r <= 0) return;
        persistAndRefresh(graphX, graphY, r);
        graphX = null;
        graphY = null;
    }

    private void persistAndRefresh(double px, double py, int pr) {
        checkResultService.checkAndPersist(px, py, pr);

        results.reload();
    }
}
