const loanAmountSlider = document.getElementById('loanAmountSlider');
const tenureSlider = document.getElementById('tenureSlider');
const interestSlider = document.getElementById('interestSlider');

const loanAmountInput = document.getElementById('loanAmountInput');
const tenureInput = document.getElementById('tenureInput');
const interestInput = document.getElementById('interestInput');

const emiDisplay = document.getElementById('emiDisplay');
const principalDisplay = document.getElementById('principalDisplay');
const interestDisplay = document.getElementById('interestDisplay');
const totalDisplay = document.getElementById('totalDisplay');

// Initialize Chart.js
const ctx = document.getElementById('loanChart').getContext('2d');
let loanChart = new Chart(ctx, {
    type: 'pie',
    data: {
        datasets: [{
            data: [993422, 42195],
            backgroundColor: ['#0F7B7B', '#9e7833'],
            
            // 👇 THIS creates gap
            spacing: 4,

            // 👇 THIS slightly separates slices
            offset: 8,

            borderWidth: 0
        }]
    },
    options: {
        plugins: {
            legend: { display: false }
        }
    }
});

function formatCurrency(num) {
    return "₹ " + Number(num).toLocaleString('en-IN');
}

function calculateEMI() {
    let P = parseFloat(loanAmountInput.value);
    let annualRate = parseFloat(interestInput.value);
    let n = parseFloat(tenureInput.value) * 12;

    let r = annualRate / 12 / 100;

    let emi;

    if (r === 0) {
        emi = P / n;
    } else {
        emi = (P * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
    }

    let totalPayable = emi * n;
    let totalInterest = totalPayable - P;

    emiDisplay.innerText = formatCurrency(Math.round(emi));
    principalDisplay.innerText = formatCurrency(P);
    interestDisplay.innerText = formatCurrency(Math.round(totalInterest));
    totalDisplay.innerText = formatCurrency(Math.round(totalPayable));

    // Smooth chart update
    loanChart.data.datasets[0].data = [P, totalInterest];
    loanChart.update('active');
}
function updateSliderFill(slider) {
    const min = slider.min || 0;
    const max = slider.max || 100;
    const value = slider.value;

    const percentage = ((value - min) / (max - min)) * 100;

    slider.style.background = `linear-gradient(to right, #9e7833 0%, #9e7833 ${percentage}%, #e5e7eb ${percentage}%, #e5e7eb 100%)`;
}
// Sync Sliders and Inputs
function syncValues(slider, input) {
    slider.addEventListener('input', () => {
        input.value = slider.value;
        updateSliderFill(slider);
        calculateEMI();
    });

    input.addEventListener('input', () => {
        slider.value = input.value;
        updateSliderFill(slider);
        calculateEMI();
    });
}
syncValues(loanAmountSlider, loanAmountInput);
syncValues(tenureSlider, tenureInput);
syncValues(interestSlider, interestInput);

// Run on load
calculateEMI();
