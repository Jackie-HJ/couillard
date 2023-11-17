<script>
  import { onMount } from 'svelte';
  import Plotly, { getDataToPixel } from 'plotly.js-dist';

  import { dbData as dbDataStore } from '../../stores';
    import App from '../../App.svelte';

  let container;

  async function renderPlot(dbData) {
    const data = [];
    for (const [panelName, xy] of Object.entries(dbData)) {
      data.push({
        name: `${panelName} (kWh)`,
        ...xy,
      });
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
      renderPlot(await promise);
    });
  });
</script>
  
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
</style>