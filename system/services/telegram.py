import asyncio
from typing import Optional, Dict, Any, List
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from interfaces.chatbot import ChatbotInterface
from config.logger import BotLogger
from services.product_search import ProductSearchService

class TelegramBot(ChatbotInterface):
    """Implementação concreta da interface ChatbotInterface para o Telegram.
    
    Esta classe gerencia a integração com o Telegram usando a biblioteca python-telegram-bot,
    permitindo envio e recebimento de mensagens através da API do Telegram.
    """
    
    def __init__(self, token: str):
        """Construtor da classe que receberá o token de acesso para as requisições para o telegram.
        
        Args:
            token (str): Token de acesso do bot fornecido pelo BotFather do Telegram
        """
        super().__init__(token)
        self.logger = BotLogger(__name__).get_logger()
        self.bot = Bot(token=self.token)
        self.application = Application.builder().token(self.token).build()
        self.is_running = False
        self.received_messages: List[Dict[str, Any]] = []
        self.product_search = ProductSearchService()
        
        # Configurar handlers
        self._setup_handlers()
        
        self.logger.info("TelegramBot initialized with provided token.")
    
    def _setup_handlers(self):
        """Configura os handlers para comandos e mensagens."""
        # Handler para o comando /start
        start_handler = CommandHandler('start', self._start_command)
        self.application.add_handler(start_handler)
        
        # Handler para o comando /help
        help_handler = CommandHandler('help', self._help_command)
        self.application.add_handler(help_handler)
        
        # Handler para o comando /buscar
        search_handler = CommandHandler('buscar', self._search_command)
        self.application.add_handler(search_handler)
        
        # Handler para mensagens de texto
        message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message)
        self.application.add_handler(message_handler)
    
    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para o comando /start."""
        welcome_message = (
            "🤖 Olá! Bem-vindo ao PromoHunter!\n\n"
            "Eu sou seu assistente inteligente para encontrar os melhores produtos "
            "com base em avaliações e custo-benefício.\n\n"
            "Digite /help para ver os comandos disponíveis ou envie uma mensagem "
            "descrevendo o produto que você está procurando!"
        )
        await update.message.reply_text(welcome_message)
        self.logger.info(f"Start command executed for user {update.effective_user.id}")
    
    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para o comando /help."""
        help_message = (
            "🔍 **Comandos Disponíveis:**\n\n"
            "/start - Iniciar o bot\n"
            "/help - Mostrar esta mensagem de ajuda\n"
            "/buscar <produto> - Buscar produto nas lojas\n\n"
            "**Exemplos de uso:**\n"
            "/buscar smartphone\n"
            "/buscar notebook gamer\n"
            "/buscar placa de video\n\n"
            "**Ou simplesmente digite:**\n"
            "Procuro um smartphone bom e barato\n\n"
            "🤖 Eu vou buscar nas melhores lojas e te mostrar as melhores ofertas!"
        )
        await update.message.reply_text(help_message, parse_mode='Markdown')
        self.logger.info(f"Help command executed for user {update.effective_user.id}")
    
    async def _search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para o comando /buscar."""
        if not context.args:
            await update.message.reply_text(
                "❌ Por favor, informe o produto que deseja buscar!\n\n"
                "**Exemplo:** /buscar smartphone\n"
                "**Ou:** /buscar notebook gamer"
            )
            return
        
        # Juntar argumentos para formar o termo de busca
        termo_busca = " ".join(context.args)
        await self._process_search(update, termo_busca)
    
    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para mensagens de texto regulares."""
        message_data = {
            'user_id': update.effective_user.id,
            'username': update.effective_user.username,
            'first_name': update.effective_user.first_name,
            'message': update.message.text,
            'timestamp': update.message.date
        }
        
        self.received_messages.append(message_data)
        
        # Processar mensagem como busca de produto
        await self._process_search(update, update.message.text)
        
        self.logger.info(f"Message received from user {update.effective_user.id}: {update.message.text}")
    
    async def _process_search(self, update: Update, termo_busca: str):
        """Processa a busca de produtos e envia os resultados."""
        chat_id = update.effective_chat.id
        
        # Enviar mensagem de "digitando..."
        await self.bot.send_chat_action(chat_id=chat_id, action="typing")
        
        # Mensagem de início da busca
        await update.message.reply_text(
            f"🔍 Buscando '{termo_busca}' nas melhores lojas...\n"
            "⏳ Aguarde um momento, estou comparando preços!"
        )
        
        try:
            # Realizar busca
            resultados = await self.product_search.search_products(termo_busca)
            
            # Encontrar melhores produtos
            melhores_produtos = self.product_search.find_best_products(
                resultados['all_products'], 
                criterio='melhor_custo_beneficio'
            )
            
            if not melhores_produtos:
                await update.message.reply_text(
                    self.product_search.format_summary_message(resultados, [])
                )
                return
            
            # Enviar resumo
            summary = self.product_search.format_summary_message(resultados, melhores_produtos)
            await update.message.reply_text(summary, parse_mode='Markdown')
            
            # Enviar comparação (se houver mais de um produto)
            if len(melhores_produtos) > 1:
                comparison = self.product_search.create_comparison_message(melhores_produtos)
                if comparison:
                    await update.message.reply_text(comparison, parse_mode='Markdown')
            
            # Enviar cada produto
            for i, produto in enumerate(melhores_produtos, 1):
                product_message = self.product_search.format_product_message(produto, i)
                await update.message.reply_text(product_message, parse_mode='Markdown')
                
                # Pequena pausa entre mensagens para não sobrecarregar
                if i < len(melhores_produtos):
                    await asyncio.sleep(0.5)
            
            # Mensagem final
            final_message = (
                "✨ **Busca concluída!**\n\n"
                "💡 **Dicas:**\n"
                "• Use /buscar para nova busca\n"
                "• Digite o nome de outro produto\n"
                "• Considere avaliações e garantia além do preço\n\n"
                "📞 Quer ajuda? Digite /help"
            )
            await update.message.reply_text(final_message, parse_mode='Markdown')
            
        except Exception as e:
            self.logger.error(f"Erro durante busca: {e}")
            await update.message.reply_text(
                "❌ Ops! Ocorreu um erro durante a busca.\n"
                "🔄 Tente novamente em alguns instantes ou com outro termo.\n\n"
                "Se o problema persistir, digite /help para mais informações."
            )
    
    async def send_message(self, chat_id: int, text: str, parse_mode: Optional[str] = None) -> bool:
        """Envia uma mensagem para o chat especificado.
        
        Args:
            chat_id (int): ID do chat de destino
            text (str): Texto da mensagem a ser enviada
            parse_mode (str, optional): Modo de formatação ('Markdown' ou 'HTML')
            
        Returns:
            bool: True se a mensagem foi enviada com sucesso, False caso contrário
        """
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode
            )
            self.logger.info(f"Message sent successfully to chat {chat_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error sending message to chat {chat_id}: {e}")
            return False
    
    async def send_photo(self, chat_id: int, photo_url: str, caption: str = "") -> bool:
        """Envia uma foto para o chat especificado.
        
        Args:
            chat_id (int): ID do chat de destino
            photo_url (str): URL ou caminho da foto
            caption (str): Legenda da foto
            
        Returns:
            bool: True se a foto foi enviada com sucesso, False caso contrário
        """
        try:
            await self.bot.send_photo(
                chat_id=chat_id,
                photo=photo_url,
                caption=caption
            )
            self.logger.info(f"Photo sent successfully to chat {chat_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error sending photo to chat {chat_id}: {e}")
            return False
    
    def receive_message(self) -> List[Dict[str, Any]]:
        """Retorna as mensagens recebidas desde a última consulta.
        
        Returns:
            List[Dict[str, Any]]: Lista de mensagens recebidas
        """
        messages = self.received_messages.copy()
        self.received_messages.clear()  # Limpa a lista após retornar
        return messages
    
    def get_latest_message(self) -> Optional[Dict[str, Any]]:
        """Retorna a última mensagem recebida.
        
        Returns:
            Optional[Dict[str, Any]]: Última mensagem recebida ou None se não houver mensagens
        """
        return self.received_messages[-1] if self.received_messages else None
    
    async def start_polling(self):
        """Inicia o bot em modo polling para receber mensagens."""
        try:
            self.logger.info("Starting Telegram bot polling...")
            self.is_running = True
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
            self.logger.info("Telegram bot is now running and listening for messages")
        except Exception as e:
            self.logger.error(f"Error starting bot polling: {e}")
            self.is_running = False
            raise
    
    async def stop_polling(self):
        """Para o bot e encerra o polling."""
        try:
            self.logger.info("Stopping Telegram bot...")
            if self.is_running:
                await self.application.updater.stop()
                await self.application.stop()
                await self.application.shutdown()
                self.is_running = False
                self.logger.info("Telegram bot stopped successfully")
        except Exception as e:
            self.logger.error(f"Error stopping bot: {e}")
            raise
    
    def run(self):
        """Método de conveniência para executar o bot (modo síncrono)."""
        try:
            self.application.run_polling()
        except KeyboardInterrupt:
            self.logger.info("Bot stopped by user")
        except Exception as e:
            self.logger.error(f"Error running bot: {e}")
            raise
    
    @property
    def is_bot_running(self) -> bool:
        """Verifica se o bot está em execução.
        
        Returns:
            bool: True se o bot está rodando, False caso contrário
        """
        return self.is_running
    
    async def get_bot_info(self) -> Dict[str, Any]:
        """Obtém informações sobre o bot.
        
        Returns:
            Dict[str, Any]: Informações do bot incluindo nome, username, etc.
        """
        try:
            bot_info = await self.bot.get_me()
            return {
                'id': bot_info.id,
                'first_name': bot_info.first_name,
                'username': bot_info.username,
                'can_join_groups': bot_info.can_join_groups,
                'can_read_all_group_messages': bot_info.can_read_all_group_messages,
                'supports_inline_queries': bot_info.supports_inline_queries
            }
        except Exception as e:
            self.logger.error(f"Error getting bot info: {e}")
            return {}