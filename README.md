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

How to do this?

1. Eliminate things in parentheses, they aren't consistent.

  ```bash
  1 1/2 cup chopped green pepper
  ```

2. Then convert measurement names to standardized measurement names (e.g. `teaspoons -> tsp, cup -> cups, gallons -> gal, ...`). Longer names are preferable because they can be easier search/replaced.

  ```bash
  1 1/2 cups chopped green pepper
  ```

1. Reverse string. Find the *shortest length* string in the `sr28` database that *matches best* to the recipe item. Ideally, this would be `green pepper`. Then eliminate that from the recipe item, so now your left with:

  `1 1/2 cups chopped`

2. Now find the best match to the string in the measurement array. This should match `cup`. Then eliminate that so your left with:

  `1 1/2 chopped`

3. Now all up all the numbers, taking note of partial fractions and return:

  ```json
  {
    "quantity":"1.5",
    "measurement":"cups",
    "ingredient":"green pepper",
    "sr28":"1239810"
  }
  ```

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
