<script>
  import { onMount } from 'svelte';
  // @ts-ignore
  import Plotly from 'plotly.js-dist';

  import { dbData as dbDataStore, LBS_CO2_PER_KWH, DOLLARS_SAVED_PER_KWH, selectedPanelStore } from '../../stores';

  let container;
  let selectedPanelName = null;
  let selectedPanelDescription = "";
  let selectedPanelUrl = "";
  let selectedPanelImageUrl = "";
  let dbData= {};

  async function renderPlot(dbData, unit, multiplier) {
    const data = [];
    for (const [panelName, xy] of Object.entries(dbData)) {
      if (!selectedPanelName || panelName === selectedPanelName) {
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

  function updatePanelSelection(event) {
    isLoading = true;
    selectedPanelName = event.target.value;
    if (selectedPanelName === "all") {
      selectedPanelName = null; 
      selectedPanelDescription="";
      selectedPanelUrl="";
      selectedPanelImageUrl = "";
    }
    else {
      selectedPanelDescription = dbData[selectedPanelName].desc;
      selectedPanelUrl = dbData[selectedPanelName].url;
      selectedPanelImageUrl = dbData[selectedPanelName].image || "https://i0.wp.com/couillardsolarfoundation.org/wp-content/uploads/2021/01/1Merton-2.png?w=1011&ssl=1"
    }
    selectedPanelStore.set(selectedPanelName); // update store value
    showKwhData();
  }

</script>

<section>
  <div bind:this={container}></div>
</section>

<section style:display={isLoading ? 'none' : 'block'}>
  <div id="description">
    <p>Filter Panels:</p>
    <select on:change={updatePanelSelection}>
      <option value="all">All Panels</option>
      {#each Object.keys(dbData || {}) as panelName}
        <option value="{panelName}">{panelName}</option>
      {/each}
    </select>
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
    
  <div id="explanations">
    To zoom out, scroll down with your cursor over the graph. To zoom in, scroll up.<br>
    You can also use the buttons in the top right, above the legend, to zoom in/out and reset.<br>
    Click, hold and drag to pan sideways on the graph.<br>
    Click on an array in the legend to toggle that line off/on.
  </div>
  
  {#if selectedPanelUrl}
    <a href={selectedPanelUrl}>Check out where we are getting the data for {selectedPanelName} from</a>
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

  a {
    color: var(--couillard-blue-color);
    text-decoration: underline;
    margin: 0.5rem;
  }

</style>
