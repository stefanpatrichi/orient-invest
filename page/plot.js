// const x = [0, 1, 2, 3, 4]; 
// const g = [1, 2, 3, 4, 5]; 
// const h = [5, 4, 3, 2, 1]; 
// const k = [2, 2, 2, 2, 2]; 

function computeY(a, b, c) { return g.map((gi, i) => a*gi + b*h[i] + c*k[i]); } 

function updatePlot() { 
    const a = parseFloat(document.getElementById("aSlider").value); 
    const b = parseFloat(document.getElementById("bSlider").value); 
    const c = parseFloat(document.getElementById("cSlider").value); 

    document.getElementById("aVal").textContent = a; 
    document.getElementById("bVal").textContent = b; 
    document.getElementById("cVal").textContent = c; 


    const layout = {
        title: "f(x) = a·g(x) + b·h(x) + c·k(x)",
        xaxis: { title: "x", range: [0, 5] }, // fixed x-axis range
        yaxis: { title: "f(x)", range: [0, 1000] }, // fixed y-axis range
    };
    const trace = {
        x: x,
        y: computeY(1, 1, 1),
        mode: "lines+markers",
        name: "f(x)"
    };
    Plotly.newPlot("plot", [trace], layout);
    const newy = computeY(a, b, c); 

    Plotly.restyle("plot", { y: [newy] }, [0]);
} 

["aSlider", "bSlider", "cSlider"].forEach(id => { document.getElementById(id).addEventListener("input", updatePlot); });
updatePlot(); 