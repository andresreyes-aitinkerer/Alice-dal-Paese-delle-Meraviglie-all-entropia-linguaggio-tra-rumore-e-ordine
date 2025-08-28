import math, random, re
import requests
from collections import Counter
import matplotlib.pyplot as plt


# 1) Scarica Alice in Wonderland (Plain Text UTF-8)
URL = "https://www.gutenberg.org/files/11/11-0.txt"
txt = requests.get(URL, timeout=30).text  # richiede internet nel tuo ambiente

# 2) Pulisci: minuscole, solo lettere a–z e spazi
txt_clean = txt.lower()
txt_clean = re.sub(r"[^a-z\s]+", " ", txt_clean)
txt_clean = re.sub(r"\s+", " ", txt_clean).strip()


alfabeto = "abcdefghijklmnopqrstuvwxyz"

# 3) Funzioni per frequenze ed entropia (Shannon)
def frequenze_lettere(testo):
    """
    Restituisce la frequenza relativa di ogni lettera.
    """
    conteggi = Counter(c for c in testo if c in alfabeto)
    totale = sum(conteggi.values())
    return {l: conteggi.get(l, 0) / totale for l in alfabeto}

def entropia_testo(testo):
    """
    Calcola l'entropia H(X) di un testo.
    """
    freq = frequenze_lettere(testo)
    return -sum(p * math.log2(p) for p in freq.values() if p > 0)

# Calcolo dell'entropia di Alice
random.seed(42)  # per replicabilità
H_alice = entropia_testo(txt_clean)
print("Entropia di Alice in Wonderland:", H_alice)

#4) Canale rumoroso: con probabilità ε sostituisce la lettera con un’altra a caso
def canale_rumoroso(testo, errore=0.2):
    out = []
    for ch in testo:
        if ch in alfabeto and random.random() < errore:
            out.append(random.choice(alfabeto))
        else:
            out.append(ch)
    return "".join(out)

eps_values = [0.0, 0.1, 0.2, 0.3, 0.4]
for eps in eps_values:
    rumoroso = canale_rumoroso(txt_clean, errore=eps)
    H_noisy = entropia_testo(rumoroso)
    print(f"epsilon={eps:.1f} | H Alice={H_alice:.4f} | H rumoroso={H_noisy:.4f}")



H_values = []
for eps in eps_values:
    rumoroso = canale_rumoroso(txt_clean, errore=eps)
    H_noisy = entropia_testo(rumoroso)
    H_values.append(H_noisy)

# Imposta sfondo nero
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(6,4))

print(H_values)
print(H_alice)


ax.plot(eps_values, H_values, marker='o', color='cyan', label="Entropia rumorosa")
ax.axhline(y=H_alice, color='yellow', linestyle='--', label="Entropia Alice")
ax.axhline(y=math.log2(len(alfabeto)), color='red', linestyle=':', label="Massimo teorico")

ax.set_xlabel(r"Probabilità di errore $\varepsilon$", color='white')
ax.set_ylabel("Entropia (bit/simbolo)", color='white')
ax.set_title("Entropia vs rumore in 'Alice in Wonderland'", color='white')

ax.legend()
ax.grid(True, color='gray', alpha=0.3)
plt.tight_layout()
plt.show()

def decodifica_probabilistica(messaggio_rumoroso, frequenze_note):
    """
    Mappa le lettere del messaggio rumoroso a quelle più probabili
    secondo le frequenze attese (approccio semplificato).
    """
    freq_rumoroso = frequenze_lettere(messaggio_rumoroso)
    ordine_rumoroso = sorted(freq_rumoroso, key=freq_rumoroso.get, reverse=True)
    ordine_attese = sorted(frequenze_note, key=frequenze_note.get, reverse=True)
    mappa = dict(zip(ordine_rumoroso, ordine_attese))
    return "".join(mappa.get(ch, ch) for ch in messaggio_rumoroso)

# Frequenze attese dal testo originale di Alice
freq_attese_alice = frequenze_lettere(txt_clean)


estratto_alice = txt_clean[:300]

random.seed(42)
msg_rum = canale_rumoroso(estratto_alice, errore=0.3)
msg_decod = decodifica_probabilistica(msg_rum, freq_attese_alice)

print("Messaggio originale:", estratto_alice[:30] + "...")
print("Messaggio rumoroso:", msg_rum[:30] + "...")
print("Messaggio decodificato (grezzo):", msg_decod[:30] + "...")

plt.style.use('dark_background')




# 1) Entropia vs rumore
eps_values = [0.0, 0.1, 0.2, 0.3, 0.4]
H_noisy_values = []

for eps in eps_values:
    y = canale_rumoroso(txt_clean, errore=eps)
    H_noisy_values.append(entropia_testo(y))

fig, ax = plt.subplots(figsize=(6,4))
ax.plot(eps_values, H_noisy_values, marker='o', color='cyan', label="Entropia del testo rumoroso H(Y)")
ax.axhline(y=H_alice, linestyle='--', color='yellow', label="Entropia originale H(X)")
ax.axhline(y=math.log2(len(alfabeto)), linestyle=':', color='red', label="Massimo teorico log2(26)")
ax.set_xlabel(r"Probabilità di errore $\varepsilon$", color='white')
ax.set_ylabel("Entropia (bit/simbolo)", color='white')
ax.set_title("Entropia vs rumore (Alice in Wonderland)", color='white')
ax.legend()
ax.grid(True, color='gray', alpha=0.3)
plt.tight_layout()
plt.show()

# 2) Stima qualitativa della capacità residua: H(X) - H(Y)
cap_estim = [H_alice - h for h in H_noisy_values]

fig, ax = plt.subplots(figsize=(6,4))
ax.plot(eps_values, cap_estim, marker='o', color='lime', label=r"Stima qualitativa $H(X)-H(Y)$")
ax.set_xlabel(r"Probabilità di errore $\varepsilon$", color='white')
ax.set_ylabel("Bit/simbolo (stima qualitativa)", color='white')
ax.set_title("Capacità residua (stima qualitativa) vs rumore", color='white')
ax.legend()
ax.grid(True, color='gray', alpha=0.3)
plt.tight_layout()
plt.show()




