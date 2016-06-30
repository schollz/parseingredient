# parseingredient
An ingredient parser written in Golang


## Notes

`id` = `hash(frozenset(ingredients + directions))`

## Todo

- [ ] Recipe item parser
- [ ] Unit converter


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

2. From the directory of the NYtimes Ingredient phrase tagger, `python lib/testing/parse-ingredients.py input.txt > input_formatted.txt`. This will give something like this:

```bash
-> % cat input_formatted.txt
# 0.547990
1$1/2   I1      L12     NoCAP   NoPAREN B-QTY/0.975233
cup     I2      L12     NoCAP   NoPAREN B-UNIT/0.985440
(       I3      L12     NoCAP   YesPAREN        B-COMMENT/0.791638
4       I4      L12     NoCAP   YesPAREN        I-COMMENT/0.790899
oz      I5      L12     NoCAP   YesPAREN        I-COMMENT/0.951383
)       I6      L12     NoCAP   YesPAREN        I-COMMENT/0.874149
chopped I7      L12     NoCAP   NoPAREN I-COMMENT/0.976875
green   I8      L12     NoCAP   NoPAREN B-NAME/0.845135
pepper  I9      L12     NoCAP   NoPAREN I-NAME/0.858413
```

3. Then `crf_test -m tmp/model_file input_formatted.txt`, which will give something like this:

```bash
-> % crf_test -m tmp/model_file input_formatted.txt
1$1/2   I1      L12     NoCAP   NoPAREN B-QTY/0.975233  B-QTY
cup     I2      L12     NoCAP   NoPAREN B-UNIT/0.985440 B-UNIT
(       I3      L12     NoCAP   YesPAREN        B-COMMENT/0.791638      B-COMMENT
4       I4      L12     NoCAP   YesPAREN        I-COMMENT/0.790899      I-COMMENT
oz      I5      L12     NoCAP   YesPAREN        I-COMMENT/0.951383      I-COMMENT
)       I6      L12     NoCAP   YesPAREN        I-COMMENT/0.874149      I-COMMENT
chopped I7      L12     NoCAP   NoPAREN I-COMMENT/0.976875      I-COMMENT
green   I8      L12     NoCAP   NoPAREN B-NAME/0.845135 B-NAME
pepper  I9      L12     NoCAP   NoPAREN I-NAME/0.858413 I-NAME
```

4. The `B-QTY` is the number, `B-UNIT` is the unit, and `B-NAME/I-NAME` is the food.

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
