class FunctionWithDerivative:

    def value(self, x):
        raise NotImplementedError("Subclasses should implement this method.")

    def derivative(self, x):
        raise NotImplementedError("Subclasses should implement this method.")
