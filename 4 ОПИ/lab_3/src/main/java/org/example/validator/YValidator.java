package org.example.validator;

import javax.faces.application.FacesMessage;
import javax.faces.component.UIComponent;
import javax.faces.context.FacesContext;
import javax.faces.validator.Validator;
import javax.faces.validator.ValidatorException;

public class YValidator implements Validator {

    private static final double Y_MIN = -5.0;
    private static final double Y_MAX = 3.0;

    @Override
    public void validate(FacesContext context, UIComponent component, Object value) throws ValidatorException {
        if (value == null) {
            return;
        }

        double y;

        try {
            y = Double.parseDouble(value.toString().replace(',', '.'));
        } catch (Exception e) {
            throw new ValidatorException(new FacesMessage(FacesMessage.SEVERITY_ERROR, "Неверный формат числа Y", null));
        }

        if (y < Y_MIN || y > Y_MAX) {
            throw new ValidatorException(new FacesMessage(FacesMessage.SEVERITY_ERROR,
                    "Y должен быть в диапазоне [" + Y_MIN + "; " + Y_MAX + "]",
                    null));
        }
    }
}
