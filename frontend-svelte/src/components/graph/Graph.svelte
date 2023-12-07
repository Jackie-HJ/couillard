<script>
  import { onMount } from 'svelte';
  // @ts-ignore
  import Plotly from 'plotly.js-dist';

  import { dbData as dbDataStore, panelName as panelNameStore, LBS_CO2_PER_KWH, DOLLARS_SAVED_PER_KWH } from '../../stores';
    import { fly } from 'svelte/transition';

  let container;
  let selectedPanelDescription = "";
  let selectedPanelUrl = "";
  let selectedPanelImageUrl = "";
  let dbData= {};

  let panelInfoSection;
  let panelInfoImage;

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

  let wScrollY;
  let alreadyScrolledDown = false;


  $: {
    if (wScrollY > 0) {
      if (selectedPanelImageUrl != "") {
        let top = panelInfoImage.getBoundingClientRect().top;
        let bot = top + panelInfoImage.getBoundingClientRect().height;
        if (((top + bot) / 2) < window.innerHeight) {
          alreadyScrolledDown = true;
        }
      }
    }
  };
  
</script>

<svelte:window bind:scrollY={wScrollY} />

<section>
  <div class="graph-auxillary-box">
    <div class="unit-changer graph-aux">
      Change Units of Graph:
      <div class="buttons">
        <button on:click={showKwhData}>kWh</button>
        <button on:click={showLbsCO2Data}>lbs CO2</button>
        <button on:click={showDollarData}>Dollars</button>
      </div>
    </div>
      
    <div class="explanations graph-aux">
      <p>
        <strong>To zoom,</strong> scroll up or down.
        <strong>To pan,</strong> click and drag.<br>
        <strong>To select specific panels,</strong> click on their entries in the legend.
      </p>
    </div>
  
    <div class="more-details graph-aux">
      {#if selectedPanelUrl}
        <a href={selectedPanelUrl}>
          <button>More Details</button>
        </a>
      {:else}
        <button disabled>Select a Panel...</button>
      {/if}
    </div>
  </div>
  <div bind:this={container}></div>
</section>

<section bind:this={panelInfoSection}>
  <div class="description-wrapper">
    <div class="description-flex">
      <div class="description">
        {#if selectedPanelDescription}
          <p>{selectedPanelDescription}</p>
        {/if}
      </div>
    </div>
    <div class="description-flex">
      <div class="description" bind:this={panelInfoImage}>
        {#if selectedPanelImageUrl}
          <img src={selectedPanelImageUrl} alt={`Picture of ${selectedPanelName} Array`}>
        {/if}
      </div>
    </div>
  </div>
</section>

{#if selectedPanelDescription && !alreadyScrolledDown}
<div class="panel-info">
  <button
    on:click={() => panelInfoSection.scrollIntoView({
      behavior: 'smooth',
    })}
    in:fly={{y: 200}}
    out:fly={{y: 200}}
  >More details below...</button>
</div>
{/if}

<style>

  .panel-info {
    position: fixed;
    bottom: 10px;
    width: 100%;
    margin-left: auto;
    margin-right: auto;
    opacity: 50%;
  }
  
  .panel-info button {
    background-color: gray;
    font-size: 18pt;
  }

  section {
    color: var(--couillard-blue-color);
  }

  .graph-auxillary-box {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    align-items: center;
  }

  .graph-aux {
    margin: 26px; /* This is what Plotly uses, this way it lines up */
    margin-bottom: 0;
  }

  .unit-changer {
    margin-right: auto;
  }

  .more-details {
    margin-left: auto;
  }

  .description-wrapper {
    display: grid;
    grid-template-columns: 2fr 1fr;
  }

  .description-flex {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .description {
    text-align: center;
    container-type: normal;
    container-name: description-container;
  }

  .description p {
    margin: 0px;
    padding: 50px;
    font-size: 18px;
    font-weight: bold;
  }

  .description img {
    max-width: 33.3vw;
    padding: 50px;
  }

  a {
    color: var(--couillard-blue-color);
    text-decoration: underline;
  }

</style>
