<script>
  import { onMount } from 'svelte';
  // @ts-ignore
  import Plotly from 'plotly.js-dist';

  import { dbData as dbDataStore, panelName as panelNameStore, LBS_CO2_PER_KWH, DOLLARS_SAVED_PER_KWH } from '../../stores';

  let container;
  let selectedPanelDescription = "";
  let selectedPanelUrl = "";
  let selectedPanelImageUrl = "";
  let dbData= {};

  let selectedPanelName = "all";
  panelNameStore.subscribe(x => {
    selectedPanelName = x;
  });

  async function renderPlot(dbData, unit, multiplier) {
    const data = [];
    for (const [panelName, xy] of Object.entries(dbData)) {
      if ((selectedPanelName === "all") || panelName === selectedPanelName) {
        //console.log(panelName);
        data.push({
          name: panelName,
          x: xy.x,
          y: xy.y,
        });
      }
    }

    if(multiplier)
      data.forEach(line => line.y = line.y.map(y => y * multiplier));

    const layout = {
      xaxis: {
        title: "Date",
        range: [new Date(new Date().getTime() - 1000 * 60 * 60 * 24 * 30 * 6), new Date()] // last 6 months (roughly)
      },
      yaxis: {
        title: unit,
        fixedrange: true,
      },
      title: `Daily Array Output (${unit})`,
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


  async function showKwhData() {
    renderPlot(dbData, "kWh Produced");
  }

  async function showLbsCO2Data() {
    renderPlot(dbData, "lbs CO2 Saved", LBS_CO2_PER_KWH);
  }

  async function showDollarData() {
    renderPlot(dbData, "Dollars Saved", DOLLARS_SAVED_PER_KWH);
  }

  let isLoading = true;
  onMount(() => {
    dbDataStore.subscribe(async promise => {
      dbData = await promise;
      showKwhData();
      isLoading = false;
    });
  });

  function updatePanelSelection(selectedPanelName) {
    if (selectedPanelName === "all") {
      selectedPanelName = null; 
      selectedPanelDescription="";
      selectedPanelUrl="";
      selectedPanelImageUrl = "";
    }
    else {
      selectedPanelDescription = dbData[selectedPanelName].desc;
      selectedPanelUrl = dbData[selectedPanelName].url;
      selectedPanelImageUrl = dbData[selectedPanelName].image_url || "";
    }
    showKwhData();
  }

  panelNameStore.subscribe(updatePanelSelection);

</script>

<section style:display={isLoading ? 'none' : 'block'}>
  <div id="description">
    {#if selectedPanelDescription}
      <p>{selectedPanelDescription}</p>
    {/if}
    {#if selectedPanelImageUrl}
    <img src={selectedPanelImageUrl} alt={`picture of ${selectedPanelName} solar array`}>
    {/if}
  </div>
  
  <div>
    Change Units of Graph:
    <div class="buttons">
      <button on:click={showKwhData}>kWh</button>
      <button on:click={showLbsCO2Data}>lbs CO2</button>
      <button on:click={showDollarData}>Dollars</button>
    </div>
  </div>
</section>
  
<section>
  <div id="explanations">
    <p>
      <strong>To zoom,</strong> scroll up or down, or use the buttons in the upper-right.
      <strong>To pan,</strong> click and drag.
      <strong>To select specific panels,</strong> click on their entries in the legend.
    </p>
  </div>
  <div class="graph-wrapper">
    <div bind:this={container}></div>
  </div>
  {#if selectedPanelUrl}
    <a href={selectedPanelUrl}>
      <button>More Details</button>
    </a>
  {/if}
</section>

<style>

  section {
    color: var(--couillard-blue-color);
  }

  #explanations {
    text-align: center;
    align-items: center;
    padding-top: 5px;
    padding-bottom: 20px;
    transform: translateY(61px);
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

  a {
    color: var(--couillard-blue-color);
    text-decoration: underline;
    margin: 0.5rem;
  }

</style>
