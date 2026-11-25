# =====================================================================
# SISTEMA DIDÁTICO DE CONTROLE DE PRODUTOS E VENDAS
# Conceitos aplicados: Listas, Dicionários, Funções, Loops e Ordenação
# =====================================================================

# Banco de dados em memória (usando listas de dicionários)
produtos = [
    {"id": 1, "nome": "Caderno Universitario", "preco": 25.50, "estoque": 30},
    {"id": 2, "nome": "Caneta Azul", "preco": 3.00, "estoque": 100},
    {"id": 3, "nome": "Mochila Escolar", "preco": 120.00, "estoque": 15},
]

vendas = []  # Armazenará o histórico de vendas realizadas
proximo_id_venda = 1


# ---------------------------------------------------------------------
# FUNÇÕES AUXILIARES
# ---------------------------------------------------------------------
def buscar_produto_por_id(id_procurado):
    """Retorna o dicionário do produto se encontrar o ID, ou None se não existir."""
    for p in produtos:
        if p["id"] == id_procurado:
            return p
    return None


def listar_produtos(lista_para_exibir=None):
    """Exibe os produtos formatados em tabela."""
    if lista_para_exibir is None:
        lista_para_exibir = produtos

    print("\n--- LISTA DE PRODUTOS ---")
    if not lista_para_exibir:
        print("Nenhum produto cadastrado.")
        return

    print(f"{'ID':<4} | {'Nome':<25} | {'Preço (R$)':<12} | {'Estoque':<8}")
    print("-" * 58)
    for p in lista_para_exibir:
        print(
            f"{p['id']:<4} | {p['nome']:<25} | {p['preco']:<12.2f} | {p['estoque']:<8}"
        )


# ---------------------------------------------------------------------
# 1. CADASTRAR PRODUTO
# ---------------------------------------------------------------------
def cadastrar_produto():
    print("\n--- CADASTRAR NOVO PRODUTO ---")
    nome = input("Nome do produto: ").strip()
    try:
        preco = float(input("Preço unitário (ex: 19.90): "))
        estoque = int(input("Quantidade inicial em estoque: "))
    except ValueError:
        print("Erro: Digite valores numéricos válidos para preço e estoque.")
        return

    # Gera um novo ID automático baseado no maior ID atual
    novo_id = max([p["id"] for p in produtos], default=0) + 1

    novo_produto = {
        "id": novo_id,
        "nome": nome,
        "preco": preco,
        "estoque": estoque,
    }
    produtos.append(novo_produto)
    print(f"Sucesso! Produto '{nome}' cadastrado com ID {novo_id}.")


# ---------------------------------------------------------------------
# 2. ALTERAR PRODUTO
# ---------------------------------------------------------------------
def alterar_produto():
    listar_produtos()
    try:
        id_prod = int(input("\nDigite o ID do produto que deseja alterar: "))
    except ValueError:
        print("Erro: ID inválido.")
        return

    produto = buscar_produto_por_id(id_prod)
    if not produto:
        print("Produto não encontrado!")
        return

    print(
        f"Editando: {produto['nome']} (Deixe em branco para manter o valor atual)"
    )

    novo_nome = input(f"Novo nome [{produto['nome']}]: ").strip()
    novo_preco = input(f"Novo preço [{produto['preco']:.2f}]: ").strip()
    novo_estoque = input(f"Novo estoque [{produto['estoque']}]: ").strip()

    if novo_nome:
        produto["nome"] = novo_nome
    if novo_preco:
        try:
            produto["preco"] = float(novo_preco)
        except ValueError:
            print("Preço inválido. Mantendo o anterior.")
    if novo_estoque:
        try:
            produto["estoque"] = int(novo_estoque)
        except ValueError:
            print("Estoque inválido. Mantendo o anterior.")

    print("Produto atualizado com sucesso!")


# ---------------------------------------------------------------------
# 3. REGISTRAR VENDA
# ---------------------------------------------------------------------
def registrar_venda():
    global proximo_id_venda
    listar_produtos()

    try:
        id_prod = int(input("\nDigite o ID do produto vendido: "))
        qtd = int(input("Quantidade vendida: "))
    except ValueError:
        print("Erro: Digite apenas números inteiros.")
        return

    produto = buscar_produto_por_id(id_prod)
    if not produto:
        print("Produto não encontrado!")
        return

    if qtd <= 0:
        print("A quantidade deve ser maior que zero.")
        return

    if produto["estoque"] < qtd:
        print(f"Estoque insuficiente! Disponível: {produto['estoque']} unidades.")
        return

    # Atualiza o estoque e registra a venda
    produto["estoque"] -= qtd
    valor_total = produto["preco"] * qtd

    nova_venda = {
        "id_venda": proximo_id_venda,
        "id_produto": produto["id"],
        "nome_produto": produto["nome"],
        "quantidade": qtd,
        "total": valor_total,
    }
    vendas.append(nova_venda)
    proximo_id_venda += 1

    print(f"Venda #{nova_venda['id_venda']} registrada! Total: R$ {valor_total:.2f}")


