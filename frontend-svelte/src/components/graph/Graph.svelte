<script>
  import { onMount } from 'svelte';
  import Plotly, { getDataToPixel } from 'plotly.js-dist';

  import { dbData as dbDataStore, selectedPanelStore } from '../../stores';

  let container;
  let selectedPanelName = null;
  let selectedPanelDescription = "";
  let selectedPanelUrl = "";
  let dbData= {};

  async function renderPlot(dbData) {
    const data = [];
    for (const [panelName, xy] of Object.entries(dbData)) {
      if (!selectedPanelName || panelName === selectedPanelName) 
      {
        //console.log(panelName);
        data.push({
          name: `${panelName} (kWh)`,
          x: xy.x,
          y: xy.y,
        });
      }
    }

    const layout = {
      xaxis: {
        title: "Date",
        range: [new Date(new Date().getTime() - 1000 * 60 * 60 * 24 * 30 * 6), new Date()] // last 6 months (roughly)
      },
      yaxis: {
        title: "Energy (kWh)",
        fixedrange: true,
      },
      title: "Solar Array Output",
      dragmode: "pan",
    };

    const config = {
      responsive: true,
      displaylogo: false,
      modeBarButtonsToRemove: [
        "autoScale2d",
        "select2d",
        "zoom2d",
        "lasso2d",
        "toImage",
        "pan2d",
      ],
      
      displayModeBar: true,
      scrollZoom: true,
    };
    //@ts-ignore
    Plotly.newPlot(container, data, layout, config);
  }
  
  onMount(() => {
    dbDataStore.subscribe(async promise => {
      dbData = await promise;
      renderPlot(dbData);
    });
  });

  function updatePanelSelection(event) {
    selectedPanelName = event.target.value;
    if (selectedPanelName === "all") {
      selectedPanelName = null; 
      selectedPanelDescription="";
      selectedPanelUrl="";
    }
    else {
      selectedPanelDescription = dbData[selectedPanelName].desc;
      selectedPanelUrl = dbData[selectedPanelName].url;
    }
    selectedPanelStore.set(selectedPanelName); // update store value
    renderPlot(dbData);
  }

</script>
  
<div id="description">
  <p>Filter Panels:</p>
  <select on:change={updatePanelSelection}>
    <option value="all">All Panels</option>
    {#each Object.keys(dbData || {}) as panelName}
      <option value="{panelName}">{panelName}</option>
    {/each}
  </select>
  <p>{selectedPanelDescription}</p>
  <p>{selectedPanelUrl}</p>
</div>
<div bind:this={container}></div>

<div id="explanations">
  To zoom out, scroll down with your cursor over the graph. To zoom in, scroll up.<br>
  You can also use the buttons in the top right, above the legend, to zoom in/out and reset.<br>
  Click, hold and drag to pan sideways on the graph.<br>
  Click on an array in the legend to toggle that line off/on.
</div>


<style>
  #explanations {
    text-align: center;
    align-items: center;
    padding-top: 5px;
    padding-bottom: 20px;
    color: black;
  }

  #description {
    padding: 15px;
    text-align: center;
  }

  #description p {
    margin: 0px;
    padding: 5px;
    font-size: 18px;
    font-weight: bold;
  }

  #description select {
    padding: 10px; 
    font-size: 16px; 
    cursor: pointer; 
    border: none;
    border-radius: 4px; 
    background-color: var(--couillard-orange-color);
  }
</style>
