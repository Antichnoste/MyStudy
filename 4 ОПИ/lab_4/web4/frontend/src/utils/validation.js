const Y_MIN = -3;
const Y_MAX = 5;

export function validateY(yValue) {
  if (yValue === '' || yValue === null || yValue === undefined) {
    return 'Введите значение Y';
  }

  const normalizedY = String(yValue).replace(',', '.');

  if (!/^-?\d+(\.\d+)?$/.test(normalizedY) && normalizedY !== '-') {
    return 'Y должен быть числом';
  }

  const num = parseFloat(normalizedY);

  if (isNaN(num)) {
    return 'Y должен быть числом';
  }

  if (num < Y_MIN || num > Y_MAX) {
    return `Y должен быть в диапазоне от ${Y_MIN} до ${Y_MAX}`;
  }

  return null;
}

export function normalizeInput(value) {
  let rawValue = value.replace(',', '.');

  const startsWithMinus = rawValue.trim().startsWith('-');

  let withoutInvalid = rawValue.replace(/[^0-9.]/g, '');

  const parts = withoutInvalid.split('.');
  let normalized = parts[0];
  if (parts.length > 1) {
    normalized += '.' + parts.slice(1).join('');
  }

  return (startsWithMinus ? '-' : '') + normalized;
}

export function handleInputKeyDown(e) {
  const allowedControlKeys = [
    'Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab', 'Home', 'End', 'Enter'
  ];

  if (e.ctrlKey || e.metaKey || allowedControlKeys.includes(e.key)) {
    return;
  }
  if (!/[\d.,-]/.test(e.key)) {
    e.preventDefault();
    return;
  }

  const { value, selectionStart, selectionEnd } = e.target;

  if (e.key === '-') {
    if (selectionStart !== 0 || (value.includes('-') && selectionStart === selectionEnd)) {
      e.preventDefault();
    }
    return;
  }

  if (e.key === '.' || e.key === ',') {
    const hasSeparator = /[.,]/.test(value);

    if (hasSeparator) {
      const selectedText = value.substring(selectionStart, selectionEnd);
      if (!/[.,]/.test(selectedText)) {
        e.preventDefault();
      }
    }
    return;
  }
}