<script>
  import { onMount } from 'svelte';
  import { totalData, selectedPanelStore } from '../../stores';
  import { TOTALS_DERIVATIONS, FORMATTING_LOCALE, CURRENCY } from '../../conversions';

  let totals = 0;
  onMount(() => {
    totalData.subscribe(async promise => {
      totals = await promise;
    });
  });

  const SIG_CHARS = 5;
  
  const compactNumberFormatter = Intl.NumberFormat(FORMATTING_LOCALE, {
    notation: 'compact',
    maximumSignificantDigits: SIG_CHARS - 1,
  });
  const siNumberFormatter = Intl.NumberFormat(FORMATTING_LOCALE, {
    notation: 'compact',
    maximumSignificantDigits: SIG_CHARS,
  })
  const moneyFormatterNoDP = Intl.NumberFormat(FORMATTING_LOCALE, {
    style: 'currency',
    currency: CURRENCY,
    maximumFractionDigits: 0,
    minimumFractionDigits: 0,
  });
  const moneyFormatter = Intl.NumberFormat(FORMATTING_LOCALE, {
    style: 'currency',
    currency: CURRENCY,
  });
  const broke = moneyFormatter.format(0);
  const currencySymbol = broke.replaceAll("0", "").replaceAll(".", "");
  function pickSiPrefix(num, just) {
    let everything = siNumberFormatter.format(num).replace("K", "k");
    let prefixless = !(/[A-Za-z]$/.test(everything));
    switch (just) {
      case "prefix":
        if (prefixless) return "";
        return everything.slice(-1);
      case "number":
        if (prefixless) return everything;
        return everything.slice(0, -1);
      default:
        console.warn("Returning undefined SI prefix, withOrWithout must be prefix or number.");
    }
  }
  function fmtNum(num, unitType, currencyShowDP = false) {
    switch (unitType) {
      case "money":
        return (
          currencyShowDP ? moneyFormatter : moneyFormatterNoDP
        ).format(num);
      case "si":
        return pickSiPrefix(num, "number");
      case "simple":
      default:
        let result = compactNumberFormatter.format(num);
        if (unitType !== "simple") {
          console.warn(`Unknown unit type ${unitType}, defaulting to simple.`);
        }
        return result;
    }
  }
  function fmtUnit(num, unit, unitType, shortForm = false) {
    switch (unitType) {
      case "money":
        if (shortForm) return unit;
        return `${currencySymbol} ${unit}`;
      case "si":
        let siPrefix = pickSiPrefix(num, "prefix");
        return `${siPrefix}${unit}`;
      case "simple":
      default:
        if (unitType !== "simple") {
          console.warn(`Unknown unit type ${unitType}, defaulting to simple.`);
        }
        return unit;
    }
  }
</script>

<div class="stats-row">
    Since we started tracking, {$selectedPanelStore ? `the ${$selectedPanelStore} array has` : "solar arrays in Deerfield have"} saved:
  <div class="row-arrange">
    {#each TOTALS_DERIVATIONS as [conv, unit, unitType, showDesc]}
      <div class="statistic">
          <p class="large">{fmtNum(conv * totals, unitType)}</p>
          <p class="medium">{fmtUnit(conv * totals, unit, unitType)}</p>
          {#if showDesc}
            <p class="small">
              *Based on {fmtNum(conv, unitType, true)}
              {fmtUnit(conv, unit, unitType, true)} per kWh
            </p>
          {/if}
      </div>
    {/each}
  </div>
  <p class="tiny">*many of our arrays have been operational for much longer than the data reflects, so these numbers are <b>underestimates</b> by a large margin!</p>
</div>

<style>
/* currently unused
  .info-title {
    font-size: 36px;
    font-weight: bolder;
    color: black;
  }
*/

.stats-row {
  margin-top: 0px;
  color: white;
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
  padding: 0px;
  font-weight: bold;
}

.large {
  font-size: 4rem;
  margin: 0%;
  font-weight: bold;
}

.medium {
  font-size: 2rem;
  margin: 0%;
}

.small {
  font-size: 1rem;
  margin: 0%;
}

.tiny {
  font-size: 0.7rem;
  margin: 0%;
}

</style>