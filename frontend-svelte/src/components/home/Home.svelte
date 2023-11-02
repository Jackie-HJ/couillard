<script>
    import { onMount } from 'svelte';
  import { totalData } from '../../stores';

  let totals = { original: 0, derived: [], };
  onMount(() => {
    totalData.subscribe(async promise => {
      totals = await promise;
    });
  });

  const compactNumberFormatter = Intl.NumberFormat('en', {
    notation: 'compact',
    maximumSignificantDigits: 4,
  });
  const fmtNum = x => compactNumberFormatter.format(x);
</script>

<div class="stats-row">
    Solar panels have saved, to date:
  <div class="row-arrange">
    {#each totals.derived as [conv, unit, showDesc]}
      <div class="statistic">
          <p class="large">{(unit[0] === "$" ? "$" : "")}{fmtNum(conv * totals.original)}</p>
          <p class="medium">{unit[0] === "$" ? unit.slice(1) : unit}</p>
          {#if showDesc}
            <p class="small">
              *Based on {(unit[0] === "$" ? "$" : "")}{conv}
              {unit[0] === "$" ? unit.slice(1) : unit} per kWh
            </p>
          {/if}
      </div>
    {/each}
  </div>
</div>

<style>
  .info-title {
  font-size: 36px;
  font-weight: bolder;
  color: black;
}


.stats-row {
  margin-top: 50px;
  color: white;
  font-weight: bold;
  font-size: x-large;
  background-color: var(--couillard-blue-color);
  text-align: center;
  padding: 20px;
  font-size: 24px;
}

.row-arrange {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  padding: 20px;
}

.statistic {
  text-align: center;
  border: 10px white;
  color: white;
}

.large {
  font-size: 4rem;
}

.medium {
  font-size: 2rem;
}

.small {
  font-size: 1rem;
}
</style>