class ConditionBuilder:
    def __init__(self,model):
        self.model = model
        self.filters = []

    def create_condition(self, **conditions):
        for key, value in conditions.items():
            self.filters.append((getattr(self.model, key) == value))
        return self.filters
