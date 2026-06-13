package org.example.web4.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.example.web4.dto.HitRequestDto;
import org.example.web4.dto.HitResponseDto;
import org.example.web4.entity.User;
import org.example.web4.service.HitService;
import org.example.web4.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;

import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("api/hits")
@RequiredArgsConstructor
@Tag(name = "Hits", description = "Работа с точками")
public class HitController {

    private final HitService hitService;
    private final UserService userService;

    @Operation(
            summary = "Добавить точку"
    )
    @PostMapping
    public ResponseEntity<HitResponseDto> add(
            @RequestBody @Valid HitRequestDto dto,
            @AuthenticationPrincipal org.springframework.security.core.userdetails.User principal) {

        User user = userService.findByUsername(principal.getUsername());
        return ResponseEntity.ok(hitService.addHit(dto, user));
    }

    @Operation(
            summary = "Получить все точки"
    )
    @GetMapping
    public ResponseEntity<List<HitResponseDto>> list(@AuthenticationPrincipal org.springframework.security.core.userdetails.User principal) {
        User user = userService.findByUsername(principal.getUsername());
        return ResponseEntity.ok(hitService.getHits(user));
    }


    @Operation(
            summary = "Удалить все точки"
    )
    @DeleteMapping
    public ResponseEntity<Void> clear(@AuthenticationPrincipal org.springframework.security.core.userdetails.User principal) {
        User user = userService.findByUsername(principal.getUsername());
        hitService.clearHits(user);
        return ResponseEntity.noContent().build();
    }
}
