# 🤖 TelegramBot - Documentação

A classe `TelegramBot` é a implementação concreta da interface `ChatbotInterface` para integração com o Telegram. Esta classe fornece funcionalidades completas para envio e recebimento de mensagens através da API do Telegram.

## 📋 Características Principais

- ✅ **Envio de mensagens** - Texto simples e formatado (Markdown/HTML)
- ✅ **Envio de imagens** - Com legendas opcionais
- ✅ **Recebimento de mensagens** - Processamento automático de mensagens dos usuários
- ✅ **Comandos personalizados** - `/start`, `/help` e comandos customizáveis
- ✅ **Logging integrado** - Sistema de logs completo para monitoramento
- ✅ **Gerenciamento de estado** - Controle do ciclo de vida do bot
- ✅ **Modo assíncrono e síncrono** - Flexibilidade na execução

## 🚀 Como Usar

### 1. Inicialização Básica

```python
from system.services.telegram import TelegramBot

# Inicializar o bot com o token
bot = TelegramBot("SEU_TOKEN_DO_TELEGRAM")
```

### 2. Envio de Mensagens

```python
import asyncio

async def enviar_mensagem():
    # Enviar mensagem simples
    sucesso = await bot.send_message(
        chat_id=123456789,
        text="Olá! Esta é uma mensagem do PromoHunter!"
    )
    
    # Enviar mensagem formatada
    await bot.send_message(
        chat_id=123456789,
        text="**Produto Encontrado!**\n\n*Smartphone XYZ* - R$ 599,00",
        parse_mode="Markdown"
    )

# Executar
asyncio.run(enviar_mensagem())
```

### 3. Envio de Imagens

```python
async def enviar_imagem():
    await bot.send_photo(
        chat_id=123456789,
        photo_url="https://exemplo.com/produto.jpg",
        caption="🔥 Promoção imperdível!"
    )

asyncio.run(enviar_imagem())
```

### 4. Recebimento de Mensagens

```python
# Verificar mensagens recebidas
mensagens = bot.receive_message()
for msg in mensagens:
    print(f"Usuário {msg['first_name']}: {msg['message']}")

# Obter apenas a última mensagem
ultima_mensagem = bot.get_latest_message()
if ultima_mensagem:
    print(f"Última mensagem: {ultima_mensagem['message']}")
```

### 5. Executar o Bot

#### Modo Síncrono (Simples)
```python
# Execução bloqueante - mais simples para scripts básicos
bot.run()
```

#### Modo Assíncrono (Avançado)
```python
async def executar_bot():
    try:
        await bot.start_polling()
        
        # Bot rodando, fazer outras operações...
        while bot.is_bot_running:
            await asyncio.sleep(1)
            
            # Processar mensagens ou outras tarefas
            
    except KeyboardInterrupt:
        await bot.stop_polling()

asyncio.run(executar_bot())
```

## 🔧 Métodos Disponíveis

### Métodos Principais

| Método | Descrição | Tipo |
|--------|-----------|------|
| `send_message()` | Envia mensagem de texto | Assíncrono |
| `send_photo()` | Envia imagem com legenda | Assíncrono |
| `receive_message()` | Obtém mensagens recebidas | Síncrono |
| `get_latest_message()` | Obtém última mensagem | Síncrono |
| `start_polling()` | Inicia recebimento de mensagens | Assíncrono |
| `stop_polling()` | Para o bot | Assíncrono |
| `run()` | Executa bot em modo síncrono | Síncrono |

### Métodos Auxiliares

| Método | Descrição | Retorno |
|--------|-----------|---------|
| `get_bot_info()` | Informações do bot | `Dict[str, Any]` |
| `is_bot_running` | Status do bot | `bool` |

## 📝 Comandos Padrão

O bot vem com comandos pré-configurados:

### `/start`
Comando de boas-vindas que apresenta o bot ao usuário.

**Resposta:**
```
🤖 Olá! Bem-vindo ao PromoHunter!

Eu sou seu assistente inteligente para encontrar os melhores produtos
com base em avaliações e custo-benefício.

Digite /help para ver os comandos disponíveis ou envie uma mensagem
descrevendo o produto que você está procurando!
```

### `/help`
Exibe informações de ajuda e comandos disponíveis.

**Resposta:**
```
🔍 **Comandos Disponíveis:**

/start - Iniciar o bot
/help - Mostrar esta mensagem de ajuda

**Como usar:**
Simplesmente envie uma mensagem descrevendo o produto que você está
procurando e eu te ajudarei a encontrar as melhores opções!
```

## ⚙️ Configuração

### 1. Obter Token do Telegram

1. Abra o Telegram
2. Procure por `@BotFather`
3. Digite `/newbot`
4. Siga as instruções para criar seu bot
5. Copie o token fornecido

### 2. Configurar Variável de Ambiente

**Windows PowerShell:**
```powershell
$env:TELEGRAM_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
```

**Linux/Mac:**
```bash
export TELEGRAM_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
```

### 3. Obter Chat ID

Para enviar mensagens, você precisa do Chat ID:

1. Envie uma mensagem para seu bot
2. Acesse: `https://api.telegram.org/bot<SEU_TOKEN>/getUpdates`
3. Encontre o `chat.id` na resposta

## 🛡️ Tratamento de Erros

A classe possui tratamento robusto de erros:

```python
# Exemplo de verificação de erro
sucesso = await bot.send_message(chat_id, "Mensagem")
if not sucesso:
    print("Erro ao enviar mensagem - verificar logs")
```

## 📊 Logs

O sistema de logging fornece informações detalhadas:

```
2025-01-13 10:30:15 - telegram - INFO - TelegramBot initialized with provided token.
2025-01-13 10:30:16 - telegram - INFO - Starting Telegram bot polling...
2025-01-13 10:30:17 - telegram - INFO - Message received from user 123456789: Olá bot!
2025-01-13 10:30:18 - telegram - INFO - Message sent successfully to chat 123456789
```

## 🔄 Integração com PromoHunter

A classe está preparada para integração com o sistema de recomendação:

```python
class PromoHunterBot(TelegramBot):
    def __init__(self, token: str, recommendation_service):
        super().__init__(token)
        self.recommendation_service = recommendation_service
    
    async def process_product_request(self, message: str, chat_id: int):
        # Processar pedido com IA
        recommendations = await self.recommendation_service.get_recommendations(message)
        
        # Enviar recomendações
        for product in recommendations:
            await self.send_message(chat_id, product.format_message())
            if product.image_url:
                await self.send_photo(chat_id, product.image_url, product.caption)
```

## 🚨 Limitações e Considerações

- **Rate Limiting**: O Telegram possui limites de mensagens por segundo
- **Tamanho de Mensagem**: Máximo de 4096 caracteres por mensagem
- **Formatos Suportados**: Texto, fotos, documentos (implementação atual: texto e fotos)
- **Grupos vs Privado**: Funciona em chats privados e grupos

## 🔗 Links Úteis

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot Documentação](https://python-telegram-bot.readthedocs.io/)
- [BotFather](https://t.me/BotFather) - Para criar e gerenciar bots