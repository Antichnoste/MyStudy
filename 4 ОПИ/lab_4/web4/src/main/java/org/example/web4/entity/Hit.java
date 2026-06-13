package org.example.web4.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "hits")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Hit {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private double x; // {-5, -4, -3, -2, -1, 0, 1, 2, 3}
    private double y; // {-3 ... 5} - text
    private int r; // {-5, -4, -3, -2, -1, 0, 1, 2, 3}

    private boolean hit;

    private LocalDateTime createdAt;

    private long executionTimeNs;

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
}
