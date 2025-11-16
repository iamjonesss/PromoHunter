from typing import List, Dict, Any
from services.lojas import Magalu, Kabuum
from config.logger import BotLogger
from concurrent.futures import ThreadPoolExecutor
import re

class ProductSearchService:
    """Serviço para buscar e comparar produtos entre diferentes lojas."""
    
    def __init__(self):
        self.logger = BotLogger(__name__).get_logger()
        self.magalu = Magalu()
        self.kabuum = Kabuum()
        
    def _clean_price(self, price_str) -> float:
        """Converte string de preço para float."""
        if isinstance(price_str, (int, float)):
            return float(price_str)
        
        if isinstance(price_str, str):
            clean_price = re.sub(r'[^\d.,]', '', str(price_str))
            clean_price = clean_price.replace(',', '.')
            try:
                return float(clean_price)
            except (ValueError, TypeError):
                return 0.0
        
        return 0.0
    
    def _normalize_product(self, produto: Dict[str, Any], loja: str) -> Dict[str, Any]:
        """Normaliza os dados do produto para comparação."""
        price = self._clean_price(produto.get('price', 0))
        full_price = self._clean_price(produto.get('full_price', 0))
        
        return {
            'id': produto.get('id', ''),
            'name': produto.get('name', 'Produto sem nome'),
            'price': price,
            'full_price': full_price if full_price > 0 else price,
            'discount': produto.get('discount', 0),
            'brand': produto.get('brand', 'Marca não informada'),
            'availability': produto.get('availability', False),
            'url': produto.get('url', ''),
            'imageUrl': produto.get('imageUrl', ''),
            'rating': produto.get('rating', {'average': 0, 'count': 0}),
            'store': loja,
            'description': produto.get('description', ''),
            'installment': produto.get('installment', ''),
            'offer': produto.get('offer', {}),
            'payment_method': produto.get('payment_method', '')
        }
    
    async def search_products(self, termo_busca: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Busca produtos em todas as lojas disponíveis.
        
        Args:
            termo_busca: Termo para buscar produtos
            
        Returns:
            Dict com resultados de cada loja
        """
        self.logger.info(f"Iniciando busca por: {termo_busca}")
        
        resultados = {
            'magalu': [],
            'kabuum': [],
            'all_products': [],
            'search_term': termo_busca
        }
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_magalu = executor.submit(self._search_magalu, termo_busca)
            future_kabuum = executor.submit(self._search_kabuum, termo_busca)
            
            try:
                produtos_magalu = future_magalu.result(timeout=30)
                resultados['magalu'] = [self._normalize_product(p, 'Magalu') for p in produtos_magalu]
                self.logger.info(f"Magalu: {len(produtos_magalu)} produtos encontrados")
            except Exception as e:
                self.logger.error(f"Erro na busca Magalu: {e}")
                
            try:
                produtos_kabuum = future_kabuum.result(timeout=30)
                resultados['kabuum'] = [self._normalize_product(p, 'Kabuum') for p in produtos_kabuum]
                self.logger.info(f"Kabuum: {len(produtos_kabuum)} produtos encontrados")
            except Exception as e:
                self.logger.error(f"Erro na busca Kabuum: {e}")
        
        resultados['all_products'] = resultados['magalu'] + resultados['kabuum']
        
        self.logger.info(f"Total de produtos encontrados: {len(resultados['all_products'])}")
        return resultados
    
    def _search_magalu(self, termo_busca: str) -> List[Dict[str, Any]]:
        """Busca produtos na Magalu."""
        try:
            return self.magalu.buscar_produtos(termo_busca) or []
        except Exception as e:
            self.logger.error(f"Erro ao buscar na Magalu: {e}")
            return []
    
    def _search_kabuum(self, termo_busca: str) -> List[Dict[str, Any]]:
        """Busca produtos na Kabuum."""
        try:
            return self.kabuum.buscar_produtos(termo_busca) or []
        except Exception as e:
            self.logger.error(f"Erro ao buscar na Kabuum: {e}")
            return []
    
    def find_best_products(self, produtos: List[Dict[str, Any]], criterio: str = 'melhor_preco') -> List[Dict[str, Any]]:
        """
        Seleciona os melhores produtos baseado no critério escolhido.
        
        Args:
            produtos: Lista de produtos normalizados
            criterio: Critério de seleção ('melhor_preco', 'melhor_custo_beneficio', 'melhor_avaliacao')
            
        Returns:
            Lista dos melhores produtos (máximo 5)
        """
        if not produtos:
            return []
        
        produtos_validos = [
            p for p in produtos 
            if p.get('availability', False) and p.get('price', 0) > 0
        ]
        
        if not produtos_validos:
            return produtos[:3]
        
        if criterio == 'melhor_preco':
            return self._sort_by_best_price(produtos_validos)
        elif criterio == 'melhor_custo_beneficio':
            return self._sort_by_best_value(produtos_validos)
        elif criterio == 'melhor_avaliacao':
            return self._sort_by_best_rating(produtos_validos)
        else:
            return produtos_validos[:5]
    
    def _sort_by_best_price(self, produtos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ordena produtos por melhor preço."""
        return sorted(produtos, key=lambda x: x.get('price', float('inf')))[:5]
    
    def _sort_by_best_value(self, produtos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ordena produtos por melhor custo-benefício (preço + avaliação + desconto)."""
        def calculate_value_score(produto):
            price = produto.get('price', float('inf'))
            rating = produto.get('rating', {}).get('average', 0)
            rating_count = produto.get('rating', {}).get('count', 0)
            discount = produto.get('discount', 0)
            
            price_score = 1 / (price / 1000 + 1)  # Evita divisão por zero
            
            rating_score = (rating / 5.0) * min(rating_count / 10, 1.0)
            
            discount_score = min(discount / 50, 1.0)
            
            total_score = (price_score * 0.5) + (rating_score * 0.3) + (discount_score * 0.2)
            
            return total_score
        
        return sorted(produtos, key=calculate_value_score, reverse=True)[:5]
    
    def _sort_by_best_rating(self, produtos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ordena produtos por melhor avaliação."""
        def rating_score(produto):
            rating = produto.get('rating', {}).get('average', 0)
            count = produto.get('rating', {}).get('count', 0)
            return rating * min(count / 10, 1.0)
        
        return sorted(produtos, key=rating_score, reverse=True)[:5]
    
    def format_product_message(self, produto: Dict[str, Any], posicao: int = 1) -> str:
        """
        Formata um produto para exibição no Telegram.
        
        Args:
            produto: Dados do produto normalizado
            posicao: Posição na lista (para numeração)
            
        Returns:
            String formatada para o Telegram
        """
        store_emoji = {
            'Magalu': '🔵',
            'Kabuum': '🟠',
            'default': '🛍️'
        }
        
        emoji = store_emoji.get(produto.get('store', ''), store_emoji['default'])
        
        price = produto.get('price', 0)
        full_price = produto.get('full_price', 0)
        discount = produto.get('discount', 0)
        
        price_text = f"💰 **R$ {price:.2f}**"
        if full_price > price and discount > 0:
            price_text += f" ~~R$ {full_price:.2f}~~ ({discount:.0f}% OFF)"
        
        rating = produto.get('rating', {})
        rating_text = ""
        if rating.get('average', 0) > 0:
            stars = "⭐" * int(rating.get('average', 0))
            rating_text = f"\n⭐ {rating.get('average', 0)}/5 ({rating.get('count', 0)} avaliações)"
        
        # Parcelamento
        installment = produto.get('installment', '')
        installment_text = f"\n💳 {installment}" if installment else ""
        
        offer = produto.get('offer', {})
        offer_text = ""
        if offer and offer.get('name'):
            offer_text = f"\n🎉 **{offer.get('name')}** - R$ {offer.get('price', 0):.2f}"
        
        message = (
            f"{emoji} **{posicao}. {produto.get('name', 'Produto')[:80]}**\n"
            f"🏪 {produto.get('store', 'Loja')}\n"
            f"🏷️ {produto.get('brand', 'Marca não informada')}\n"
            f"{price_text}"
            f"{rating_text}"
            f"{installment_text}"
            f"{offer_text}\n"
            f"🔗 [Ver produto]({produto.get('url', '#')})\n"
        )
        
        return message
    
    def format_summary_message(self, resultados: Dict[str, Any], melhores_produtos: List[Dict[str, Any]]) -> str:
        """
        Formata mensagem de resumo da busca.
        
        Args:
            resultados: Resultados completos da busca
            melhores_produtos: Lista dos melhores produtos selecionados
            
        Returns:
            String formatada com resumo
        """
        termo = resultados.get('search_term', 'produto')
        total_magalu = len(resultados.get('magalu', []))
        total_kabuum = len(resultados.get('kabuum', []))
        total_geral = len(resultados.get('all_products', []))
        
        if total_geral == 0:
            return (
                f"🔍 **Busca por: {termo}**\n\n"
                "❌ Nenhum produto encontrado nas lojas consultadas.\n\n"
                "💡 **Dicas:**\n"
                "• Tente termos mais simples (ex: 'notebook' em vez de 'notebook gamer asus')\n"
                "• Use palavras-chave específicas\n"
                "• Verifique a ortografia\n\n"
                "Digite outro termo para buscar! 😊"
            )
        
        summary = (
            f"🔍 **Busca por: {termo}**\n\n"
            f"📊 **Resultados encontrados:**\n"
            f"🔵 Magalu: {total_magalu} produtos\n"
            f"🟠 Kabuum: {total_kabuum} produtos\n"
            f"📦 Total: {total_geral} produtos\n\n"
            f"🏆 **Top {len(melhores_produtos)} melhores ofertas:**\n\n"
        )
        
        return summary
    
    def create_comparison_message(self, produtos: List[Dict[str, Any]]) -> str:
        """
        Cria mensagem comparativa entre produtos.
        
        Args:
            produtos: Lista de produtos para comparar
            
        Returns:
            String com comparação formatada
        """
        if len(produtos) < 2:
            return ""
        
        mais_barato = min(produtos, key=lambda x: x.get('price', float('inf')))
        mais_caro = max(produtos, key=lambda x: x.get('price', 0))
        
        economia = mais_caro.get('price', 0) - mais_barato.get('price', 0)
        
        message = (
            "💡 **Comparação Rápida:**\n"
            f"💰 Mais barato: **R$ {mais_barato.get('price', 0):.2f}** ({mais_barato.get('store', 'Loja')})\n"
            f"💸 Mais caro: **R$ {mais_caro.get('price', 0):.2f}** ({mais_caro.get('store', 'Loja')})\n"
            f"💵 Economia: **R$ {economia:.2f}**\n\n"
        )
        
        return message