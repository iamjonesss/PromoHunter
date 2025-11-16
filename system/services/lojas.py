import requests
from interfaces.lojas import InteracaoLojasInterface
import traceback

class Magalu(InteracaoLojasInterface):
    """ Classe concreta para cadastro de lojas online via API.

    :param InteracaoLojasInterface: Assinatura voltada para cadastro de lojas online via API.
    """
    
    def buscar_produtos(self, termo_busca: str):
        """Busca produtos na loja Magalu usando o termo informado."""
        try:
            api = (
                f"https://www.magazinevoce.com.br/_next/data/6cijUACDhFQyBEGYnV_Mr/"
                f"magazinemagalushopbr/busca/{termo_busca}.json?"
                f"path0=magazinemagalushopbr&path2={termo_busca}"
            )

            response = requests.get(api, timeout=10)

            response.raise_for_status()

            data = response.json()

            produtos_raw = data.get("pageProps", {}).get("data", {}).get("search", {}).get("products", [])
            
            produtos_processados = []
            
            for produto_raw in produtos_raw:
                produto = {
                    'id': produto_raw.get('id', ''),
                    'name': produto_raw.get('title', 'Nome não disponível'),
                    'url': produto_raw.get('url', ''),
                    'imageUrl': produto_raw.get('image', ''),
                    'brand': produto_raw.get('brand', {}).get('name', 'Marca não informada') if isinstance(produto_raw.get('brand'), dict) else 'Marca não informada',
                    'description': produto_raw.get('description', ''),
                    'availability': produto_raw.get('available', False)
                }
                
                price_info = produto_raw.get('price', {})
                if isinstance(price_info, dict):
                    produto['price'] = price_info.get('bestPrice', price_info.get('price', 'Preço não informado'))
                    produto['full_price'] = price_info.get('fullPrice', price_info.get('price', ''))
                    produto['discount'] = price_info.get('discount', '0')
                    produto['payment_method'] = price_info.get('paymentMethodDescription', '')
                else:
                    produto['price'] = 'Preço não informado'
                    produto['full_price'] = ''
                    produto['discount'] = '0'
                    produto['payment_method'] = ''
                
                rating_info = produto_raw.get('rating', {})
                if isinstance(rating_info, dict):
                    produto['rating'] = {
                        'average': rating_info.get('average', 0),
                        'count': rating_info.get('count', 0)
                    }
                else:
                    produto['rating'] = {'average': 0, 'count': 0}
                
                produtos_processados.append(produto)
            
            return produtos_processados

        except requests.exceptions.RequestException as e:
            print(f"Erro de requisição ao buscar o produto na Magalu: {e}")
        except Exception:
            print(f"Erro inesperado: {traceback.format_exc()}")


class Kabuum(InteracaoLojasInterface):
    """Classe concreta para buscar produtos na Kabum via API pública."""

    def buscar_produtos(self, termo_busca: str):
        """Busca produtos na loja Kabum usando o termo informado."""
        try:
            url = f"https://servicespub.prod.api.aws.grupokabum.com.br/catalog/v2/sponsored_products?query={termo_busca}&context=search"
            
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                'Origin': 'https://www.kabum.com.br',
                'Referer': 'https://www.kabum.com.br/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'Client-Id': 'kabum',
                'Session': 'c191668c71a88c3b61ab232316e549a4'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            
            print("Status da resposta:", response.status_code)
            print("Chaves na resposta:", list(data.keys()) if isinstance(data, dict) else "Não é dict")
            
            produtos_raw = data.get("data", [])
            print(f"Número de produtos encontrados: {len(produtos_raw)}")
            
            if len(produtos_raw) == 0:
                print("Array de produtos está vazio")
                print("Conteúdo completo da resposta:")
                import json
                print(json.dumps(data, indent=2)[:500] + "..." if len(str(data)) > 500 else json.dumps(data, indent=2))

            produtos_processados = []

            for produto_raw in produtos_raw:
                attributes = produto_raw.get('attributes', {})
                
                produto = {
                    'id': produto_raw.get('id', ''),
                    'name': attributes.get('title', 'Nome não disponível'),
                    'url': f"https://www.kabum.com.br/produto/{produto_raw.get('id')}/{attributes.get('product_link', '')}",
                    'imageUrl': attributes.get('images', [''])[0] if attributes.get('images') else '',
                    'brand': attributes.get('manufacturer', {}).get('name', 'Marca não informada'),
                    'description': attributes.get('description', ''),
                    'availability': attributes.get('available', False)
                }

                price = attributes.get('price', 0)
                price_with_discount = attributes.get('price_with_discount', 0)
                old_price = attributes.get('old_price', 0)
                
                produto['price'] = price_with_discount if price_with_discount > 0 else price
                produto['full_price'] = old_price if old_price > 0 else price
                
                # Calcular desconto
                if old_price > 0 and price_with_discount > 0:
                    desconto = ((old_price - price_with_discount) / old_price) * 100
                    produto['discount'] = round(desconto, 2)
                elif price > 0 and price_with_discount > 0 and price > price_with_discount:
                    desconto = ((price - price_with_discount) / price) * 100
                    produto['discount'] = round(desconto, 2)
                else:
                    produto['discount'] = 0

                produto['rating'] = {
                    'average': attributes.get('score_of_ratings', 0),
                    'count': attributes.get('number_of_ratings', 0)
                }
                produto['installment'] = attributes.get('max_installment', '')
                
                offer = attributes.get('offer')
                if offer:
                    produto['offer'] = {
                        'name': offer.get('name', ''),
                        'price': offer.get('price_with_discount', offer.get('price', 0)),
                        'discount_percentage': offer.get('discount_percentage', 0)
                    }

                produtos_processados.append(produto)

            return produtos_processados

        except requests.exceptions.RequestException as e:
            print(f"Erro de requisição ao buscar produto na Kabum: {e}")
        except Exception:
            print(f"Erro inesperado: {traceback.format_exc()}")
