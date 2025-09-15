#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot para gerenciar o parâmetro m_Enable do KillFeed.json
Altera automaticamente o valor baseado no horário:
- Sábados às 17:20: m_Enable = 0 (desabilita KillFeed)
- Sábados às 23h: m_Enable = 1 (habilita KillFeed)
- Outros dias: m_Enable = 1 (sempre habilitado)
"""

import json
import os
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('killfeed_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class KillFeedBot:
    def __init__(self, json_file_path):
        """
        Inicializa o bot com o caminho do arquivo JSON
        
        Args:
            json_file_path (str): Caminho completo para o arquivo KillFeed.json
        """
        self.json_file_path = Path(json_file_path)
        self.last_state = None  # Para evitar mudanças desnecessárias
        
    def read_json_file(self):
        """
        Lê o arquivo JSON e retorna o conteúdo
        
        Returns:
            dict: Conteúdo do arquivo JSON ou None se houver erro
        """
        try:
            if not self.json_file_path.exists():
                logger.error(f"Arquivo não encontrado: {self.json_file_path}")
                return None
                
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                logger.debug(f"Arquivo lido com sucesso: {self.json_file_path}")
                return data
                
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro ao ler arquivo: {e}")
            return None
    
    def write_json_file(self, data):
        """
        Escreve dados no arquivo JSON
        
        Args:
            data (dict): Dados para escrever no arquivo
            
        Returns:
            bool: True se sucesso, False se erro
        """
        try:
            # Criar backup do arquivo original
            backup_path = self.json_file_path.with_suffix('.json.backup')
            if self.json_file_path.exists():
                import shutil
                shutil.copy2(self.json_file_path, backup_path)
                logger.info(f"Backup criado: {backup_path}")
            
            # Escrever novo arquivo
            with open(self.json_file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
                logger.info(f"Arquivo atualizado com sucesso: {self.json_file_path}")
                return True
                
        except Exception as e:
            logger.error(f"Erro ao escrever arquivo: {e}")
            return False
    
    def update_m_enable(self, value):
        """
        Atualiza o parâmetro m_Enable no arquivo JSON
        
        Args:
            value (int): Novo valor para m_Enable (0 ou 1)
            
        Returns:
            bool: True se sucesso, False se erro
        """
        data = self.read_json_file()
        if data is None:
            return False
            
        # Verificar se o valor já está correto
        if data.get('m_Enable') == value:
            logger.debug(f"m_Enable já está com o valor {value}, não é necessário alterar")
            return True
            
        # Atualizar o valor
        data['m_Enable'] = value
        
        # Escrever arquivo atualizado
        if self.write_json_file(data):
            logger.info(f"m_Enable alterado para {value}")
            return True
        else:
            return False
    
    def should_enable_killfeed(self):
        """
        Verifica se o KillFeed deve estar habilitado baseado no horário atual
        
        Returns:
            bool: True se deve estar habilitado (1), False se deve estar desabilitado (0)
        """
        now = datetime.now()
        
        # Verificar se é sábado (weekday() retorna 5 para sábado)
        if now.weekday() != 5:  # Não é sábado
            return True  # Fora dos sábados, sempre habilitado
            
        # Verificar horário específico dos sábados
        current_time = now.time()
        disable_time = datetime.strptime("17:20", "%H:%M").time()
        enable_time = datetime.strptime("23:00", "%H:%M").time()
        
        if current_time >= enable_time:  # 23h em diante
            return True  # Habilitado após 23h
        elif current_time >= disable_time:  # 17:20 às 22:59
            return False  # Desabilitado das 17:20 às 23h
        else:
            return True  # Antes das 17:20, habilitado
    
    def run(self):
        """
        Executa o loop principal do bot
        """
        logger.info("Bot KillFeed iniciado")
        logger.info(f"Monitorando arquivo: {self.json_file_path}")
        
        try:
            while True:
                current_time = datetime.now()
                
                # Verificar se deve estar habilitado
                should_enable = self.should_enable_killfeed()
                
                # Determinar o valor correto
                target_value = 1 if should_enable else 0
                
                # Aplicar mudança se necessário
                if self.last_state != target_value:
                    logger.info(f"Estado mudou: {self.last_state} -> {target_value}")
                    if self.update_m_enable(target_value):
                        self.last_state = target_value
                    else:
                        logger.error("Falha ao atualizar arquivo")
                
                # Log do status atual
                status = "HABILITADO" if should_enable else "DESABILITADO"
                logger.info(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] "
                           f"Status: {status} (m_Enable = {target_value})")
                
                # Aguardar 1 minuto antes da próxima verificação
                time.sleep(60)
                
        except KeyboardInterrupt:
            logger.info("Bot interrompido pelo usuário")
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
        finally:
            logger.info("Bot finalizado")

def main():
    """
    Função principal
    """
    # Caminho do arquivo JSON
    json_file_path = r"C:\Program Files (x86)\CFTools Software GmbH\Architect\Agent\deployments\VDS-BACKUP\profiles\AC\Settings\KillFeed.json"
    
    # Verificar se o arquivo existe
    if not os.path.exists(json_file_path):
        logger.error(f"Arquivo não encontrado: {json_file_path}")
        logger.error("Verifique se o caminho está correto e se o arquivo existe")
        return
    
    # Criar e executar o bot
    bot = KillFeedBot(json_file_path)
    bot.run()

if __name__ == "__main__":
    main()
