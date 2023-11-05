<script>
  import Nav from "./components/nav/Nav.svelte"
  import Home from "./components/home/Home.svelte"
  import Footer from "./components/footer/Footer.svelte"
  import Graph from "./components/graph/Graph.svelte"
  import LoadingDialog from "./components/loadingdialog/LoadingDialog.svelte"
</script>

<main>
  <LoadingDialog />
  <Nav />
  <Home />
  <Graph />
  <Footer />
</main>

<style>
  
</style>