# ---------------------------------------------------------------------
# 4. CANCELAR VENDA (E DEVOLVER AO ESTOQUE)
# ---------------------------------------------------------------------
def cancelar_venda():
    print("\n--- HISTÓRICO DE VENDAS ---")
    if not vendas:
        print("Nenhuma venda registrada para cancelar.")
        return

    for v in vendas:
        print(
            f"Venda #{v['id_venda']} | Produto: {v['nome_produto']} | Qtd: {v['quantidade']} | Total: R$ {v['total']:.2f}"
        )

    try:
        id_cancelar = int(input("\nDigite o ID da venda que deseja cancelar: "))
    except ValueError:
        print("Erro: ID inválido.")
        return

    for i, v in enumerate(vendas):
        if v["id_venda"] == id_cancelar:
            # Devolve os itens ao estoque do produto original
            produto = buscar_produto_por_id(v["id_produto"])
            if produto:
                produto["estoque"] += v["quantidade"]

            vendas.pop(i)  # Remove a venda da lista
            print(
                f"Venda #{id_cancelar} cancelada e {v['quantidade']} unidade(s) devolvida(s) ao estoque!"
            )
            return

    print("ID de venda não encontrado.")


# ---------------------------------------------------------------------
# 5. CLASSIFICAR PRODUTOS (ORDENAÇÃO)
# ---------------------------------------------------------------------
def classificar_produtos():
    print("\n--- CLASSIFICAR PRODUTOS ---")
    print("1. Por Nome (A-Z)")
    print("2. Por Preço (Menor -> Maior)")
    print("3. Por Preço (Maior -> Menor)")
    print("4. Por Estoque (Menor -> Maior)")

    opcao = input("Escolha o critério: ")

    # O método sorted() cria uma cópia ordenada sem bagunçar a lista original
    if opcao == "1":
        ordenados = sorted(produtos, key=lambda p: p["nome"].lower())
    elif opcao == "2":
        ordenados = sorted(produtos, key=lambda p: p["preco"])
    elif opcao == "3":
        ordenados = sorted(produtos, key=lambda p: p["preco"], reverse=True)
    elif opcao == "4":
        ordenados = sorted(produtos, key=lambda p: p["estoque"])
    else:
        print("Opção inválida.")
        return

    listar_produtos(ordenados)


# ---------------------------------------------------------------------
# 6. RANKING DE MAIS VENDIDOS
# ---------------------------------------------------------------------
def exibir_ranking():
    print("\n--- RANKING DE PRODUTOS MAIS VENDIDOS ---")
    if not vendas:
        print("Ainda não há vendas registradas para gerar o ranking.")
        return

    # Dicionário para somar a quantidade vendida por produto
    contagem = {}
    for v in vendas:
        nome = v["nome_produto"]
        contagem[nome] = contagem.get(nome, 0) + v["quantidade"]

    # Transforma o dicionário em lista de tuplas e ordena da maior quantidade para a menor
    ranking_ordenado = sorted(contagem.items(), key=lambda item: item[1], reverse=True)

    print(f"{'Posição':<8} | {'Produto':<25} | {'Unidades Vendidas':<18}")
    print("-" * 56)
    for posicao, (nome, qtd_total) in enumerate(ranking_ordenado, start=1):
        print(f"{posicao}º {'':<5} | {nome:<25} | {qtd_total:<18}")


# ---------------------------------------------------------------------
# MENU PRINCIPAL
# ---------------------------------------------------------------------
def menu():
    while True:
        print("\n========================================")
        print("      SISTEMA DE GESTÃO DE VENDAS       ")
        print("========================================")
        print("1. Listar Produtos")
        print("2. Cadastrar Produto")
        print("3. Alterar Produto")
        print("4. Registrar Venda")
        print("5. Cancelar Venda")
        print("6. Classificar Produtos")
        print("7. Ranking de Mais Vendidos")
        print("0. Sair")
        print("========================================")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_produtos()
        elif opcao == "2":
            cadastrar_produto()
        elif opcao == "3":
            alterar_produto()
        elif opcao == "4":
            registrar_venda()
        elif opcao == "5":
            cancelar_venda()
        elif opcao == "6":
            classificar_produtos()
        elif opcao == "7":
            exibir_ranking()
        elif opcao == "0":
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida! Tente novamente.")


# Inicia o programa
if __name__ == "__main__":
    menu()
