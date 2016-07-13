# README

1. Generate JSON data for each recipe. Data will be in `finished`

  `cd src && python3 parseHTML.py /location/to/data`

2. Tag recipes. Make sure to have ingredientTagging setup in another directory (see source)

  `cd src && python3 ingredientTagging.py`

3. Generate the models and then generate the markov files

  `cd src && python3 markovRecipe.py`

## Todo

- [x] Recipe extractors
- [x] Ingredient parser (using NYTimes phrase-tagger)
- [ ] Unit converter

### Unit converter notes

Give the parsed recipe,

```json
{
  "quantity":"1.5",
  "measurement":"cups",
  "ingredient":"green pepper",
  "sr28":"1239810"
}
```

it will make the conversion to grams:

```json
{
  "quantity":"300",
  "measurement":"gram",
  "ingredient":"green pepper",
  "sr28":"1239810"
}
```

How to do this?

1. Look up ingredient in `sr28`. If found, and the weight associated with it is the same as the current weight, use that conversion, if not make a conversion to a weight associated with the `sr28`.

2. (optional) To convert the measurement, use an array of increasing measurement types:

  `[milliliter, teaspoon, tablespoon, ounce, cup, pint, quart, gallon, liter]`

  and the associated transformation array (left to right):

  `[4, 3, 2, 8, 2, 2, 4, 0.2642]`.

  For example, `4 millilter = 1 teaspoon` and `0.26452 gallon = 1 liter`. Any conversion can be made by simply traversing the array.

3. Use the `sr28` weight to convert to grams.


## Data

`data/FoodPricesDatabase0304.tab` from [here](http://www.cnpp.usda.gov/USDAFoodPlansCostofFood) which contains prices per 100 g.

`data/sr28/*` are from the [sr28 USDA database](http://www.ars.usda.gov/Services/docs.htm?docid=25700).
[Documentation is available](http://www.ars.usda.gov/SP2UserFiles/Place/80400525/Data/SR/SR28/sr28_doc.pdf).


## Relevant

http://opensourcecook.com/recipes-copyright-law
https://news.ycombinator.com/item?id=11711467
