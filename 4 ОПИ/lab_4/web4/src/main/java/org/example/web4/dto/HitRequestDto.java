package org.example.web4.dto;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class HitRequestDto {

    @Min(value = -5, message = "X должен быть не меньше -5")
    @Max(value = 3, message = "X должен быть не больше 3")
    private Double x;

    @Min(value = -3, message = "Y должен быть не меньше -3")
    @Max(value = 5, message = "Y должен быть не больше 5")
    private Double y;

    @Min(value = -5, message = "R должен быть не меньше -5")
    @Max(value = 3, message = "R должен быть не больше 3")
    private Integer r;
}
