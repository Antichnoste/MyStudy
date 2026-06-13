package org.example.web4;

import org.example.web4.dto.HitRequestDto;
import org.example.web4.dto.HitResponseDto;
import org.example.web4.entity.User;
import org.example.web4.repository.HitRepository;
import org.example.web4.repository.UserRepository;
import org.example.web4.service.HitService;
import org.example.web4.support.PostgresIntegrationTest;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
@ActiveProfiles("test")
@Transactional
class HitServiceTest extends PostgresIntegrationTest {

    @Autowired
    private HitService hitService;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private HitRepository hitRepository;

    @Test
    void addHitPersistsDataAndClearRemovesIt() {
        User user = userRepository.save(User.builder()
                .username("bob")
                .passwordHash("hash")
                .createdAt(LocalDateTime.now())
                .build());

        HitRequestDto request = new HitRequestDto(0.5, 0.5, 3);

        HitResponseDto response = hitService.addHit(request, user);

        assertThat(response.getId()).isNotNull();
        assertThat(response.getHit()).isTrue();

        assertThat(hitService.getHits(user))
                .hasSize(1)
                .first()
                .extracting(HitResponseDto::getId)
                .isEqualTo(response.getId());

        hitService.clearHits(user);

        assertThat(hitRepository.findByUserOrderByCreatedAtDesc(user)).isEmpty();
    }
}