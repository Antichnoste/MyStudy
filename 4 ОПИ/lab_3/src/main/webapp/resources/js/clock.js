class AnalogClock {
    constructor() {
        this.hourHand = document.getElementById('hour-hand');
        this.minuteHand = document.getElementById('minute-hand');
        this.secondHand = document.getElementById('second-hand');
        this.digitalTimeElement = document.getElementById('digital-time');
        this.container = document.getElementById('clock-container');

        this.init();
    }

    init() {
        if (!this.container) return;

        const periodSeconds = parseInt(this.container.getAttribute('data-period-sec'));

        let updateInterval = 1000;
        if (isFinite(periodSeconds) && periodSeconds > 0){
            updateInterval= periodSeconds * 1000
        }

        this.update();
        setInterval(() => this.update(), updateInterval);
    }

    update() {
        const now = new Date();
        const hours = now.getHours();
        const minutes = now.getMinutes();
        const seconds = now.getSeconds();

        if (this.hourHand) {
            this.hourHand.style.transform = `translateX(-50%) rotate(${(hours % 12) * 30 + minutes * 0.5}deg)`;
        }
        if (this.minuteHand) {
            this.minuteHand.style.transform = `translateX(-50%) rotate(${minutes * 6 + seconds * 0.1}deg)`;
        }
        if (this.secondHand) {
            this.secondHand.style.transform = `translateX(-50%) rotate(${seconds * 6}deg)`;
        }

        if (this.digitalTimeElement) {
            this.digitalTimeElement.textContent =
                `${now.getFullYear()}-${('0' + (now.getMonth() + 1)).slice(-2)}-${('0' + now.getDate()).slice(-2)} ` +
                `${('0' + hours).slice(-2)}:${('0' + minutes).slice(-2)}:${('0' + seconds).slice(-2)}`;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new AnalogClock();
});