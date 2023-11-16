<script>
  import { onMount } from 'svelte';
  // @ts-ignore
  import Plotly from 'plotly.js-dist';

  let container;
  let currentData;

  // Define your original data and modified data
  const kwhData = {
    x: [1, 2, 3, 4, 5],
    y: [1, 2, 4, 8, 16],
    name: 'kWh Produced',
    type: 'scatter',
    mode: 'lines+markers'
  };

  const lbsCO2Data = {
    x: kwhData.x,
    y: kwhData.y.map(y => y * 0.954),
    name: 'lbs CO2 Saved',
    type: 'scatter',
    mode: 'lines+markers'
  };

  const dollarData = {
    x: kwhData.x,
    y: kwhData.y.map(y => y * 0.14),
    name: 'Dollars Saved',
    type: 'scatter',
    mode: 'lines+markers'
  };

  const config = {
    responsive: true,
    displaylogo: false,
    modeBarButtonsToRemove: ["autoScale2d", "select2d", "zoom2d", "lasso2d", "toImage", "pan2d"],
    displayModeBar: true,
    scrollZoom: true,
  };

  // Function to update the data and layout based on button clicked
  function showData(selectedData) {
    currentData = [...selectedData]; // Use spread operator to trigger reactivity
    console.log(selectedData); // For debugging
    let yAxisTitle = selectedData.length === 1 ? selectedData[0].name : "kWh Produced, lbs CO2 Saved, & Dollars Saved";

    const updatedLayout = {
      xaxis: { title: "Date" },
      yaxis: { title: yAxisTitle, fixedrange: true },
      title: "Solar Array Output",
      dragmode: "pan"
    };

    //@ts-ignore
    Plotly.purge(container);
    //@ts-ignore
    Plotly.newPlot(container, currentData, updatedLayout, config);
  }

  function resetGraph() {
    showData([kwhData, lbsCO2Data, dollarData]);
  }

  onMount(() => {
    // Initially show all data
    resetGraph();
  });
</script>

<div bind:this={container}></div>
<div class="buttons">
  <button on:click={() => showData([kwhData])}>Show kWh Produced</button>
  <button on:click={() => showData([lbsCO2Data])}>Show lbs CO2 Saved</button>
  <button on:click={() => showData([dollarData])}>Show Dollars Saved</button>
  <button on:click={() => resetGraph()}>Show All Data</button>
</div>
