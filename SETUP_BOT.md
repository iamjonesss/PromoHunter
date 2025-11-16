# 🚀 Setup do PromoHunter Telegram Bot

Este guia irá te ajudar a configurar e executar o bot do Telegram do PromoHunter.

## 📋 Pré-requisitos

- Python 3.11 ou superior
- Conta no Telegram
- Token de bot do Telegram

## 🔧 Configuração Passo a Passo

### 1. Instalar Dependências

```powershell
# Navegar para o diretório do projeto
cd "d:\BECKUP\PROJETOS\Python\PromoHunter"

# Criar ambiente virtual (opcional, mas recomendado)
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt
```

### 2. Criar Bot no Telegram

1. **Abra o Telegram** e procure por `@BotFather`
2. **Digite `/newbot`** para criar um novo bot
3. **Escolha um nome** para seu bot (ex: "PromoHunter Bot")
4. **Escolha um username** (deve terminar com "bot", ex: "promohunter_bot")
5. **Copie o token** fornecido pelo BotFather

### 3. Configurar Token

#### Opção A: Variável de Ambiente (Recomendado)

**Windows PowerShell:**
```powershell
$env:TELEGRAM_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
```

**CMD:**
```cmd
set TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

#### Opção B: Arquivo .env (Avançado)

Crie um arquivo `.env` na raiz do projeto:
```env
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
DEBUG_MODE=true
LOG_LEVEL=INFO
```

### 4. Executar o Bot

#### Execução Simples
```powershell
cd system
python main.py
```

#### Execução com Exemplo
```powershell
python example_bot_usage.py
```

## 🧪 Testando o Bot

1. **Encontre seu bot** no Telegram pelo username escolhido
2. **Digite `/start`** para iniciar
3. **Envie uma mensagem** como "Procuro um smartphone bom e barato"
4. **Verifique os logs** no terminal para confirmar o funcionamento

## 📁 Estrutura dos Arquivos

```
PromoHunter/
├── system/
│   ├── main.py                 # Arquivo principal
│   ├── config/
│   │   ├── settings.py         # Configurações centralizadas
│   │   └── logger.py           # Sistema de logging
│   ├── interfaces/
│   │   └── chatbot.py          # Interface abstrata
│   └── services/
│       └── telegram.py         # Implementação do bot
├── docs/
│   └── telegram_bot.md         # Documentação detalhada
├── example_bot_usage.py        # Exemplo de uso
└── requirements.txt            # Dependências
```

## 🔍 Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `/start` | Iniciar o bot e ver mensagem de boas-vindas |
| `/help` | Mostrar comandos disponíveis |
| Mensagem livre | Processar solicitação de produto |

## 🐛 Resolução de Problemas

### Erro: "Token not found"
- Verifique se a variável `TELEGRAM_TOKEN` está definida
- Confirme que o token está correto (sem espaços extras)

### Erro: "Unauthorized"
- Verifique se o token do bot está correto
- Confirme que o bot foi criado corretamente no BotFather

### Bot não responde
- Verifique se o bot está executando (sem erros no terminal)
- Confirme que você está enviando mensagens para o bot correto
- Verifique os logs para identificar possíveis erros

### Erro de módulos não encontrados
```powershell
# Instalar dependências novamente
pip install --upgrade python-telegram-bot
```

## 📊 Monitoramento

### Logs do Sistema
Os logs aparecem no terminal mostrando:
- Inicialização do bot
- Mensagens recebidas
- Mensagens enviadas
- Erros (se houver)

### Exemplo de Log:
```
2025-01-13 10:30:15 - telegram - INFO - TelegramBot initialized with provided token.
2025-01-13 10:30:16 - telegram - INFO - Starting Telegram bot polling...
2025-01-13 10:30:17 - telegram - INFO - Message received from user 123456789: Olá bot!
```

## 🔄 Próximos Passos

Após configurar o bot básico, você pode:

1. **Integrar com IA** - Conectar com Ollama para recomendações inteligentes
2. **Adicionar comandos** - Implementar comandos personalizados
3. **Conectar APIs** - Integrar com sites de e-commerce
4. **Melhorar UX** - Adicionar botões inline e menus

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs para mensagens de erro
2. Consulte a [documentação detalhada](docs/telegram_bot.md)
3. Verifique se todas as dependências estão instaladas
4. Confirme que o Python 3.11+ está sendo usado

## ⚡ Comandos Rápidos

```powershell
# Setup completo rápido
cd "d:\BECKUP\PROJETOS\Python\PromoHunter"
pip install -r requirements.txt
$env:TELEGRAM_TOKEN="SEU_TOKEN_AQUI"
cd system
python main.py
```

Agora seu PromoHunter Bot deve estar funcionando! 🎉