<script lang="ts">
    import { onMount } from 'svelte';
    import { dbData } from '../../stores';

    let isLoading = true;
    onMount(() => {
        dbData.subscribe(_ => {
            isLoading = false;
        });
    });
</script>

{#if !isLoading}
    <dialog>
        I do be loading
    </dialog>
{/if}
