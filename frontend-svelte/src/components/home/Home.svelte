<script>
  import { onMount } from 'svelte';
  import { totalData, panelName } from '../../stores';
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
  function fmtNum(num, unitType, forceHigherPrecision = false) {
    switch (unitType) {
      case "money":
        return (
          forceHigherPrecision ? moneyFormatter : moneyFormatterNoDP
        ).format(num);
      case "si":
        return pickSiPrefix(num, "number");
      case "expanded":
        return forceHigherPrecision ? num.toLocaleString() : Math.floor(num).toLocaleString();
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
        if (shortForm) return "";
        return unit;
      case "si":
        let siPrefix = pickSiPrefix(num, "prefix");
        return `${siPrefix}${unit}`;
      case "simple":
      case "expanded":
        return unit;
      default:
        console.warn(`Unknown unit type ${unitType}, defaulting to simple.`);
        return unit;
    }
  }
</script>

<div class="stats-row">
    Since we started tracking {($panelName !== "all") ? `the ${$panelName} Array` : "solar arrays in Deerfield"}...
  <div class="row-arrange">
    {#each TOTALS_DERIVATIONS as [conv, unit, unitType, unitSuffix, showDesc]}
      <div class="statistic">
          <p class="large">{fmtNum(conv * totals, unitType)}</p>
          <p class="medium statistic-detail">
            {#if unit === "" && unitSuffix === ""}
              <div class="invisible-placeholder">X</div>
            {:else}
              {fmtUnit(conv * totals, unit, unitType)} {unitSuffix}
            {/if}
          </p>
          {#if showDesc}
            <p class="small statistic-detail">
              *Based on {fmtNum(conv, unitType, true)}
              {fmtUnit(conv, unit, unitType, true)} {unitSuffix.toLowerCase()} per kWh
            </p>
          {/if}
      </div>
    {/each}
  </div>
  <p class="tiny">*many of our arrays have been operational for much longer than the data reflects, so these numbers are <b>underestimates</b> by a large margin!</p>
</div>

<style>
/* UNUSED .info-title {
  font-size: 36px;
  font-weight: bolder;
  color: black;
} */


.stats-row {
  margin-top: 0px;
  color: white;
  font-size: x-large;
  background-color: var(--couillard-blue-color);
  text-align: center;
  padding: 20px;
  font-size: 24px;
}

.invisible-placeholder {
  visibility: hidden;
}

.row-arrange {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  padding: 80px;
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