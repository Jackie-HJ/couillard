<script>
    import FilterDropdown from "./FilterDropdown.svelte";

</script>
<div class="header">
    <div class="width-define">
        <div class="link-row flex-wrapper-header">
            <div class="logo">
                <img id="logo" src="logo.jpg" width="80" alt="Logo">
                <p class="logo">Deerfield Solar Analytics</p>
            </div>
            <FilterDropdown />
        </div>
    </div>
</div>

<style> 
.header {
    background-color: white;
    display: flex;
    padding: 6px;
    padding-left: 10%;
    padding-right: 10%;
    flex-direction: column;
    justify-content: center;
}

.flex-wrapper-header {
    justify-content: space-between;
}

.logo {
    display: flex;
    align-items: center;
    padding: 5px;
    font-size: 40px;
    color: var(--couillard-blue-color); 
    border-radius: 50%;
}

#logo {
    margin-right: 10px;
    border-radius: 0%;
}

p {
    font-size: 18px;
    margin: 0px;
    font-weight: normal;
}
</style>