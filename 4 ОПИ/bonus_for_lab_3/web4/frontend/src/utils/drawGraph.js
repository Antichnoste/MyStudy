const COLORS = {
    bg: 'white',
    axis: 'black',
    text: 'black',
    shape: '#3b82f6',
    pointHit: '#22c55e',
    pointMiss: '#ef4444',
    pointBorder: '#333'
};

export const MAX_VALUE = 6;

const drawBackground = (ctx, width, height) => {
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = COLORS.bg;
    ctx.fillRect(0, 0, width, height);
};

const drawAxes = (ctx, width, height, padding, centerX, centerY) => {
    ctx.strokeStyle = COLORS.axis;
    ctx.lineWidth = 2;


    ctx.beginPath();
    ctx.moveTo(padding, centerY);
    ctx.lineTo(width - padding, centerY);
    ctx.stroke();


    ctx.beginPath();
    ctx.moveTo(centerX, height - padding);
    ctx.lineTo(centerX, padding);
    ctx.stroke();

    ctx.fillStyle = COLORS.text;
    ctx.font = '14px Arial';
    ctx.fillText('X', width - padding + 5, centerY + 5);
    ctx.fillText('Y', centerX + 5, padding - 5);
};

const drawShapes = (ctx, r, scale, centerX, centerY) => {
    if (r === 0) return;

    ctx.fillStyle = COLORS.shape;

    const absR = Math.abs(r);
    if (r > 0) {
        ctx.fillRect(centerX - r * scale, centerY - r * scale, r * scale, r * scale);
    } else {
        ctx.fillRect(centerX, centerY, absR * scale, absR * scale);
    }

    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    if (r > 0) {
        ctx.lineTo(centerX + (r / 2) * scale, centerY);
        ctx.lineTo(centerX, centerY - (r / 2) * scale);
    } else {
        ctx.lineTo(centerX - (absR / 2) * scale, centerY);
        ctx.lineTo(centerX, centerY + (absR / 2) * scale);
    }
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    if (r > 0) {
        ctx.arc(centerX, centerY, (r / 2) * scale, 0.5 * Math.PI, Math.PI);
    } else {
        ctx.arc(centerX, centerY, (absR / 2) * scale, 1.5 * Math.PI, 2 * Math.PI);
    }
    ctx.fill();
};

const drawLabels = (ctx, r, scale, centerX, centerY) => {
    ctx.fillStyle = COLORS.text;
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    ctx.fillText('0', centerX - 12, centerY + 12);

    for (let i = 1; i < MAX_VALUE; i++) {
        const xPos = centerX + i * scale;
        ctx.beginPath(); ctx.moveTo(xPos, centerY - 3); ctx.lineTo(xPos, centerY + 3); ctx.stroke();
        ctx.fillText(i.toString(), xPos, centerY + 15);

        const xNeg = centerX - i * scale;
        ctx.beginPath(); ctx.moveTo(xNeg, centerY - 3); ctx.lineTo(xNeg, centerY + 3); ctx.stroke();
        ctx.fillText("-" + i, xNeg, centerY + 15);

        const yPosUp = centerY - i * scale;
        ctx.beginPath(); ctx.moveTo(centerX - 3, yPosUp); ctx.lineTo(centerX + 3, yPosUp); ctx.stroke();
        ctx.fillText(i.toString(), centerX - 15, yPosUp);

        const yPosDown = centerY + i * scale;
        ctx.beginPath(); ctx.moveTo(centerX - 3, yPosDown); ctx.lineTo(centerX + 3, yPosDown); ctx.stroke();
        ctx.fillText("-" + i, centerX - 15, yPosDown);
    }
};

const drawPoints = (ctx, points, scale, centerX, centerY, currentR) => {
    if (currentR === 0){
        return;
    }

    points.forEach(point => {
        let xVal = point.x;
        let yVal = point.y;

        if (currentR !== 0 && point.r !== 0) {
            const factor = currentR / point.r;
            xVal = point.x * factor;
            yVal = point.y * factor;
        }

        const x = centerX + xVal * scale;
        const y = centerY - yVal * scale;

        ctx.beginPath();
        ctx.arc(x, y, 4, 0, 2 * Math.PI);
        ctx.fillStyle = point.hit ? COLORS.pointHit : COLORS.pointMiss;
        ctx.fill();
        ctx.strokeStyle = COLORS.pointBorder;
        ctx.lineWidth = 1;
        ctx.stroke();
    });
};

export const drawGraph = (canvas, r, points) => {
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    const padding = 20;
    const centerX = width / 2;
    const centerY = height / 2;

    const pixelsPerUnit = (width / 2 - padding) / MAX_VALUE;

    drawBackground(ctx, width, height);
    drawShapes(ctx, r, pixelsPerUnit, centerX, centerY);
    drawAxes(ctx, width, height, padding, centerX, centerY);
    drawLabels(ctx, r, pixelsPerUnit, centerX, centerY);
    drawPoints(ctx, points, pixelsPerUnit, centerX, centerY, r);
};