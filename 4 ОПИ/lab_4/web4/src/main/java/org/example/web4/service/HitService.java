package org.example.web4.service;

import lombok.extern.slf4j.Slf4j;
import org.example.web4.dto.HitRequestDto;
import org.example.web4.dto.HitResponseDto;
import org.example.web4.entity.Hit;
import org.example.web4.entity.User;
import org.example.web4.mapper.HitMapper;
import org.example.web4.repository.HitRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import io.micrometer.core.instrument.DistributionSummary;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Slf4j
@Service
@Transactional
public class HitService {

    private final HitRepository hitRepository;
    private final HitMapper hitMapper;
    private final MeterRegistry meterRegistry;

    private final Counter hitsTotal;
    private final Counter hitsInsideTotal;
    private final Timer addHitTimer;
    private final Map<Long, Long> lastClickTsByUser = new ConcurrentHashMap<>();

    public HitService(HitRepository hitRepository, HitMapper hitMapper, MeterRegistry meterRegistry) {
        this.hitRepository = hitRepository;
        this.hitMapper = hitMapper;
        this.meterRegistry = meterRegistry;

        this.hitsTotal = meterRegistry.counter("app_hits_total", "service", "hitService");
        this.hitsInsideTotal = meterRegistry.counter("app_hits_inside_total", "service", "hitService");
        this.addHitTimer = meterRegistry.timer("app_add_hit_duration_ns", "service", "hitService");
    }

    public HitResponseDto addHit(HitRequestDto dto, User user) {
        long start = System.nanoTime();
        boolean hit = isHit(dto.getX(), dto.getY(), dto.getR());
        long duration = System.nanoTime() - start;

        hitsTotal.increment();
        if (hit) {
            hitsInsideTotal.increment();
        }
        addHitTimer.record(duration, java.util.concurrent.TimeUnit.NANOSECONDS);

        if (user != null && user.getId() != null) {
            String userIdTag = String.valueOf(user.getId());
            String usernameTag = user.getUsername() != null ? user.getUsername() : "unknown";
            meterRegistry.counter("app_user_points_total", "user", userIdTag, "username", usernameTag).increment();

            long nowMs = System.currentTimeMillis();
            Long prev = lastClickTsByUser.put(user.getId(), nowMs);
            if (prev != null) {
                long intervalMs = Math.max(0, nowMs - prev);
                DistributionSummary summary = meterRegistry.summary("app_click_interval_ms", "user", userIdTag, "username", usernameTag);
                summary.record(intervalMs);
            }
        }

        Hit e = Hit.builder()
                .x(dto.getX())
                .y(dto.getY())
                .r(dto.getR())
                .hit(hit)
                .createdAt(LocalDateTime.now())
                .executionTimeNs(duration)
                .user(user)
                .build();

        hitRepository.save(e);
        return hitMapper.toDto(e);
    }

    public List<HitResponseDto> getHits(User user) {
        return hitRepository.findByUserOrderByCreatedAtDesc(user).stream()
                .map(hitMapper::toDto)
                .toList();
    }

    public void clearHits(User user) {
        hitRepository.deleteByUser(user);
    }

     private boolean isHit(double x, double y, double r) {

        log.info("Пришла точка {},{},{}", x,y,r);

        if (r == 0){
            return false;
        }

        if (r < 0){
            return isHit(-x, -y, -r);
        }

        double r_2 = r / 2.0;

        // I четверть (треугольник)
         if (y >= 0 && x >= 0){
             double yLine = -1.0 * x + r_2;
             if (y <= yLine){
                 return true;
             }
         }

         // II четверть (квадрат)
         if (0 <= y && y <= r && -1.0 * r <= x && x <= 0){
             return true;
         }

         // III четверть (четверть круга)
         if (y <= 0 && x <= 0){
             if (x*x + y*y <= r_2 * r_2){
                 return true;
             }
         }

        return false;
    }
}
