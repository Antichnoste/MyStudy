package org.example.web4.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.example.web4.dto.HitRequestDto;
import org.example.web4.dto.HitResponseDto;
import org.example.web4.entity.Hit;
import org.example.web4.entity.User;
import org.example.web4.mapper.HitMapper;
import org.example.web4.repository.HitRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional
public class HitService {

    private final HitRepository hitRepository;
    private final HitMapper hitMapper;

    public HitResponseDto addHit(HitRequestDto dto, User user) {
        long start = System.nanoTime();
        boolean hit = isHit(dto.getX(), dto.getY(), dto.getR());
        long duration = System.nanoTime() - start;

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
