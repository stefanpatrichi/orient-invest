function updateImage() {
    const select = document.getElementById("etf-select");
    const chart = document.getElementById("etf-chart");
    const selected = select.value;

    const imageMap = {
        etf1: "chart1.png",
        etf2: "chart2.png",
        etf3: "chart3.png",
    };

    chart.src = imageMap[selected];
}

function toggleMenu() {
    const menu = document.getElementById("mobileMenu");
    menu.classList.toggle("open");
}

const dropdown = document.getElementById("etf-dropdown");
const selectedEtfsContainer = document.getElementById("selected-etfs");

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
