# Can remove the fitted parameter and test if the parameter has a distribution function?

class Parameters():
    def __init__(self, parameters, distributions, fitted_parameters):
        """
        parameters: dict of all the default parameters the model has
        fitted_parameters: list of all parameters that shall be examined
        distribution_function: Either a function for all parameters, or a dictionary
                               with the distribution for each parameter
        """

        self.parameters = {}
        self.parameter_space = None
        self.dist = None

        if type(fitted_parameters) is str:
            self.fitted_parameters = [fitted_parameters]
        else:
            self.fitted_parameters = fitted_parameters


        if hasattr(distributions, '__call__'):
            for param in parameters:
                self.parameter[param] = Parameter(param, parameters[param],
                                                  distributions, param in fitted_parameters)
        else:
            for parameter in parameters:
                if parameter in fitted_parameters:
                    self.parameters[parameter] = Parameter(parameter, parameters[parameter],
                                                           distributions[parameter], True)
                else:
                    self.parameters[parameter] = Parameter(parameter, parameters[parameter])


    # def parameterSpace(self):
    #     """
    #     Generalized parameter space creation
    #     """
    #     if self.parameter_space is not None:
    #         return self.parameter_space
    #
    #     self.parameter_space = []
    #     for parameter in self.parameters:
    #         if self.parameters[parameter].fitted:
    #             self.parameter_space.append(self.parameters[parameter].parameter_space)
    #
    #     return self.parameter_space


    def getIfFitted(self, item):
        items = []
        for parameter in self.parameters.values():
            if parameter.fitted:
                items.append(getattr(parameter, item))
        return items


    def get(self, item):
        if item in self.parameters.keys():
            return self.parameters[item]

        return [getattr(parameter, item) for parameter in self.parameters.values()]


class Parameter():
    def __init__(self, name, value, distribution_function=None, fitted=False):

        self.name = name
        self.value = value
        self.distribution_function = distribution_function
        self.fitted = fitted

        if self.fitted:
            self.parameter_space = self.distribution_function(self.value)
