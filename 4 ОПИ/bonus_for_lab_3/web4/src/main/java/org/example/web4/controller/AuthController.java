package org.example.web4.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.example.web4.dto.AuthRequest;
import org.example.web4.dto.AuthResponse;
import org.example.web4.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("api/auth")
@RequiredArgsConstructor
@Tag(name = "Authentication", description = "Регистрация и вход")
public class AuthController {

    private final UserService userService;

    @Operation(
            summary = "Зарегистрировать пользователя",
            security = @SecurityRequirement(name = "none")
    )
    @PostMapping("/register")
    public ResponseEntity<AuthResponse> register(@RequestBody @Valid AuthRequest req) {
        return ResponseEntity.ok(userService.register(req));
    }

    @Operation(
            summary = "Войти в систему",
            security = @SecurityRequirement(name = "none")
    )
    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@RequestBody @Valid AuthRequest req) {
        return ResponseEntity.ok(userService.login(req));
    }
}
