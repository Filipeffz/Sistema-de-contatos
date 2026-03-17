import sqlite3
from datetime import datetime

BANCO = "contatos.db"

def conectar():
    return sqlite3.connect(BANCO)


def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            cidade TEXT,
            favorito INTEGER DEFAULT 0,
            criado_em TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


def pausar():
    input("\nPressione Enter para continuar...")


def limpar_linha():
    print("-" * 50)


def adicionar_contato():
    print("\n=== ADICIONAR CONTATO ===")
    nome = input("Nome: ").strip()
    telefone = input("Telefone: ").strip()
    email = input("Email: ").strip()
    cidade = input("Cidade: ").strip()

    if not nome or not telefone or not email:
        print("Nome, telefone e email são obrigatórios.")
        return

    criado_em = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO contatos (nome, telefone, email, cidade, favorito, criado_em)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, telefone, email, cidade, 0, criado_em))

        conexao.commit()
        conexao.close()

        print("Contato adicionado com sucesso!")

    except sqlite3.IntegrityError:
        print("Erro: já existe um contato com esse email.")


def listar_contatos():
    print("\n=== LISTA DE CONTATOS ===")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, telefone, email, cidade, favorito, criado_em
        FROM contatos
        ORDER BY nome ASC
    """)
    contatos = cursor.fetchall()
    conexao.close()

    if len(contatos) == 0:
        print("Nenhum contato cadastrado.")
        return

    for contato in contatos:
        favorito = "Sim" if contato[5] == 1 else "Não"

        limpar_linha()
        print(f"ID: {contato[0]}")
        print(f"Nome: {contato[1]}")
        print(f"Telefone: {contato[2]}")
        print(f"Email: {contato[3]}")
        print(f"Cidade: {contato[4]}")
        print(f"Favorito: {favorito}")
        print(f"Criado em: {contato[6]}")
    limpar_linha()


def buscar_por_nome():
    print("\n=== BUSCAR CONTATO POR NOME ===")
    nome = input("Digite o nome: ").strip()

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, telefone, email, cidade, favorito, criado_em
        FROM contatos
        WHERE nome LIKE ?
        ORDER BY nome ASC
    """, ('%' + nome + '%',))

    contatos = cursor.fetchall()
    conexao.close()

    if len(contatos) == 0:
        print("Nenhum contato encontrado.")
        return

    for contato in contatos:
        favorito = "Sim" if contato[5] == 1 else "Não"

        limpar_linha()
        print(f"ID: {contato[0]}")
        print(f"Nome: {contato[1]}")
        print(f"Telefone: {contato[2]}")
        print(f"Email: {contato[3]}")
        print(f"Cidade: {contato[4]}")
        print(f"Favorito: {favorito}")
        print(f"Criado em: {contato[6]}")
    limpar_linha()


