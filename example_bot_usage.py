"""
Exemplo de uso da classe TelegramBot do PromoHunter.

Este arquivo demonstra como utilizar a classe TelegramBot para:
1. Inicializar o bot
2. Enviar mensagens
3. Iniciar o polling para receber mensagens
4. Gerenciar o ciclo de vida do bot

Para usar este exemplo:
1. Crie um bot no Telegram através do @BotFather
2. Obtenha o token do bot
3. Defina a variável de ambiente TELEGRAM_TOKEN ou substitua diretamente no código
4. Execute este arquivo: python example_bot_usage.py
"""

import os
import asyncio
from system.services.telegram import TelegramBot

async def main():
    """Exemplo principal de uso do TelegramBot."""
    
    # Obter o token do bot (substitua pelo seu token ou use variável de ambiente)
    # Para obter um token, converse com @BotFather no Telegram
    token = os.getenv('TELEGRAM_TOKEN', 'SEU_TOKEN_AQUI')
    
    if token == 'SEU_TOKEN_AQUI':
        print("⚠️  Por favor, configure seu token do Telegram!")
        print("1. Converse com @BotFather no Telegram para criar um bot")
        print("2. Obtenha o token do bot")
        print("3. Defina a variável de ambiente TELEGRAM_TOKEN ou edite este arquivo")
        return
    
    # Inicializar o bot
    bot = TelegramBot(token)
    
    try:
        # Obter informações do bot
        bot_info = await bot.get_bot_info()
        print(f"🤖 Bot inicializado: {bot_info.get('first_name')} (@{bot_info.get('username')})")
        
        # Exemplo de envio de mensagem (substitua pelo chat_id desejado)
        # Para obter o chat_id, você pode enviar uma mensagem para o bot e verificar os logs
        # chat_id = 123456789  # Substitua pelo ID do chat
        # await bot.send_message(chat_id, "Olá! Este é uma mensagem de teste do PromoHunter!")
        
        print("🚀 Iniciando o bot... (Pressione Ctrl+C para parar)")
        print("💬 Envie mensagens para o bot no Telegram para testá-lo!")
        
        # Iniciar o bot em modo polling
        await bot.start_polling()
        
        # Manter o bot rodando
        while bot.is_bot_running:
            await asyncio.sleep(1)
            
            # Verificar mensagens recebidas
            messages = bot.receive_message()
            if messages:
                for message in messages:
                    print(f"📨 Nova mensagem de {message['first_name']}: {message['message']}")
    
    except KeyboardInterrupt:
        print("\n🛑 Parando o bot...")
        await bot.stop_polling()
        print("✅ Bot parado com sucesso!")
    
    except Exception as e:
        print(f"❌ Erro ao executar o bot: {e}")
        await bot.stop_polling()

def run_bot_sync():
    """Método alternativo para executar o bot de forma síncrona."""
    token = os.getenv('TELEGRAM_TOKEN', 'SEU_TOKEN_AQUI')
    
    if token == 'SEU_TOKEN_AQUI':
        print("⚠️  Por favor, configure seu token do Telegram!")
        return
    
    bot = TelegramBot(token)
    print("🚀 Iniciando o bot em modo síncrono...")
    print("💬 Envie mensagens para o bot no Telegram para testá-lo!")
    
    # Este método bloqueia até o bot ser parado
    bot.run()

if __name__ == "__main__":
    print("🤖 PromoHunter Telegram Bot - Exemplo de Uso")
    print("=" * 50)
    
    # Escolher entre execução assíncrona ou síncrona
    mode = input("Escolha o modo de execução:\n1. Assíncrono (recomendado)\n2. Síncrono\nDigite 1 ou 2: ")
    
    if mode == "2":
        run_bot_sync()
    else:
        asyncio.run(main())