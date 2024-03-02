<script>
  import { onMount } from 'svelte';
  // @ts-ignore
  import Plotly from 'plotly.js-dist';

  import { dbData as dbDataStore, panelName as panelNameStore, LBS_CO2_PER_KWH, DOLLARS_SAVED_PER_KWH, totalData } from '../stores';
    import { fly } from 'svelte/transition';

  let container;
  let selectedPanelDescription = "";
  let selectedPanelUrl = "";
  let selectedPanelImageUrl = "";
  let dbData= null;

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
      dragmode: "pan"
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
  let totals = 0;
  onMount(() => {
    dbDataStore.subscribe(async promise => {
      dbData = await promise;
      showKwhData();
      isLoading = false;
    });
    totalData.subscribe(async promise => {
      totals = await promise;
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
  let wInnerWidth;
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

  $: console.log(totals)
  
</script>

<svelte:window bind:scrollY={wScrollY} bind:innerWidth={wInnerWidth} />

{#if wInnerWidth < 760}
<p class="sm-scn-msg">Visit this page on a larger screen to see graphs of daily data collected from each array</p>
{/if}
<section class={totals > 0 &&  wInnerWidth > 760 ? "" : "hidden"}>
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
          <button>View Data Source</button>
        </a>
      {:else}
        <button disabled>Select a Panel...</button>
      {/if}
    </div>
  </div>
  <div bind:this={container} class="graph-cont"></div>
</section>

<section bind:this={panelInfoSection}>
  <div class="description-wrapper">
    {#if selectedPanelImageUrl}
    <div class="description-item">
      <div class="description" bind:this={panelInfoImage}>
          <img src={selectedPanelImageUrl} alt={`Picture of ${selectedPanelName} Array`}>
      </div>
    </div>
    {/if}
    {#if selectedPanelDescription}
    <div class="description-item">
      <div class="description">
          <p>{selectedPanelDescription}</p>
      </div>
    </div>
    {/if}
  </div>
</section>

{#if selectedPanelDescription && !alreadyScrolledDown && totals > 0}
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

  .sm-scn-msg {
    text-align: center;
    color: var(--couillard-blue-color);
    padding: 6px;
  }

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
    display: flex;
    justify-content: center;
    padding: 10px;
  }

  .description-item {
    width: 50%;
  }


  @media(max-width: 760px) {
    .description-wrapper {
      flex-direction: column;
    }
    .description-item {
      width: 100%;
    }
  }

  .description {
    text-align: center;
    container-type: normal;
    container-name: description-container;
  }

  .description p {
    margin: 0px;
    padding: 10px;
    font-size: 18px;
    font-weight: bold;
  }

  .description img {
    max-width: 100%;
  }

  a {
    color: var(--couillard-blue-color);
    text-decoration: underline;
  }

  .hidden {
    opacity: 0;
    height: 0px !important;
  }
</style>
