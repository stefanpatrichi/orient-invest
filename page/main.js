function updateImage() {
    const select = document.getElementById("etf-select");
    const chart = document.getElementById("etf-chart");
    const selected = select.value;

    fetch("http://127.0.0.1:8000/get_etf_history?etf=" + selected, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
    }).then((res) => res.json()).then((data) => {
        jsondata = JSON.parse(data)
        const xValues = Object.keys(jsondata).map(Number);
        const yValues = Object.values(jsondata);

        const trace = {
            x: xValues,
            y: yValues,
            type: 'scatter',
            mode: 'lines',
            name: 'XY dict',
        };

        var minX = 0;
        for (var i in xValues) {
            minX = i;
            if (jsondata[i] != null) break;
        }

        const isMobile = window.innerWidth < 600;
        Plotly.newPlot('plot-closing-prices', [trace], {
            autosize: true,
            title: 'Prețuri',
            xaxis: { 
                title: 'Timp', 
                range: [minX, xValues.length], 
                linewidth: 1, 
                automargin: true, 
                titlefont: { size: isMobile ? 12 : 16 },
                tickfont: { size: isMobile ? 10 : 14 } 
            },
            yaxis: { 
                title: 'Preț', 
                linewidth: 1, 
                automargin: true, 
                titlefont: { size: isMobile ? 12 : 16 },
                tickfont: { size: isMobile ? 10 : 14 }
            },
            font: { size: isMobile ? 12 : 16 },
        }, { responsive: true });

        document.getElementById("plot-closing-prices").style["margin"] = "auto";
    });
}

function toggleMenu() {
    const menu = document.getElementById("mobileMenu");
    menu.classList.toggle("open");
}

const dropdown = document.getElementById("etf-dropdown");
const selectedEtfsContainer = document.getElementById("selected-etfs");
let etfOrder = [];

dropdown.addEventListener("change", () => {
const value = dropdown.value;
const label = dropdown.options[dropdown.selectedIndex].text;

if (!document.getElementById(value)) {
    const tag = document.createElement("div");
    tag.className = "etf-tag";
    tag.id = value;
    tag.innerHTML = `
        ${label}
        <button onclick="removeEtf('${value}')"><img src="images/close.svg" width="15px" style="margin-top:5px;"></button>
    `;
    selectedEtfsContainer.appendChild(tag);
}
});

function removeEtf(id) {
    const tag = document.getElementById(id);
    if (tag) tag.remove();
}

// Ia ETF-urile din lista
fetch("http://127.0.0.1:8000/get_etfs", {
    method: "GET",
    headers: { "Content-Type": "application/json" },
}).then((res) => res.json()).then((data) => {
    etfOrder = data;

    const select1 = document.getElementById("etf-select");
    const select2 = document.getElementById("etf-dropdown");

    select1.innerHTML = "";
    select2.innerHTML = "";

    data.forEach((etf) => {
        const option1 = document.createElement("option");
        option1.value = etf;
        option1.textContent = etf;
        select1.appendChild(option1);

        const option2 = document.createElement("option");
        option2.value = etf;
        option2.textContent = etf;
        select2.appendChild(option2);
    });
}).catch((err) => {
    console.error(err);
    alert("get_etfs error.");
});

