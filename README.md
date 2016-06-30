# parseingredient
An ingredient parser written in Golang


## Notes

`id` = `hash(frozenset(ingredients + directions))`

## Todo

- [ ] Ingredient parser (using NYTimes phrase-tagger)
- [ ] Unit converter
- [ ] Recipe extractors


### Recipe Parser v1

Given a recipe item,

```bash
1 1/2 cup (4 oz) chopped green pepper
```

it will return

```json
{
  "quantity":"1.5",
  "measurement":"cups",
  "ingredient":"green pepper"
}
```

How to do this? Use [NYtimes Ingredient phrase tagger](https://github.com/schollz/ingredient-phrase-tagger)

1. Make a file with the line. `input.txt`:
```
1 1/2 cup (4 oz) chopped green pepper
```
2. From the directory of the NYtimes Ingredient phrase tagger, `python lib/testing/parse-ingredients.py input.txt > input_formatted.txt &&  python lib/testing/convert-to-json.py input_formatted.txt`

### Unit converter v1

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
