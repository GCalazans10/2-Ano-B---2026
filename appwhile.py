import random

# O computador escolhe um número secreto entre 1 e 50
numero_secreto = random.randint(1, 50)
tentativas = 0
acertou = False

print("--- 🎮 DESAFIO DA ADIVINHAÇÃO ---")
print("Tente adivinhar o número que pensei entre 1 e 50!")

# O loop continua enquanto o aluno não acertar
while not acertou:
    palpite = int(input("\nQual o seu palpite? "))
    tentativas += 1

    if palpite == numero_secreto:
        print(f"✅ BOA! Você acertou em {tentativas} tentativas.")
        acertou = True
    elif palpite < numero_secreto:
        print("📈 Dica: É MAIOR!")
    else:
        print("📉 Dica: É MENOR!")

print("--------------------------------")
