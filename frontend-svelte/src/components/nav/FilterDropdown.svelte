<script>
    import { fly } from "svelte/transition";
    import { ANIMATE_OUT_LOADING_TIME, ANIMATE_DURATION } from "../../animationTimings";
import { dbData as dbDataStore, panelName as panelNameStore, readyToAnimate } from "../../stores";
let panelNames = [];
let isLoading = true;
dbDataStore.subscribe(async x => {
    panelNames = Object.keys((await x) || {});
    isLoading = false;
});
function updatePanelNameStore(event) {
    panelNameStore.set(event.target.value);
}
const flyOptions = {
    x: 100,
    duration: ANIMATE_DURATION,
};
const flyOptionsFilter = {
    ...flyOptions,
    delay: ANIMATE_OUT_LOADING_TIME,
}
</script>

<div class="filter-panel-widget">
    {#if !isLoading}
        <div in:fly={flyOptionsFilter} on:introend={() => readyToAnimate.set(true)}>
            <select on:change={updatePanelNameStore}>
                <option value="all">All Panels</option>
                {#each panelNames as panelName}
                <option value="{panelName}">{panelName}</option>
                {/each}
            </select>
        </div>
    {/if}
</div>

<style>

.filter-panel-widget select {
    padding: 10px;
    font-size: 16px;
    cursor: pointer;
    border: none;
    border-radius: 4px; 
    background-color: var(--couillard-orange-color);
}
</style>
