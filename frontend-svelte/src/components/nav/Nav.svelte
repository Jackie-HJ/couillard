<script>
    import FilterDropdown from "./FilterDropdown.svelte";

</script>
<div class="header">
    <img src="logo.jpg" alt="Logo">
    <h1 >Deerfield Solar Analytics</h1>
    <FilterDropdown />
</div>

<style> 
.header {
    background-color: white;
    width: 100%;
    padding-bottom: 10px;
}


h1 {
    font-size: 40px;
    color: var(--couillard-blue-color);
    padding: 0;
    text-align: center;
}

@media(max-width: 640px) {
    h1 {
        font-size: 20px;
    }
}

img {
    position: absolute;
    top: 6px;
    left: 6px;
    width: 80px;
    height: 80px;
}

@media(max-width: 760px) {
    img {
        width: 40px;
        height: 40px;
    }
}

</style>