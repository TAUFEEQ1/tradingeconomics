/**
 * @typedef Country
 * @property {number} gdp_per_capita
 */
/**
 * 
 * @param {any} ctx
 * @param {Country[]} data 
 * 
 */
function drawPerCapitaChart(ctx,config){
    const myChart = new Chart(ctx,config);
    return myChart;
}
