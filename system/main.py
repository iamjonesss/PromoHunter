import traceback
import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'system'))

from services.telegram import TelegramBot
from config.environments import Environments

async def main():
    """Exemplo principal do PromoHunter com busca integrada."""
    
    print("🤖 PromoHunter - Bot Telegram com Busca Integrada")
    print("=" * 55)
    
    try:
        env = Environments()
        token = env.TELEGRAM_TOKEN.get_secret_value()
        
        if not token:
            print("❌ Token do Telegram não configurado!")
            print("\nConfigure o token no arquivo .env:")
            print('TELEGRAM_TOKEN="seu_token_aqui"')
            return
        
        bot = TelegramBot(token)
        
        bot_info = await bot.get_bot_info()
        print(f"🤖 Bot: {bot_info.get('first_name', 'PromoHunter')} (@{bot_info.get('username', 'seu_bot')})")
        
        print("\n🚀 Iniciando bot com funcionalidades:")
        print("  ✅ Busca automática de produtos")
        print("  ✅ Comparação entre Magalu e Kabuum") 
        print("  ✅ Seleção dos melhores produtos")
        print("  ✅ Formatação inteligente das respostas")
        
        print(f"\n💬 Comandos disponíveis:")
        print("  • /start - Inicializar bot")
        print("  • /help - Ver ajuda completa")
        print("  • /buscar <produto> - Buscar produto específico")
        print("  • Ou digite diretamente: 'procuro smartphone'")
        
        print(f"\n🔥 Exemplos de uso:")
        print("  /buscar smartphone")
        print("  /buscar notebook gamer")
        print("  /buscar placa de video")
        print("  procuro um mouse gamer barato")
        
        print(f"\n⚡ Como funciona:")
        print("  1. Você envia o produto desejado")
        print("  2. Bot busca em múltiplas lojas")
        print("  3. Compara preços e avaliações")
        print("  4. Retorna os 5 melhores produtos")
        print("  5. Mostra comparação de preços")
        
        print("\n" + "=" * 55)
        print("🚀 Bot iniciado! Envie mensagens no Telegram.")
        print("🛑 Pressione Ctrl+C para parar")
        print("=" * 55)
        
        await bot.start_polling()
        
        while bot.is_bot_running:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Parando PromoHunter...")
        if 'bot' in locals():
            await bot.stop_polling()
        print("✅ PromoHunter parado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao executar PromoHunter: {e}")
        traceback.print_exc()

def quick_test():
    """Teste rápido das funcionalidades."""
    print("🧪 Teste Rápido das Funcionalidades")
    print("-" * 40)
    
    try:
        print("📦 Testando importações...")
        from services.product_search import ProductSearchService
        from services.lojas import Magalu, Kabuum
        
        print("  ✅ ProductSearchService")
        print("  ✅ Magalu")
        print("  ✅ Kabuum")
        
        print("\n🔧 Testando inicializações...")
        search_service = ProductSearchService()
        magalu = Magalu()
        kabuum = Kabuum()
        
        print("  ✅ ProductSearchService inicializado")
        print("  ✅ Magalu inicializado")
        print("  ✅ Kabuum inicializado")
        
        print("\n✅ Todos os componentes funcionando!")
        print("\nPara usar o bot completo, execute:")
        print("python exemplo_completo.py")
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("\nVerifique se todos os arquivos estão no lugar correto.")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='PromoHunter - Bot Telegram Completo')
    parser.add_argument('--test', '-t', action='store_true', 
                       help='Executar apenas teste rápido')
    
    args = parser.parse_args()
    
    if args.test:
        quick_test()
    else:
        asyncio.run(main())
