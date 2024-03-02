<script>
    import { onMount } from 'svelte';
    import { totalData } from '../stores';

    let isLoading = true;
    onMount(() => {

        totalData.subscribe(async x => {
            await x;
            isLoading = false;
        });
    });

    // I spent so long getting this to work. 
    // For some reason I will never in my life understand
    // Firefox (maybe other browsers idk) won't create
    // the backdrop for a <dialog> if you tell it to be open
    // by default. 
    // It seems like you should be able to just do <dialog open>
    // instead of this nonsense, but doing that will break everything. 
    // Now you, just like me, won't be able to sleep tonight. 
    // Constantly wondering why on earth they don't create a backdrop
    // for an open-by-default modal. 
    // Forever wandering in circles in our own minds....
    // Wait why do we even need a backdrop? Well it turns out that the
    // default one is to slightly dim the rest of the page, but backdrops
    // in most browsers can't be animated. This means that if we animate
    // the dialog out, the backdrop will suddenly just yeet itself away. 
    // This looks like crap, so we supply our own backdrop which is just
    // actually transparent and therefore invisible. 
    function showImmediately(domnode) {
        domnode.showModal();
    }

    import { fade } from 'svelte/transition';
    import { ANIMATE_OUT_LOADING_TIME } from "../animationTimings"
</script>

{#if isLoading}
    <dialog class="dialog_inner" use:showImmediately out:fade={{ duration: ANIMATE_OUT_LOADING_TIME }}>
        <div class="dialog_flex">
            <span class="dialog_text">Loading panel data...</span>
        </div>
    </dialog>
{/if}

<style>
dialog {
    --dialog-color: black;
    overflow: hidden;
    border: none;
}

.dialog_inner {
    font-size: 40pt;
    color: var(--dialog-color);
    background-color: var(--dialog-color);
    border-radius: 20px;
}

.dialog_text {
    color: white;
}

dialog::backdrop {
    background-color: rgba(0, 0, 0, 0);
}

dialog::after {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  bottom: -50%;
  left: -50%;
  background: linear-gradient(
    to bottom,
    rgb(0, 0, 0, 0),
    rgba(255,255,255,0.5) 50%,
    rgba(0, 0, 0, 0)
  );
  transform: rotateZ(-60deg) translate(1em, -9em);
}

dialog::before, dialog::after {
    animation: sheen 0.5s forwards;
}

@keyframes sheen {
  100% {
    transform: rotateZ(-60deg) translate(-5em, 7.5em);
  }
}

.dialog_flex {
    align-items: center;
    display: flex;
    justify-content: center;
}
</style>
