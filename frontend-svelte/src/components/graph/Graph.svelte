<script>
  import { onMount } from 'svelte';
  // @ts-ignore
  import Plotly from 'plotly.js-dist';

  import { dbData as dbDataStore, LBS_CO2_PER_KWH, DOLLARS_SAVED_PER_KWH } from '../../stores';

  let container;

  // Define yourdata
  // const kwhData = {
  //   x: [1, 2, 3, 4, 5],
  //   y: [1, 2, 4, 8, 16],
  //   name: 'kWh Produced',
  //   type: 'scatter',
  //   mode: 'lines+markers',
  //   line: { color: 'rgb(16, 58, 113)' }, // Couillard Blue
  //   marker: { color: 'rgb(16, 58, 113)' }
  // };
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

  async function renderPlot(dbData, unit, multiplier) {
    const data = [];
    for (const [panelName, xy] of Object.entries(dbData)) {
      data.push({
        name: `${panelName} (${unit})`,
        ...xy,
      });
    }
    if(multiplier)
      data.forEach(line => line.y.map(y => y * multiplier));
    // @ts-ignore
    Plotly.newPlot(container, data, layout, config);
  }

  // const lbsCO2Data = {
  //   x: kwhData.x,
  //   y: kwhData.y.map(y => y * 0.954),
  //   name: 'lbs CO2 Saved',
  //   type: 'scatter',
  //   mode: 'lines+markers',
  //   line: { color: 'rgb(247, 147, 30)' }, // Couillard Orange
  //   marker: { color: 'rgb(247, 147, 30)' }
  // };

  // const dollarData = {
  //   x: kwhData.x,
  //   y: kwhData.y.map(y => y * 0.14),
  //   name: 'Dollars Saved',
  //   type: 'scatter',
  //   mode: 'lines+markers',
  //   line: { color: 'black' },
  //   marker: { color: 'black' }
  // };

  // function updateGraph(data) {
  //   // Update the Y-axis title based on the dataset
  //   layout.yaxis.title = data.length === 1 ? data[0].name : "Various Metrics";
  //   // @ts-ignore
  //   Plotly.newPlot(container, data, layout, config);
  // }

  async function showKwhData() {
    dbDataStore.subscribe(async promise => {
      renderPlot(await promise, "kWh");
    });
  }

  async function showLbsCO2Data() {
    dbDataStore.subscribe(async promise => {
      renderPlot(await promise, "lbs CO2 Saved", LBS_CO2_PER_KWH);
    });
  }

  async function showDollarData() {
    dbDataStore.subscribe(async promise => {
      renderPlot(await promise, "Dollars Saved", DOLLARS_SAVED_PER_KWH);
    });
  }

  onMount(() => {
    showKwhData();
  });
</script>

<div bind:this={container}></div>
<div class="buttons">
  <button on:click={showKwhData}>Show kWh Produced</button>
  <button on:click={showLbsCO2Data}>Show lbs CO2 Saved</button>
  <button on:click={showDollarData}>Show Dollars Saved</button>
</div>
