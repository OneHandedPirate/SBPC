let chart

document.addEventListener('DOMContentLoaded', function () {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    const searchButton = document.getElementById('search-button');
    let selectedProduct = null;

    searchInput.addEventListener('input', function (event) {
        let query = searchInput.value;
        if (query.length >= 3) {
            fetch('/search/?q=' + encodeURIComponent(query))
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    searchResults.innerHTML = '';
                    let found = false;
                    data.results.forEach(function (result) {
                        const div = document.createElement('div');
                        div.className = 'result';
                        div.textContent = result.name;
                        div.addEventListener('click', function () {
                            searchInput.value = result.name;
                            searchResults.innerHTML = '';
                            found = true;
                            selectedProduct = result.name;
                            searchButton.disabled = false;
                        });
                        searchResults.appendChild(div);
                        if (result.name.toLowerCase() === query.toLowerCase()) {
                            found = true;
                            selectedProduct = result.name;
                        }
                    });
                    searchResults.style.display = (data.results.length > 0) ? 'block' : 'none';
                    if (!found) {
                        selectedProduct = null;
                        searchButton.disabled = true;
                    }
                })
                .catch(function (error) {
                    console.log(error);
                });
        } else {
            searchResults.innerHTML = '';
            searchResults.style.display = 'none';
            selectedProduct = null;
            searchButton.disabled = true;
        }
    });

    searchInput.addEventListener('focus', function (event) {
        if (searchResults.innerHTML.trim() !== '') {
            searchResults.style.display = 'block';
        }
    });

    searchForm.addEventListener('submit', function (event) {
        event.preventDefault();
        if (chart) {
            chart.destroy();
        }
        searchInput.value = ''
        searchButton.disabled = true;
        if (selectedProduct !== null) {
            fetch('/prices/?q=' + encodeURIComponent(selectedProduct))
                .then(response => response.json())
                .then((data) => {
                    drawChart(data);
                });
        }

    });

    document.addEventListener('click', function (event) {
        if (event.target !== searchInput && event.target !== searchResults) {
            searchResults.style.display = 'none';
        }
    });
});

function drawChart(data) {
    const ctx = document.getElementById('myChart').getContext('2d');

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
