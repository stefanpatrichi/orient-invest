const windowSize = 200;

async function updateImage() {
    const select  = document.getElementById("etf-select");
    const chart   = document.getElementById("etf-chart");
    const selected = select.value;

    const jsondata = await fetch(
        `http://127.0.0.1:8000/get_etf_history?etf=${selected}`
    ).then(r => r.json()).then(data => JSON.parse(data));

    const xValues = Object.keys(jsondata).map(Number);
    const yValues = Object.values(jsondata);

    const trace = { x: xValues, y: yValues, type: "scatter", mode: "lines", name: "XY dict"};

    let minX = xValues.findIndex(x => jsondata[x] != null);
    if (minX < 0) minX = 0;

    const isMobile = window.innerWidth < 600;
    Plotly.newPlot("plot-closing-prices", [trace], {
        autosize: true,
        title: "Prețuri",
        xaxis: {
            title: "Timp",
            range: [minX, xValues.length],
            linewidth: 1,
            automargin: true,
            titlefont: { size: isMobile ? 12 : 16 },
            tickfont:  { size: isMobile ? 10 : 14 }
        },
        yaxis: {
            title: "Preț",
            linewidth: 1,
            automargin: true,
            titlefont: { size: isMobile ? 12 : 16 },
            tickfont:  { size: isMobile ? 10 : 14 }
        },
        font: { size: isMobile ? 12 : 16 }
    }, { responsive: true });

    document.getElementById("plot-closing-prices").style.margin = "auto";
}

function toggleMenu() {
    document.getElementById("mobileMenu").classList.toggle("open");
}

const dropdown              = document.getElementById("etf-dropdown");
const selectedEtfsContainer = document.getElementById("selected-etfs");
let   etfOrder              = [];

dropdown.addEventListener("change", () => {
    const value = dropdown.value;
    const label = dropdown.options[dropdown.selectedIndex].text;
    if (!document.getElementById(value)) {
        const tag = document.createElement("div");
        tag.className = "etf-tag";
        tag.id        = value;
        tag.innerHTML = `
            ${label}
            <button onclick="removeEtf('${value}')">
                <img src="images/close.svg" width="15" style="margin-top:5px">
            </button>`;
        selectedEtfsContainer.appendChild(tag);
    }
});
function removeEtf(id){ const tag = document.getElementById(id); if(tag) tag.remove(); }

fetch("http://127.0.0.1:8000/get_etfs")
    .then(r => r.json())
    .then(data => {
        etfOrder = data;
        const select1 = document.getElementById("etf-select");
        const select2 = document.getElementById("etf-dropdown");
        select1.innerHTML = select2.innerHTML = "";
        data.forEach(etf => {
            select1.appendChild(new Option(etf, etf));
            select2.appendChild(new Option(etf, etf));
        });
    })
    .catch(err => { console.error(err); alert("get_etfs error."); });

document.getElementById("train-model-btn").addEventListener("click", async () => {
    const tags = Array.from(selectedEtfsContainer.children).map(el => el.id);
    if (tags.length < 1) { alert("Selectează cel puțin două ETF-uri înainte de antrenare."); return; }
    const sortedTags = etfOrder.filter(etf => tags.includes(etf));
    const data = await fetch("http://127.0.0.1:8000/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(sortedTags)
    }).then(r => r.json()).catch(e => { console.error(e); alert("Eroare la antrenare."); });

    const ul = document.getElementById("results-ul");
    ul.innerHTML = "";
    data.allocations.forEach((value, idx) => {
        const li = document.createElement("li");
        li.textContent = `${sortedTags[idx]}: ${(value * 100).toFixed(2)}%`;
        ul.appendChild(li);
    });
    document.getElementById("result-list").style.display = "block";
    document.getElementById("roi-sharpe").innerHTML = `
        <b>Rată de recuperare a investiției (ROI, return on investment):</b> ${(data.roi * 100).toFixed(2)}%<br>
        <b>Raport Sharpe:</b> ${data.sharpe.toFixed(2)}`;

    const sliders = document.getElementById("weight-sliders");
    sliders.innerHTML = "<h3>Ponderile ETF-urilor:</h3>";
    var officialScalars = [];
    sortedTags.forEach((tag, idx) => {
        const pct = Math.floor(data.allocations[idx] * 100);
        officialScalars.push(data.allocations[idx]);
        const label = document.createElement("label");
        label.innerHTML = `
            ${tag}: <input type="range" id="${tag}-slider" min="0" max="100" step="1" value="${pct}">
            <span id="${tag}-val">${pct}</span>`;
        sliders.appendChild(label);
    });

    const histories = await Promise.all( sortedTags.map(tag =>
        fetch(`http://127.0.0.1:8000/get_etf_history?etf=${tag}`)
            .then(r => r.json())
            .then(data => JSON.parse(data))
            .then(obj => ({
                tag,
                x:  Object.keys(obj).map(Number),
                y:  Object.values(obj)
            }))
    ));

    const xValues  = histories[0].x;
    const yValList = histories.map(h => h.y);
    
    console.log(yValList);

    // var minX = 0;
    // yValList.forEach(arr => {
    //     let mintemp = arr.findIndex(x => x != null);
    //     if (mintemp < 0) minX = 0;

    //     if (mintemp > minX) minX = mintemp;
    // });
    var maxY = Math.max(...yValList.flat().filter(v => v != null));
    console.log(maxY);

    const isMobile = window.innerWidth < 600;
    const layout = {
        autosize   : true,
        title      : "Prețuri",
        uirevision : "keep-axes",
        xaxis: {
            title      : "Timp",
            range      : [yValList[0].length - windowSize + 1, yValList[0].length],
            linewidth  : 1,
            automargin : true,
            titlefont  : { size: isMobile ? 12 : 16 },
            tickfont   : { size: isMobile ? 10 : 14 }
        },
        yaxis: {
            title      : "Preț",
            range      : [0, maxY],
            linewidth  : 1,
            automargin : true,
            titlefont  : { size: isMobile ? 12 : 16 },
            tickfont   : { size: isMobile ? 10 : 14 }
        },
        font: { size: isMobile ? 12 : 16 }
    };

    function updatePlot(){
        const scalars = sortedTags.map(tag => {
            const x = parseInt(document.getElementById(`${tag}-slider`).value, 10);
            document.getElementById(`${tag}-val`).textContent = x;
            return x / 100;
        });
        /* combine scalar * price for each day */
        const yValues = xValues.map((_, i) =>
            yValList.reduce((sum, arr, j) => sum + scalars[j] * arr[i], 0)
        );
        document.getElementById("plot-options").style.height = "500px";
        console.log(layout);
        Plotly.react("plot-options", [{
            x: xValues,
            y: yValues,
            type: "scatter",
            mode: "lines",
            name: "XY dict"
        }], layout, { responsive: true });
        document.getElementById("plot-options").style.margin = "auto";
    }
    updatePlot();
    sortedTags.forEach(tag =>
        document.getElementById(`${tag}-slider`).addEventListener("input", updatePlot)
    );
});