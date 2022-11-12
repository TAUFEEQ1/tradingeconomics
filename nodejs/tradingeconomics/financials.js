'use strict'

const auth = require('./auth.js');
const func = require('./functions.js');
const fetch = require('node-fetch');

//setting global variables to be used outside this module
global.symbol = null;
global.country = null;


//This function builds the path to get the API request:
/***********************************************************************************  
   parameters:
    String or list: symbol
    String or list: country

   example:

        getFinancialsData(symbol = 'aapl:us'); 
        getFinancialsData(symbol = ['aapl:us', 'ea:us']);
        getFinancialsData(country = 'china');
        getFinancialsData(country = ['china', 'united states']);

          
***********************************************************************************/
function getFinancialsData(){
    try {
        var data_url = '';
    
        // d is a dictionary used for create the api url
        var d = {
            'url_base': 'https://api.tradingeconomics.com/financials',
            'symbol': '',
            'country': '/companies',
            'key': `?c=${apikey}`,
            'output_type' : ''
        }
        
        if (country != null && symbol == null){
            //the 'key' value has to be changed due to url enpoint use of '?' or '&' characters. 
            d.key = `&c=${apikey}`;
            d.country = `/companies?country=${country}`;
        }
        if (symbol != null && country == null) {
            d.country = '';
            d.symbol = `/symbol/${symbol}`;
        }
        data_url = `${d.url_base}${d.symbol}${d.country}${d.key}`.replace (' ', '%20');    
        
        console.log('If both "country" and "symbols" are null or not null at the same time, a full companies list will be provided ')
        return func.makeTheRequest(data_url)
        // return fetch(data_url)
        // .then(func.handleErrors)   
        // .then(function(response) {    
        //     return response.json(); // process it inside the `then` when calling the function       
        // }).catch(function (err) {
        //     return err.message;
        // });
    } catch (error) {
        throw error
    }
   
}

module.exports.getFinancialsData = getFinancialsData;










