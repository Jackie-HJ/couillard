<script>
  import { onMount } from 'svelte';
  // @ts-ignore
  import Plotly from 'plotly.js-dist';

  let container;

  // Define yourdata
  const kwhData = {
    x: [1, 2, 3, 4, 5],
    y: [1, 2, 4, 8, 16],
    name: 'kWh Produced',
    type: 'scatter',
    mode: 'lines+markers',
    line: { color: 'rgb(16, 58, 113)' }, // Couillard Blue
    marker: { color: 'rgb(16, 58, 113)' }
  };

  const lbsCO2Data = {
    x: kwhData.x,
    y: kwhData.y.map(y => y * 0.954),
    name: 'lbs CO2 Saved',
    type: 'scatter',
    mode: 'lines+markers',
    line: { color: 'rgb(247, 147, 30)' }, // Couillard Orange
    marker: { color: 'rgb(247, 147, 30)' }
  };

  const dollarData = {
    x: kwhData.x,
    y: kwhData.y.map(y => y * 0.14),
    name: 'Dollars Saved',
    type: 'scatter',
    mode: 'lines+markers',
    line: { color: 'black' },
    marker: { color: 'black' }
  };

  const config = {
    responsive: true,
    displaylogo: false,
    modeBarButtonsToRemove: ["autoScale2d", "select2d", "zoom2d", "lasso2d", "toImage", "pan2d"],
    displayModeBar: true,
    scrollZoom: true,
  };

  const layout = {
    xaxis: { title: "Date" },
    yaxis: { title: "", fixedrange: true},
    title: "Solar Array Output",
    dragmode: "pan"
  };

  function updateGraph(data) {
    // Update the Y-axis title based on the dataset
    layout.yaxis.title = data.length === 1 ? data[0].name : "Various Metrics";
    // @ts-ignore
    Plotly.newPlot(container, data, layout, config);
  }

  function showKwhData() {
    updateGraph([kwhData]);
  }

  function showLbsCO2Data() {
    updateGraph([lbsCO2Data]);
  }

  function showDollarData() {
    updateGraph([dollarData]);
  }

  function resetGraph() {
    updateGraph([kwhData, lbsCO2Data, dollarData]);
  }

  onMount(() => {
    resetGraph();
  });
</script>

<div bind:this={container}></div>
<div id="explanation">
  To zoom into graph, scroll outwards. To zoom out, scroll inwards.
  Click on legend to toggle which solar stations' data is displayed.
</div>
<div class="buttons">
  <button on:click={showKwhData}>Show kWh Produced</button>
  <button on:click={showLbsCO2Data}>Show lbs CO2 Saved</button>
  <button on:click={showDollarData}>Show Dollars Saved</button>
  <button on:click={resetGraph}>Show All Data</button>
</div>
