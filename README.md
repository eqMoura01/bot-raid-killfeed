# Bot KillFeed - Gerenciador Automático

## ⚠️ AVISO LEGAL IMPORTANTE

**Este software é fornecido apenas para fins educacionais e de desenvolvimento pessoal.**

- ❌ **NÃO USE** este software sem autorização prévia do proprietário do sistema
- ❌ **NÃO DISTRIBUA** ou modifique sem permissão explícita
- ⚖️ **USO NÃO AUTORIZADO** pode resultar em ações legais, incluindo notificações DMCA
- 🔒 **RESPONSABILIDADE** pelo uso indevido é exclusiva do usuário

**Ao usar este software, você concorda com estes termos e assume total responsabilidade por suas ações.**

---

Este bot Python monitora automaticamente o arquivo `KillFeed.json` e altera o parâmetro `m_Enable` baseado no horário e dia da semana.

## Funcionalidades

- **Monitoramento automático**: Verifica o horário a cada minuto
- **Controle por horário**: 
  - Sábados às 17:20: `m_Enable = 0` (desabilita KillFeed)
  - Sábados às 23h: `m_Enable = 1` (habilita KillFeed)
  - Outros dias: `m_Enable = 1` (sempre habilitado)
- **Backup automático**: Cria backup do arquivo antes de modificá-lo
- **Logging completo**: Registra todas as ações em arquivo de log
- **Tratamento de erros**: Lida com problemas de acesso ao arquivo

## Como usar

### 1. Instalação
```bash
# Clone ou baixe os arquivos
# Não são necessárias dependências externas (usa apenas bibliotecas padrão do Python)
```

### 2. Configuração
O bot está configurado para monitorar o arquivo:
```
C:\Program Files (x86)\CFTools Software GmbH\Architect\Agent\deployments\VDS-BACKUP\profiles\AC\Settings\KillFeed.json
```

### 3. Execução
```bash
python killfeed_bot.py
```

### 4. Execução em segundo plano (Windows)
Para executar como serviço em segundo plano:
```bash
# Usando o Task Scheduler do Windows ou
pythonw killfeed_bot.py
```

## Arquivos gerados

- `killfeed_bot.log`: Log de todas as operações
- `KillFeed.json.backup`: Backup automático do arquivo original

## Logs

O bot registra:
- Início e fim da execução
- Mudanças de estado do `m_Enable`
- Erros de leitura/escrita do arquivo
- Status atual a cada minuto

## Exemplo de log

```
2024-01-13 17:19:00 - INFO - Bot KillFeed iniciado
2024-01-13 17:19:00 - INFO - Monitorando arquivo: C:\Program Files (x86)\...
2024-01-13 17:19:00 - INFO - [2024-01-13 17:19:00] Status: HABILITADO (m_Enable = 1)
2024-01-13 17:20:00 - INFO - Estado mudou: None -> 0
2024-01-13 17:20:00 - INFO - Backup criado: KillFeed.json.backup
2024-01-13 17:20:00 - INFO - Arquivo atualizado com sucesso
2024-01-13 17:20:00 - INFO - m_Enable alterado para 0
2024-01-13 17:20:00 - INFO - [2024-01-13 17:20:00] Status: DESABILITADO (m_Enable = 0)
2024-01-13 23:00:00 - INFO - Estado mudou: 0 -> 1
2024-01-13 23:00:00 - INFO - m_Enable alterado para 1
2024-01-13 23:00:00 - INFO - [2024-01-13 23:00:00] Status: HABILITADO (m_Enable = 1)
```

## Parâmetros do arquivo JSON

O bot modifica apenas o parâmetro `m_Enable`:
- `1`: KillFeed habilitado
- `0`: KillFeed desabilitado

Todos os outros parâmetros permanecem inalterados.

## Troubleshooting

### Arquivo não encontrado
- Verifique se o caminho está correto
- Confirme se o arquivo existe no local especificado
- Execute como administrador se necessário

### Erro de permissão
- Execute o bot como administrador
- Verifique as permissões do arquivo JSON

### Bot não está funcionando
- Verifique o arquivo de log `killfeed_bot.log`
- Confirme se o horário do sistema está correto
- Verifique se é realmente sábado