//Script-ul pentru butonul de train
document.getElementById("train-model-btn") .addEventListener("click", () => {
    const tags = Array.from(selectedEtfsContainer.children).map(
        (el) => el.id
    );
    if (tags.length <= 0) {
        alert("Selectează cel puțin două ETF-uri înainte de antrenare.");
        return;
    }

    const sortedTags = etfOrder.filter((etf) => tags.includes(etf));

    fetch("http://127.0.0.1:8000/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(sortedTags),
    }).then((res) => res.json()).then((data) => {
        const resultDiv = document.getElementById("result-list");
        const ul = document.getElementById("results-ul");
        ul.innerHTML = "";

        data["allocations"].forEach((value, idx) => {
            const li = document.createElement("li");
            li.textContent = `${sortedTags[idx]}: ${(value * 100).toFixed(
                2
            )}%`;
            ul.appendChild(li);
        });

        resultDiv.style.display = "block";

        document.getElementById("roi-sharpe").innerHTML = 
            `<b>Rată de recuperare a investiției (ROI, return on investment):</b> ${(data["roi"] * 100).toFixed(2)}%<br>
             <b>Raport Sharpe:</b> ${data["sharpe"].toFixed(2)}`;

        const sliders = document.getElementById("weight-sliders");
        sliders.innerHTML = "";

        const h3 = document.createElement("h3");
        h3.innerText = "Ponderile ETF-urilor:";
        sliders.appendChild(h3);

        sortedTags.forEach((tag, idx) => {
            const label = document.createElement("label");
            label.innerHTML = `${tag}: <input type="range" id="${tag}-slider" min="0" max="100" step="1" 
                value="${Number(Math.floor(data["allocations"][idx] * 100))}"></label> 
                <span id="${tag}-val">${Number(Math.floor(data["allocations"][idx] * 100))}</span>`;

            sliders.appendChild(label);
        })

        function mymax(a, b) {
            return (a > b) ? a : b;
        }

        var xValues, yValList = [], minX = 0, maxY = 0;
        sortedTags.forEach(tag => {
            fetch("http://127.0.0.1:8000/get_etf_history?etf=" + tag, {
                method: "GET",
                headers: { "Content-Type": "application/json" },
            }).then((res) => res.json()).then((data) => {
                jsondata = JSON.parse(data);
                xValues = Object.keys(jsondata).map(Number);
                var _yValues = Object.values(jsondata);
                yValList.push(_yValues);
                for (var i in xValues) {
                    minX = mymax(Number(minX), Number(i));
                    if (jsondata[i] != null) break;
                }
                console.log(minX);

                yValList.forEach(subArr => {
                    subArr.splice(0, minX);
                })
                for (var arr in yValList) {
                    for (var y in arr) {
                        console.log(y);
                        maxY = mymax(Number(maxY), Number(y));
                    }
                }
                console.log(maxY);
            });
        });


        function updatePlot() {
            var scalars = [];
            sortedTags.forEach((tag) => {
                const x = parseInt(document.getElementById(`${tag}-slider`).value);
                document.getElementById(`${tag}-val`).textContent = x;
                scalars.push(x);
            });

            if (yValList.length != scalars.length) alert("length error");
            const yValues = Array.from({ length: yValList[0].length }, (_, i) => {
                return yValList.reduce((sum, arr, j) => sum + scalars[j] / 100.0 * arr[i], 0)
            });

            console.log(scalars);
            console.log(yValues);

            const trace = {
                x: xValues,
                y: yValues,
                type: 'scatter',
                mode: 'lines',
                name: 'XY dict',
            };

            const isMobile = window.innerWidth < 600;
            Plotly.newPlot('plot-options', [trace], {
                autosize: true,
                title: 'Prețuri',
                xaxis: { 
                    title: 'Timp', 
                    range: [minX, xValues.length], 
                    linewidth: 1, 
                    automargin: true, 
                    titlefont: { size: isMobile ? 12 : 16 },
                    tickfont: { size: isMobile ? 10 : 14 } 
                },
                yaxis: { 
                    title: 'Preț', 
                    range: [0, maxY],
                    linewidth: 1, 
                    automargin: true, 
                    titlefont: { size: isMobile ? 12 : 16 },
                    tickfont: { size: isMobile ? 10 : 14 }
                },
                font: { size: isMobile ? 12 : 16 },
            }, { responsive: true });

            document.getElementById("plot-closing-prices").style["margin"] = "auto";
        }

        sortedTags.forEach(tag => {
            document.getElementById(`${tag}-slider`).addEventListener("input", updatePlot);
        });
    }).catch((err) => {
        console.error(err);
        alert("Eroare la antrenare.");
    });
});
