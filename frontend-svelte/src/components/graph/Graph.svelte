<script>
  import { onMount } from 'svelte';
  import Plotly, { getDataToPixel } from 'plotly.js-dist';

  import { dbData as dbDataStore } from '../../stores';

  let container;

  async function renderPlot(dbData) {
    const data = [
      dbData["Kelly Lane"],
    ];

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
    dbDataStore.subscribe(renderPlot);
  });
</script>
  
<div bind:this={container}></div>
  