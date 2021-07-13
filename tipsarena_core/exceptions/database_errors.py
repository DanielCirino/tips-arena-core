from . import Error


class ConexaoError(Error): pass


class InserirDocumentoError(Error): pass


class AtualizarDocumentoError(Error): pass


class InserirOuAtualizarDocumentoError(Error): pass


class InserirOuAtualizarDocumentosEmLoteError(Error): pass


class DeletarDocumentoError(Error): pass


class ListarDocumentosError(Error): pass


class TotalDocumentosError(Error): pass


class ObterDocumentoError(Error): pass


class AgregarDadosError(Error): pass


class PesquisaTextoError(Error): pass


class CriarIndiceError(Error): pass
