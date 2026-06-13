package org.example.web4.repository;

import org.example.web4.entity.Hit;
import org.example.web4.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface HitRepository extends JpaRepository<Hit, Long> {

    List<Hit> findByUserOrderByCreatedAtDesc(User user);

    void deleteByUser(User user);
}
