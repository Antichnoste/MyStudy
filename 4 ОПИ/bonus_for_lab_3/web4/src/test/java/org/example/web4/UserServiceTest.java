package org.example.web4;

import org.example.web4.dto.AuthRequest;
import org.example.web4.dto.AuthResponse;
import org.example.web4.entity.User;
import org.example.web4.repository.UserRepository;
import org.example.web4.service.UserService;
import org.example.web4.support.PostgresIntegrationTest;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
@ActiveProfiles("test")
@Transactional
class UserServiceTest extends PostgresIntegrationTest {

    @Autowired
    private UserService userService;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Test
    void registerPersistsUserAndLoginReturnsToken() {
        AuthRequest request = new AuthRequest("alice", "secret123");

        AuthResponse registerResponse = userService.register(request);

        assertThat(registerResponse.getToken()).isNotBlank();

        User savedUser = userRepository.findByUsername("alice").orElseThrow();
        assertThat(savedUser.getId()).isNotNull();
        assertThat(savedUser.getPasswordHash()).isNotEqualTo("secret123");
        assertThat(passwordEncoder.matches("secret123", savedUser.getPasswordHash())).isTrue();

        AuthResponse loginResponse = userService.login(request);

        assertThat(loginResponse.getToken()).isNotBlank();
    }
}