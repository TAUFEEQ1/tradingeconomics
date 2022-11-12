from flask import Flask, abort
from flask import render_template,request
import tradingeconomics as te
from os import getenv
from typing import List, TypedDict
from collections import defaultdict
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

appl = Flask(__name__)
API_KEY = getenv("API_KEY")

te.login(API_KEY)
# supported names
SUPPORTED_COUNTRIES = ['thailand', 'mexico', 'sweden', 'new zealand']
INDICATORS = ['gdp', 'inflation rate', 'population']


class Country(TypedDict):
    name: str
    gdp: float
    inflation: float
    inflation_since: str
    gdp_per_capita: float
    popn: float


class CountryNews(TypedDict):
    title: str
    description: str
    date: str

# COUNTRY GDP BY CONTINENT


@appl.route("/", methods=['GET'])
def countries():
    country_df: pd.DataFrame = te.getIndicatorData(
        indicators=INDICATORS, output_type='df', country=SUPPORTED_COUNTRIES)
    rows = country_df.to_dict(orient='records')
    items = defaultdict(dict)
    for row in rows:
        if row["Category"] == "GDP":
            items[row["Country"]].update({"gdp": row["LatestValue"]})
        if row["Category"] == "Inflation Rate":
            items[row["Country"]].update(
                {"inflation": row["LatestValue"], "inflation_since": row["PreviousValueDate"].split("T")[0]})
        if row["Category"] == "Population":
            items[row["Country"]].update({"popn": row["LatestValue"]})

    def per_capita(k, v): return Country(
        v, gdp_per_capita=v["gdp"]*1000/v["popn"], name=k)
    results: List[Country] = [per_capita(k, v) for k, v in items.items()]
    return render_template("index.jinja", countries=results)


@appl.route("/news", methods=['GET'])
def news():
    country = request.args.get("country","Mexico")
    if country.lower() not in SUPPORTED_COUNTRIES:
        abort(404)
    news_df: pd.DataFrame = te.getNews(
        country=country, output_type='df')
    rows = news_df.to_dict(orient='records')
    items = list()
    for row in rows[1:]:
        items.append(
        CountryNews(title=row["title"], description=row["description"],date=row["date"].split("T")[0]))
    
    return items

@appl.route("/history", methods=['GET'])
def history():
    country = request.args.get("country","Mexico")
    # get historical data (gdp+inflation)
    if country.lower() not in SUPPORTED_COUNTRIES:
        abort(404)
    country_df: pd.DataFrame = te.getHistoricalData(
        country=country, indicator='gdp',output_type='df')
    country_df.dropna(inplace=True)
    country_df["DateTime"] = country_df["DateTime"].str.split("T").str.get(0)
    rows = country_df.sort_values(by=['DateTime']).to_dict(orient='records')
    return [{'date':row["DateTime"],'value':row["Value"]} for row in rows if row["DateTime"] is not None]
