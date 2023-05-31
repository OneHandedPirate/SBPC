let chart

const searchResults = document.querySelector('#results')
const chartElem = document.querySelector('#chart')
const searchInput = document.querySelector('#search-input')

searchInput.addEventListener('input', event => {
    if (chart) {
        chart.destroy()
    }

    if (searchInput.value.length > 0 && searchResults.innerHTML === '') {
        searchResults.innerHTML = '<div class="text-center">Loading...</div>'
    }

    setTimeout(() => {
        if (searchInput.value.length > 0 && searchResults.innerHTML === '') {
            searchResults.innerHTML = '<div class="text-center">No results</div>'
        }
    }, 2000)
})
chartElem.addEventListener('DOMSubtreeModified', event => {
    if (searchResults.innerHTML !== '') {
    searchResults.innerHTML = '';
    let data = JSON.parse(chartElem.innerHTML);
    drawChart(data);
    searchInput.value = ''
    chartElem.innerHTML = ''
}})

function drawChart(data) {
    const ctx = document.getElementById('chart').getContext('2d');

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.prices.map(function (price) {
                return price.date;
            }),
            datasets: [{
                label: data.name,
                data: data.prices.map(function (price) {
                    return price.price;
                }),
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderWidth: 2,
                pointRadius: 3,
                fill: false,
            }]
        },
        options: {
            legend: {
                display: true,
                onClick: function (event, legendItem) {
                    event.stopPropagation();
                }
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Дата'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Цена'
                    },
                    ticks: {
                        beginAtZero: false
                    }
                }]
            },
            elements: {
                line: {
                    tension: 0.4
                }
            },
            plugins: {
                filler: {
                    propagate: false
                }
            },
        }
    });
}