def buscar_por_id():
    print("\n=== BUSCAR POR ID ===")

    try:
        id_contato = int(input("Digite o ID: "))

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, nome, telefone, email, cidade, favorito, criado_em
            FROM contatos
            WHERE id = ?
        """, (id_contato,))

        contato = cursor.fetchone()
        conexao.close()

        if contato is None:
            print("Contato não encontrado.")
            return

        favorito = "Sim" if contato[5] == 1 else "Não"

        limpar_linha()
        print(f"ID: {contato[0]}")
        print(f"Nome: {contato[1]}")
        print(f"Telefone: {contato[2]}")
        print(f"Email: {contato[3]}")
        print(f"Cidade: {contato[4]}")
        print(f"Favorito: {favorito}")
        print(f"Criado em: {contato[6]}")
        limpar_linha()

    except ValueError:
        print("Digite um ID válido.")


def atualizar_contato():
    print("\n=== ATUALIZAR CONTATO ===")

    try:
        id_contato = int(input("Digite o ID do contato: "))

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM contatos WHERE id = ?", (id_contato,))
        contato = cursor.fetchone()

        if contato is None:
            print("Contato não encontrado.")
            conexao.close()
            return

        print("\nDeixe em branco para manter o valor atual.")
        novo_nome = input(f"Novo nome ({contato[1]}): ").strip()
        novo_telefone = input(f"Novo telefone ({contato[2]}): ").strip()
        novo_email = input(f"Novo email ({contato[3]}): ").strip()
        nova_cidade = input(f"Nova cidade ({contato[4]}): ").strip()

        nome_final = novo_nome if novo_nome else contato[1]
        telefone_final = novo_telefone if novo_telefone else contato[2]
        email_final = novo_email if novo_email else contato[3]
        cidade_final = nova_cidade if nova_cidade else contato[4]

        cursor.execute("""
            UPDATE contatos
            SET nome = ?, telefone = ?, email = ?, cidade = ?
            WHERE id = ?
        """, (nome_final, telefone_final, email_final, cidade_final, id_contato))

        conexao.commit()
        conexao.close()

        print("Contato atualizado com sucesso!")

    except ValueError:
        print("Digite um ID válido.")
    except sqlite3.IntegrityError:
        print("Erro: esse email já está em uso por outro contato.")


def remover_contato():
    print("\n=== REMOVER CONTATO ===")

    try:
        id_contato = int(input("Digite o ID do contato: "))

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT nome FROM contatos WHERE id = ?", (id_contato,))
        contato = cursor.fetchone()

        if contato is None:
            print("Contato não encontrado.")
            conexao.close()
            return

        confirmar = input(f"Tem certeza que deseja remover '{contato[0]}'? (s/n): ").strip().lower()

        if confirmar == "s":
            cursor.execute("DELETE FROM contatos WHERE id = ?", (id_contato,))
            conexao.commit()
            print("Contato removido com sucesso!")
        else:
            print("Remoção cancelada.")

        conexao.close()

    except ValueError:
        print("Digite um ID válido.")


def favoritar_contato():
    print("\n=== FAVORITAR / DESFAVORITAR CONTATO ===")

    try:
        id_contato = int(input("Digite o ID do contato: "))

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT favorito, nome FROM contatos WHERE id = ?", (id_contato,))
        contato = cursor.fetchone()

        if contato is None:
            print("Contato não encontrado.")
            conexao.close()
            return

        novo_valor = 0 if contato[0] == 1 else 1

        cursor.execute("""
            UPDATE contatos
            SET favorito = ?
            WHERE id = ?
        """, (novo_valor, id_contato))

        conexao.commit()
        conexao.close()

        if novo_valor == 1:
            print(f"{contato[1]} foi marcado como favorito.")
        else:
            print(f"{contato[1]} foi removido dos favoritos.")

    except ValueError:
        print("Digite um ID válido.")


def listar_favoritos():
    print("\n=== CONTATOS FAVORITOS ===")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, telefone, email, cidade, criado_em
        FROM contatos
        WHERE favorito = 1
        ORDER BY nome ASC
    """)

    contatos = cursor.fetchall()
    conexao.close()

    if len(contatos) == 0:
        print("Nenhum contato favorito.")
        return

    for contato in contatos:
        limpar_linha()
        print(f"ID: {contato[0]}")
        print(f"Nome: {contato[1]}")
        print(f"Telefone: {contato[2]}")
        print(f"Email: {contato[3]}")
        print(f"Cidade: {contato[4]}")
        print(f"Criado em: {contato[5]}")
    limpar_linha()


def contar_contatos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM contatos")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM contatos WHERE favorito = 1")
    favoritos = cursor.fetchone()[0]

    conexao.close()

    print("\n=== RESUMO ===")
    print(f"Total de contatos: {total}")
    print(f"Total de favoritos: {favoritos}")


def menu():
    while True:
        print("\n" + "=" * 50)
        print("         SISTEMA DE CONTATOS - SQLITE")
        print("=" * 50)
        print("1 - Adicionar contato")
        print("2 - Listar contatos")
        print("3 - Buscar contato por nome")
        print("4 - Buscar contato por ID")
        print("5 - Atualizar contato")
        print("6 - Remover contato")
        print("7 - Favoritar / Desfavoritar contato")
        print("8 - Listar favoritos")
        print("9 - Mostrar resumo")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            adicionar_contato()
            pausar()
        elif opcao == "2":
            listar_contatos()
            pausar()
        elif opcao == "3":
            buscar_por_nome()
            pausar()
        elif opcao == "4":
            buscar_por_id()
            pausar()
        elif opcao == "5":
            atualizar_contato()
            pausar()
        elif opcao == "6":
            remover_contato()
            pausar()
        elif opcao == "7":
            favoritar_contato()
            pausar()
        elif opcao == "8":
            listar_favoritos()
            pausar()
        elif opcao == "9":
            contar_contatos()
            pausar()
        elif opcao == "0":
            print("Encerrando programa...")
            break
        else:
            print("Opção inválida.")
            pausar()


criar_tabela()

menu()
