<script>
  import { onMount } from 'svelte';
  import Plotly from 'plotly.js-dist';

  let container;

  onMount(() => {
    const data = [{
      x: [1, 2, 3, 4, 5],
      y: [1, 2, 4, 8, 16]
    }];

    const layout = {
      title: 'Sample Graph',
      xaxis: {
        title: 'X Axis'
      },
      yaxis: {
        title: 'Y Axis'
      }
    };

    const config = {
      responsive: true
    };

    Plotly.newPlot(container, data, layout, config);
  });
</script>
  
<div bind:this={container}></div>
  