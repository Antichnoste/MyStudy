package org.example.web4.dto;

import lombok.*;

import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class HitResponseDto {
    private Long id;
    private Double x;
    private Double y;
    private Double r;
    private Boolean hit;
    private LocalDateTime createdAt;
    private Long executionTimeNs;
}
