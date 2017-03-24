from uncertainpy import Parameters

class Model():
    """
The model must be able to handle these calls

simulation.run()


If you create your own model it must either be in it's own file
or the main part of the program must be inside

if __name__ == "__main__":
    # Main part of the program here

Run must store the results from the simulation in self.t and self.U
    """


    def __init__(self,
                 parameters=None,
                 adaptive_model=False,
                 xlabel="",
                 ylabel=""):
        """

----------
Required arguments

parameters: Parameters object | list of Parameter objects | list [[name, value, distribution],...]


    On the form:
    parameters = Parameters Object
    or
    parameters = [[name1, value1, distribution1],
                  [name2, value2, distribution2],
                     ...]
        name: str
            Name of the parameter
        value: number
            Value of the parameter
        distribution: None | Chaospy distribution | Function that returns a Chaospy distribution
            The distribution of the parameter.
            A parameter is considered uncertain if if has a distributiona associated
            with it.

    or
    parameters = [ParameterObject1, ParameterObject2,...]
        """

        self.adaptive_model = adaptive_model

        self.xlabel = xlabel
        self.ylabel = ylabel

        if isinstance(parameters, Parameters) or parameters is None:
            self.parameters = parameters
        elif isinstance(parameters, list):
            self.parameters = Parameters(parameters)
        else:
            raise ValueError("parameter argument has wrong type")



    def setDistribution(self, parameter_name, distribution_function):
        if self.parameters is None:
            raise AttributeError("Parameters is not in the model")

        self.parameters.setDistribution(parameter_name, distribution_function)


    def setAllDistributions(self, distribution_function):
        if self.parameters is None:
            raise AttributeError("Parameters are not in the model")

        self.parameters.setAllDistributions(distribution_function)



    def run(self, parameters):
        """
        Run must return t, U
        """
        raise NotImplementedError("No run() method implemented")
