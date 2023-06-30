class Product:
    def __init__(self, name, unit, price):
        self.name = name
        self.unit = unit
        self.price = price

    def get_name(self):
        return self.name.replace('Daily Table ', '')

    def get_unit(self):
        return self.unit

    def get_price(self):
        return self.price

    def get_price_per_unit(self):
        return self.price/self.unit

    def get_nutritional_unit(self):
        return [self.num_servings, self.quantity, self.serving_unit, self.weight_grams]

    def get_nutrition_info(self):
        return [self.calories, self.cals_from_fat, self.total_fat, self.sat_fat, self.trans_fatty_acid, self.poly_fat, self.mono_fat, self.cholesterol, self.sodium, self.tot_carb, self.fiber, self.sugar, self.protein, self.vitamin_a, self.vitamin_c, self.calcium, self.iron]

    def set_nutrition_unit(self, num_servings, quantity, serving_unit, weight_grams):
        self.num_servings = num_servings
        self.quantity = quantity
        self.serving_unit = serving_unit
        self.weight_grams = weight_grams

    def set_nutrition(self, calories, cals_from_fat, total_fat, sat_fat, trans_fatty_acid, poly_fat, mono_fat, cholesterol, sodium, tot_carb, fiber, sugar, protein, vitamin_a, vitamin_c, calcium, iron):
        self.calories = calories
        self.cals_from_fat = cals_from_fat
        self.total_fat = total_fat
        self.sat_fat = sat_fat
        self.trans_fatty_acid = trans_fatty_acid
        self.poly_fat = poly_fat
        self.mono_fat = mono_fat
        self.cholesterol = cholesterol
        self.sodium = sodium
        self.tot_carb = tot_carb
        self.fiber = fiber
        self.sugar = sugar
        self.protein = protein
        self.vitamin_a = vitamin_a
        self.vitamin_c = vitamin_c
        self.calcium = calcium
        self.iron = iron