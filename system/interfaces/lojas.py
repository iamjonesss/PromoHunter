from abc import ABC, abstractmethod

class InteracaoLojasInterface(ABC):
    """ Interface voltada para interação com diferentes lojas online via API. """
    
    @abstractmethod
    def buscar_produtos(self, termo_busca: str):
        """ Método responsável por buscar produtos em determinada loja online via API. """
        pass
