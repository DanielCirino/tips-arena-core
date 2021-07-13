class Error(Exception):
  """
  Classe base para erros da aplicação
  Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
  """

  def __init__(self, expression=None, message=None):
    self.expression = expression
    self.message = message
