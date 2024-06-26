function submit() {
    const cl = document.getElementById("toggle").checked ? 0 : 1;
    const zip = document.getElementById("zipcode").value;
    const loading = document.getElementById("loading").value;
    const takeOff = document.getElementById("dep").value;
    const modi = document.getElementById("modi").value;

    let link = "stromRechner";
    if (modi === "solar") {
        link = "stromRechnerSolar";
    } else if (modi === "comb") {
        link = "stromRechnerCombined";
    }

    const xhr = new XMLHttpRequest();
    xhr.open("GET", `http://127.0.0.1:5000/${link}?zip=${zip}&dur=${loading}&takeOff=${takeOff}&split=${cl}`);
    xhr.responseType = "json";

    xhr.onload = () => {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                const data = xhr.response;
                console.log(data);
                renderTable(data);
                if (data.code === 200) {
                    renderChart(data.data);
                }
            } else {
                console.error(`Error: ${xhr.status} - ${xhr.statusText}`);
            }
        }
    };

    xhr.onerror = () => {
        console.error('Request failed');
    };

    xhr.send();
}

function renderChart(data) {
    // Reset any existing chart
    if (window.myChart) {
        window.myChart.destroy();
    }

    let labels = data.map(entry => entry.time_str);

    // Extract all details fields dynamically
    let detailsKeys = Object.keys(data[0].details || {});
    let datasets = [];

    // Define colors for datasets
    const colors = [
        'rgb(54, 162, 235)',    // Blue
        'rgb(255, 205, 86)',    // Yellow
        'rgb(255, 99, 132)',    // Red
        'rgb(153, 102, 255)',   // Purple
        'rgb(255, 159, 64)'     // Orange
    ];

    // Highlight the 'value' field
    datasets.push({
        label: 'Efficiency',
        data: data.map(entry => entry.value),
        fill: false,
        borderColor: 'rgb(75, 192, 192)', // Red color for highlight
        tension: 0.1
    });

    // Iterate over each details field
    detailsKeys.forEach((key, index) => {
        let dataset = {
            label: key.charAt(0).toUpperCase() + key.slice(1), // Capitalize first letter
            data: data.map(entry => entry.details[key] !== undefined ? entry.details[key] : null),
            fill: false,
            borderColor: colors[index % colors.length], // Use different color for each dataset
            tension: 0.1
        };
        datasets.push(dataset);
    });

    // Get canvas element
    let ctx = document.getElementById('chart').getContext('2d');

    // Create chart instance
    window.myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Value'
                    }
                }
            }
        }
    });
}

function renderTable(response) {
    const container = document.getElementById('result-container');
    container.innerHTML = ""; // Clear any previous content

    if (response.code === 200) {
        data = response.data.filter(entry => entry.highest == 1)
        const table = document.createElement('table');
        table.className = 'table table-striped';

        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        ['Date', 'Time', "Efficiency"].forEach(headerText => {
            const th = document.createElement('th');
            th.innerText = headerText;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        data.forEach(item => {
            const row = document.createElement('tr');

            const dateTd = document.createElement('td');
            const timeTd = document.createElement('td');
            const [date, time] = item.time_str.split(' ');

            dateTd.innerText = date;
            timeTd.innerText = time;

            const dataTd = document.createElement('td');
            dataTd.innerText = item.value;

            row.appendChild(dateTd);
            row.appendChild(timeTd);
            row.appendChild(dataTd);

            tbody.appendChild(row);
        });
        table.appendChild(tbody);

        container.appendChild(table);
    } else {
        const errorMsg = document.createElement('p');
        errorMsg.className = 'text-danger';
        errorMsg.innerText = `Error: ${response.data}`;
        container.appendChild(errorMsg);
    }
}