<script>
  import Nav from "./components/nav/Nav.svelte"
  import Home from "./components/home/Home.svelte"
  import Footer from "./components/footer/Footer.svelte"
  import Graph from "./components/graph/Graph.svelte"
  import LoadingDialog from "./components/loadingdialog/LoadingDialog.svelte"

  import { totalData, readyToAnimate } from "./stores"
  import { ANIMATE_OUT_LOADING_TIME, ANIMATE_DURATION } from "./animationTimings"


  import { onMount } from "svelte";
  import { fly } from "svelte/transition";

  let notReadyYet = true;
  onMount(() => {
    readyToAnimate.subscribe(x => {
      if (x) notReadyYet = false;
    })
  });
  
  let homeInPlace = false;
  let graphInPlace = false;
  let footerInPlace = false;

  const flyOptions = {
    y: 200,
    duration: ANIMATE_DURATION,
  };
  const flyOptionsFirst = {
    ...flyOptions,
    delay: ANIMATE_OUT_LOADING_TIME,
  }
</script>

<main>
  <LoadingDialog />
  <Nav />
  {#if !notReadyYet}
    <div in:fly={flyOptionsFirst} on:introend={() => { homeInPlace = true; }}>
      <Home />
    </div>
  {/if}
  {#if !notReadyYet && homeInPlace}
    <div in:fly={flyOptions} on:introend={() => { graphInPlace = true; }}>
      <Graph />
    </div>
  {/if}
  {#if !notReadyYet && graphInPlace}
    <div in:fly={flyOptions} on:introend={() => { footerInPlace = true; }}>
      <Footer />
    </div>
  {/if}
</main>

<style>
  
</style>
