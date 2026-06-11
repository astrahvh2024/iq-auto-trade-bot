--

# 📊 IQTradeBot V4.0 - Hybrid System

Robô de trading automatizado para **IQ Option**, desenvolvido em Python com interface gráfica (CustomTkinter), combinando estratégias de:

* 📈 RSI (Índice de Força Relativa)
* 📊 Bandas de Bollinger
* ⏱️ Timeframe configurável
* 🤖 Auto-trading em OTC + alertas em ativos normais

---

## ⚙️ Funcionalidades

* Login direto na IQ Option (Real / Practice)
* Execução automática de ordens em ativos OTC
* Sinais visuais e sonoros
* Estratégia híbrida (RSI + Bollinger Bands)
* Estatísticas em tempo real:

  * Lucro total
  * Winrate
  * Vitórias e derrotas
* Monitoramento contínuo de múltiplos ativos
* Interface gráfica completa e intuitiva

---

## 🧠 Estratégia do Robô

O robô combina dois indicadores técnicos:

### 📈 RSI

* Detecta sobrecompra e sobrevenda
* Base para entrada:

  * PUT quando RSI alto + preço acima da banda superior
  * CALL quando RSI baixo + preço abaixo da banda inferior

### 📊 Bandas de Bollinger

MA \pm k\sigma

* MA = média móvel (20 períodos)
* σ = desvio padrão
* k = desvio configurável (1.0 a 2.5)

---

## ⏱️ Timeframe

O sistema permite ajuste de tempo das velas:

* 1 min (scalping rápido)
* 2 min (intermediário)
* 5 min (mais seguro)

> ⚠️ Observação: no código atual o timeframe está fixo em `60 segundos`, mas já existe variável preparada (`var_tf`) para expansão futura.

---

## 🧩 Estrutura do Código (Explicação)

### 1. Interface (CustomTkinter)

* Cria painel gráfico completo
* Login, botões e estatísticas
* Logs em tempo real

---

### 2. Conexão com IQ Option

```python
self.api = IQ_Option(email, senha)
```

* Conecta na corretora
* Alterna entre conta REAL e DEMO

---

### 3. Loop de Estatísticas

* Atualiza saldo
* Calcula winrate
* Mostra lucro em tempo real
* Executa em thread separada

---

### 4. Estratégia de Entrada

No `main_loop`:

* Busca velas do ativo:

```python
self.api.get_candles(ativo, 60, 40, time.time())
```

* Calcula:

  * RSI
  * Bollinger Bands

* Define direção:

```python
PUT → RSI alto + preço acima da banda superior  
CALL → RSI baixo + preço abaixo da banda inferior
```

---

### 5. Execução de Ordens

```python
self.api.buy(valor, ativo, direcao, exp)
```

* Executa operação automática
* Verifica resultado (win/loss)
* Atualiza estatísticas

---

### 6. Alertas

* Voz no sistema:

  * “Operação”
  * “Vitória”
  * “Derrota”
  * “Atenção Sinal”

---

## 📊 Ativos monitorados

* EURUSD (OTC e normal)
* GBPUSD
* EURJPY
* USDJPY
* AUDUSD

---

## 💡 Melhorias possíveis (IMPORTANTE)

Seu código já está funcional, mas pode evoluir bastante:

* 🔥 Usar `var_tf` realmente no get_candles (atualmente não está ativo)
* 📉 Filtro de tendência (EMA 200)
* 🧠 Machine Learning para confirmação de sinal
* ⚡ Evitar múltiplas entradas simultâneas no mesmo ativo
* 📊 Dashboard web (em vez de só GUI desktop)
* 🛑 Stop loss / daily limit automático

---

## 🚨 Aviso

Este robô:

* Não garante lucro
* Opera com base em indicadores técnicos
* Pode gerar perdas em mercados voláteis

Use sempre em conta demo antes.

---

## 📩 Contato / Versão Pro

Para dúvidas, melhorias ou versão profissional do robô:

📲 Telegram: **@astrahvhdev**

---

Se quiser, posso na próxima etapa:

* transformar isso em **README estilo GitHub profissional com badges e imagens**
* ou melhorar seu robô com **filtro de tendência + anti-loss system (bem mais forte)**
