<script>
    import { onMount } from 'svelte';
    import { dbData } from '../../stores';

    let isLoading = true;
    onMount(() => {
        dbData.subscribe(async x => {
            await x;
            isLoading = false;
        });
    });
</script>

{#if isLoading}
    <dialog open class="dialog_inner">
        <div class="dialog_flex">
            Loading panel data...
        </div>
    </dialog>
{/if}

<style>
.dialog_inner {
    font-size: 20pt;
    transform: translateY(10px);
}

.dialog_flex {
    align-items: center;
    display: flex;
    justify-content: center;
}
</style>
