package org.example.web4.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Getter
@Setter
@AllArgsConstructor
public class AuthRequest {

    @NotBlank (message = "Логин должен что-то содержать")
    private String username;

    @NotBlank (message = "Пароль должен что-то содержать")
    private String password;
}
