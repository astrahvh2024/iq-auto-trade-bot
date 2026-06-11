import customtkinter as ctk
from iqoptionapi.stable_api import IQ_Option
import pandas as pd
import threading
import time
import os
from datetime import datetime

# Estilo Visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class IQTradeBot(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("IQTradeBot V4.0 - Hybrid System")
        self.attributes('-fullscreen', True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.api = None
        self.rodando = False
        
        # Estatísticas
        self.lucro_total = 0.0
        self.vitorias = 0
        self.derrotas = 0
        self.win_rate = 0.0

        # Variáveis Dinâmicas
        self.var_rsi = ctk.StringVar(value="80")
        self.var_exp = ctk.StringVar(value="1")
        self.var_tf = ctk.StringVar(value="1")
        self.var_bb = ctk.StringVar(value="2.0")
        self.var_valor = ctk.StringVar(value="2.0")

        self.after(100, self.setup_ui)

    def setup_ui(self):
        # HEADER
        self.lbl_titulo = ctk.CTkLabel(self, text="SISTEMA HÍBRIDO: AUTO-TRADE & SINALIZADOR", 
                                      font=("Roboto", 35, "bold"), text_color="#FF8C00")
        self.lbl_titulo.pack(pady=10)

        # AVISO DE ESTRATÉGIA
        self.lbl_manual = ctk.CTkLabel(self, text="💡 ESTRATÉGIA: Níveis baixos (RSI 50/BB 1.0) geram MUITOS SINAIS (Arriscado).\nNíveis altos (RSI 90/BB 2.5) são para Sniper (Seguro).", 
                                     font=("Roboto", 13), text_color="#3498db")
        self.lbl_manual.pack(pady=2)

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=30)

        # --- COLUNA ESQUERDA ---
        self.col_left = ctk.CTkFrame(self.main_container, width=400)
        self.col_left.pack(side="left", fill="both", padx=10, pady=10)

        self.ent_email = ctk.CTkEntry(self.col_left, placeholder_text="E-mail", height=45)
        self.ent_senha = ctk.CTkEntry(self.col_left, placeholder_text="Senha", show="*", height=45)
        self.ent_email.pack(pady=5, padx=20, fill="x"); self.ent_senha.pack(pady=5, padx=20, fill="x")
        
        self.tipo_conta = ctk.CTkSegmentedButton(self.col_left, values=["PRACTICE", "REAL"])
        self.tipo_conta.set("PRACTICE"); self.tipo_conta.pack(pady=10, padx=20, fill="x")
        
        self.btn_login = ctk.CTkButton(self.col_left, text="CONECTAR", fg_color="#FF8C00", font=("Roboto", 18, "bold"), command=self.conectar)
        self.btn_login.pack(pady=10, padx=20, fill="x")

        # PAINEL DE PERFORMANCE
        self.frame_calc = ctk.CTkFrame(self.col_left, fg_color="#1a1a1a", border_width=1, border_color="#FF8C00")
        self.frame_calc.pack(pady=10, padx=20, fill="x")
        self.lbl_lucro = ctk.CTkLabel(self.frame_calc, text="LUCRO: R$ 0.00", font=("Roboto", 22, "bold"))
        self.lbl_lucro.pack(pady=5)
        self.lbl_winrate = ctk.CTkLabel(self.frame_calc, text="ASSERTIVIDADE: 0%", font=("Roboto", 18, "bold"), text_color="#44FF44")
        self.lbl_winrate.pack(pady=5)
        self.lbl_stats = ctk.CTkLabel(self.frame_calc, text="W: 0 | L: 0", font=("Roboto", 16)); self.lbl_stats.pack()

        self.lbl_banca = ctk.CTkLabel(self.col_left, text="BANCA: R$ --", font=("Roboto", 32, "bold"), text_color="#44FF44")
        self.lbl_banca.pack(pady=15)

        # --- COLUNA DIREITA ---
        self.col_right = ctk.CTkFrame(self.main_container)
        self.col_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.render_radio_group("NÍVEL RSI", ["50", "60", "70", "80", "90"], self.var_rsi)
        self.render_radio_group("DESVIO BB", ["1.0", "1.5", "2.0", "2.5"], self.var_bb)
        self.render_radio_group("EXPIRAÇÃO", ["1", "2", "5"], self.var_exp)

        self.ent_val_trade = ctk.CTkEntry(self.col_right, width=150, textvariable=self.var_valor, placeholder_text="Valor R$")
        self.ent_val_trade.pack(pady=10)

        self.btn_start = ctk.CTkButton(self.col_right, text="INICIAR MONITORAMENTO", state="disabled", 
                                      fg_color="#228B22", height=80, font=("Roboto", 30, "bold"), command=self.toggle_bot)
        self.btn_start.pack(pady=20, padx=50, fill="x")

        self.txt_log = ctk.CTkTextbox(self, height=250, font=("Courier New", 18, "bold"), fg_color="#000000", text_color="#00FF00")
        self.txt_log.pack(fill="x", padx=30, pady=20)

    def render_radio_group(self, titulo, valores, variavel):
        frame = ctk.CTkFrame(self.col_right, fg_color="transparent")
        frame.pack(pady=10, fill="x", padx=30)
        ctk.CTkLabel(frame, text=titulo, font=("Roboto", 18, "bold"), text_color="#FF8C00").pack(side="left", padx=15)
        for v in valores:
            ctk.CTkRadioButton(frame, text=v, variable=variavel, value=v).pack(side="left", padx=10)

    def alert_sound(self, tipo):
        if tipo == "ordem": os.system('say "Operação"')
        if tipo == "win": os.system('say "Vitória"')
        if tipo == "loss": os.system('say "Derrota"')
        if tipo == "sinal": os.system('say "Atenção Sinal"')

    def log(self, msg):
        self.txt_log.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.txt_log.see("end")

    def conectar(self):
        self.api = IQ_Option(self.ent_email.get(), self.ent_senha.get())
        check, _ = self.api.connect()
        if check:
            self.api.change_balance(self.tipo_conta.get())
            self.btn_start.configure(state="normal")
            self.loop_estatisticas()
            self.log("✅ CONECTADO! Automático: OTC | Alerta: Outros.")

    def loop_estatisticas(self):
        def update():
            while True:
                if self.api:
                    try:
                        b = self.api.get_balance()
                        self.lbl_banca.configure(text=f"BANCA: R$ {b:.2f}")
                        total = self.vitorias + self.derrotas
                        rate = (self.vitorias / total * 100) if total > 0 else 0
                        self.lbl_stats.configure(text=f"W: {self.vitorias} | L: {self.derrotas}")
                        self.lbl_winrate.configure(text=f"ASSERTIVIDADE: {rate:.1f}%")
                        self.lbl_lucro.configure(text=f"LUCRO: R$ {self.lucro_total:.2f}")
                    except: pass
                time.sleep(5)
        threading.Thread(target=update, daemon=True).start()

    def toggle_bot(self):
        self.rodando = not self.rodando
        self.btn_start.configure(text="PARAR" if self.rodando else "INICIAR MONITORAMENTO", fg_color="#B22222" if self.rodando else "#228B22")
        if self.rodando: threading.Thread(target=self.main_loop, daemon=True).start()

    def gerenciar_ordem(self, ativo, direcao, valor, exp):
        status, id_o = self.api.buy(valor, ativo, direcao, exp)
        if status:
            self.alert_sound("ordem")
            self.log(f"🔥 AUTO-TRADE: {ativo} | {direcao.upper()}")
            _, win = self.api.check_win_v3(id_o)
            if win > 0:
                self.vitorias += 1; self.lucro_total += win
                self.alert_sound("win")
            else:
                self.derrotas += 1; self.lucro_total -= valor
                self.alert_sound("loss")

    def main_loop(self):
        ativos = ["EURUSD-OTC", "GBPUSD-OTC", "EURJPY-OTC", "EURUSD", "GBPUSD", "USDJPY", "AUDUSD"]
        while self.rodando:
            try:
                rsi_limit = float(self.var_rsi.get())
                bb_dev = float(self.var_bb.get())
                val = float(self.var_valor.get())
                exp = int(self.var_exp.get())

                for ativo in ativos:
                    if not self.rodando: break
                    velas = self.api.get_candles(ativo, 60, 40, time.time())
                    if not velas: continue
                    
                    df = pd.DataFrame(velas)
                    fechamento = df['close']
                    
                    # Cálculo RSI
                    diff = fechamento.diff()
                    g = diff.where(diff > 0, 0).rolling(2).mean()
                    l = -diff.where(diff < 0, 0).rolling(2).mean()
                    rsi = 100 - (100 / (1 + (g / l))).iloc[-1]
                    
                    # Cálculo Bollinger
                    ma = fechamento.rolling(20).mean().iloc[-1]
                    std = fechamento.rolling(20).std().iloc[-1]
                    b_sup, b_inf = ma + (bb_dev * std), ma - (bb_dev * std)
                    preco = fechamento.iloc[-1]

                    direcao = "put" if rsi >= rsi_limit and preco >= b_sup else "call" if rsi <= (100-rsi_limit) and preco <= b_inf else None
                    
                    if direcao:
                        if "OTC" in ativo:
                            # EXECUÇÃO AUTOMÁTICA EM OTC
                            threading.Thread(target=self.gerenciar_ordem, args=(ativo, direcao, val, exp), daemon=True).start()
                        else:
                            # APENAS ALERTA EM PARES NORMAIS
                            self.alert_sound("sinal")
                            self.log(f"🔔 ALERTA: {ativo} | {direcao.upper()} (Opere manual)")
                    
                    time.sleep(0.3)
                time.sleep(1)
            except: time.sleep(2)

if __name__ == "__main__":
    IQTradeBot().mainloop()
