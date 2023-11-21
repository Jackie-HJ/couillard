<script>
  import Nav from "./components/nav/Nav.svelte"
  import Home from "./components/home/Home.svelte"
  import Footer from "./components/footer/Footer.svelte"
  import Graph from "./components/graph/Graph.svelte"
  import LoadingDialog from "./components/loadingdialog/LoadingDialog.svelte"

  import { totalData } from "./stores"
  import { ANIMATE_OUT_LOADING_TIME } from "./animationTimings"


  import { onMount } from "svelte";
  import { fly } from "svelte/transition";

  let isLoading = true;
  onMount(() => {
    totalData.subscribe(async x => {
      await x;
      isLoading = false;
    })
  });
  
  let homeInPlace = false;
  let graphInPlace = false;
  let footerInPlace = false;

  const flyOptions = {
    y: 200,
  };
  const flyOptionsFirst = {
    ...flyOptions,
    delay: ANIMATE_OUT_LOADING_TIME,
  }
</script>

<main>
  <LoadingDialog />
  <Nav />
  {#if !isLoading}
    <div in:fly={flyOptionsFirst} on:introend={() => { homeInPlace = true; }}>
      <Home />
    </div>
  {/if}
  {#if !isLoading && homeInPlace}
    <div in:fly={flyOptions} on:introend={() => { graphInPlace = true; }}>
      <Graph />
    </div>
  {/if}
  {#if !isLoading && graphInPlace}
    <div in:fly={flyOptions} on:introend={() => { footerInPlace = true; }}>
      <Footer />
    </div>
  {/if}
</main>

<style>
  
</style>
