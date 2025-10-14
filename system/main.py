"""
Arquivo principal do PromoHunter - Um assistente inteligente para encontrar produtos.

Este é o ponto de entrada principal da aplicação PromoHunter, que integra
o bot do Telegram com o sistema de recomendação de produtos.
"""

from services.telegram import TelegramBot
from config.logger import BotLogger
from config.environments import Environments

def main():
    """Função principal da aplicação PromoHunter."""
    
    # Configurar logger
    logger = BotLogger(__name__).get_logger()
    logger.info("🚀 Iniciando PromoHunter...")
    
    env = Environments()
    token = env.TELEGRAM_TOKEN.get_secret_value()

    if not token:
        logger.error("❌ Token do Telegram não encontrado!")
        print("\n⚠️  CONFIGURAÇÃO NECESSÁRIA:")
        print("1. Converse com @BotFather no Telegram para criar um bot")
        print("2. Obtenha o token do bot")
        print("3. Configure a variável de ambiente TELEGRAM_TOKEN")
        print("\nExemplo no Windows PowerShell:")
        print('$env:TELEGRAM_TOKEN="SEU_TOKEN_AQUI"')
        print("\nExemplo no Linux/Mac:")
        print('export TELEGRAM_TOKEN="SEU_TOKEN_AQUI"')
        return
    
    try:
        # Inicializar o bot do Telegram
        bot = TelegramBot(token)
        
        logger.info("🤖 Bot do Telegram inicializado com sucesso")
        logger.info("💬 O bot está pronto para receber mensagens!")
        
        # Executar o bot
        print("🚀 PromoHunter está rodando...")
        print("💬 Envie mensagens para o bot no Telegram!")
        print("🛑 Pressione Ctrl+C para parar")
        
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("🛑 PromoHunter parado pelo usuário")
        print("\n✅ PromoHunter parado com sucesso!")
        
    except Exception as e:
        logger.error(f"❌ Erro ao executar PromoHunter: {e}")
        print(f"\n❌ Erro: {e}")
        raise

if __name__ == "__main__":
    main()