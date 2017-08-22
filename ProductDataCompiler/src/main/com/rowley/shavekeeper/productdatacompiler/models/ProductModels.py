

class ItemBase:
    brand = str
    model = str

    def __init__(self, brand=str, model=str):
        self.brand = brand
        self.model = model


class PreShave(ItemBase):

    def __init__(self, brand=str, model=str):
        ItemBase.__init__(self, brand, model)


class Soap(ItemBase):

    def __init__(self, brand=str, model=str):
        ItemBase.__init__(self, brand, model)


class Brush(ItemBase):

    def __init__(self, brand=str, model=str):
        ItemBase.__init__(self, brand, model)


class Razor(ItemBase):
    razor_type = str
    uses_blade = bool
    is_adjustable = bool

    def __init__(self, brand=str, model=str, razor_type=str, uses_blade=bool, is_adjustable=bool):
        ItemBase.__init__(self, brand, model)
        self.razor_type = razor_type
        self.uses_blade = uses_blade
        self.is_adjustable = is_adjustable


class Blade(ItemBase):

    def __init__(self, brand=str, model=str):
        ItemBase.__init__(self, brand, model)


class PostShave(ItemBase):

    def __init__(self, brand=str, model=str):
        ItemBase.__init__(self, brand, model)


class AfterShave(ItemBase):

    def __init__(self, brand=str, model=str):
        ItemBase.__init__(self, brand, model)
