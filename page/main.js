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

        console.log(jsondata)
        console.log(xValues)
        console.log(yValues)

        var minX = 0;
        for (var i in xValues) {
            minX = i;
            if (jsondata[i] != null) break;
        }

        console.log(minX)

        const isMobile = window.innerWidth < 600;
        Plotly.newPlot('plot-closing-prices', [trace], {
            autosize: true,
            title: 'Prețuri de închidere ' + selected,
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
    console.log("API răspuns:", data);

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
    if (tags.length === 0) {
        alert("Selectează cel puțin un ETF înainte de antrenare.");
        return;
    }

    const sortedTags = etfOrder.filter((etf) => tags.includes(etf));

    fetch("http://127.0.0.1:8000/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(sortedTags),
    })
        .then((res) => res.json())
        .then((data) => {
            const resultDiv = document.getElementById("result-list");
            const ul = document.getElementById("results-ul");
            ul.innerHTML = "";

            data.forEach((value, idx) => {
                const li = document.createElement("li");
                li.textContent = `${sortedTags[idx]}: ${(value * 100).toFixed(
                    2
                )}%`;
                ul.appendChild(li);
            });

            resultDiv.style.display = "block";
        })
        .catch((err) => {
            console.error(err);
            alert("Eroare la antrenare.");
        });
});
