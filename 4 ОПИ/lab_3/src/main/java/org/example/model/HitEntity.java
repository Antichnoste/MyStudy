package org.example.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

@Getter
@Setter
@Entity
@Table(name = "hit")
public class HitEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private double x;
    @Column(nullable = false)
    private double y;
    @Column(nullable = false)
    private int r;
    @Column(nullable = false)
    private boolean hit;

    @Column(nullable = false)
    private LocalTime createdAt;

    public String formmatedCreatedAt(){
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm:ss");

        return createdAt.format(formatter);
    }
}
