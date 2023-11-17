<script>
  import { onMount } from 'svelte';
  import Plotly, { getDataToPixel } from 'plotly.js-dist';

  import { dbData as dbDataStore } from '../../stores';

  let container;
  let selectedPanelName = null;
  let dbData= {};

/*   $: dbDataStore.subscribe(value => { dbData = value; });
  $: if (dbData) renderPlot(dbData); */

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
        //range: [new Date(new Date().getTime() - 15768000), new Date()]   - last 6 months, can use this once we have data with dates
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
      console.log(dbData);
      renderPlot(dbData);
    });
  });

  function updatePanelSelection(event) {
    selectedPanelName = event.target.value;
    //console.log(dbData);
    renderPlot(dbData);
  }

</script>
  
<div id="description">
  <select on:change={updatePanelSelection}>
    <option value="">Select a panel</option>
    {#each Object.keys(dbData || {}) as panelName}
      <option value="{panelName}">{panelName}</option>
    {/each}
  </select>
</div>
<div bind:this={container}></div>

<div id="explanations">
  To zoom into graph, scroll outwards. To zoom in, scroll inwards.<br>
  Click on legend to toggle which solar data sources are shown.
</div>


<style>
  #explanations {
    text-align: center;
    align-items: center;
    padding-top: 5px;
    padding-bottom: 20px;
  }

  #description {
    padding: 15px;
  }
</style>