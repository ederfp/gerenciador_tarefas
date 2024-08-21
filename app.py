from time import sleep
from datetime import datetime
import sqlite3 as sql
from rich.table import Table
from rich.console import Console
from rich import print


class GerenciadorTarefas:

    def __init__(self):
        self.horario_atual = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.tarefa_nao_concluida = 'Não'

    def criacao_tabela_db(self):
        '''
        Criação da Tabela SQLite3
        '''
        conexao = sql.connect('ger_tarefas.db')
        cursor = conexao.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tarefas (
            id INTEGER PRIMARY KEY,
            tarefa TEXT NOT NULL,
            tarefa_concluida TEXT NOT NULL,                
            dataCriacao TEXT NOT NULL);
                            """)
        conexao.commit()

        return conexao, cursor

    def inserir_tarefa(self, tarefa, tarefa_concluida, dataCriacao):
        '''
        Inserir dados em uma tabela
        '''
        conexao, cursor = GerenciadorTarefas.criacao_tabela_db(self)

        cursor.execute("INSERT INTO Tarefas (tarefa, tarefa_concluida, dataCriacao) VALUES (?, ?, ?)",
                    (tarefa, tarefa_concluida, dataCriacao))
        
        conexao.commit()

    def selecionar_todas_tarefas(self):
        '''
        Listar todos os dados de uma tabela
        '''
        conexao, cursor = GerenciadorTarefas.criacao_tabela_db(self)

        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Tarefas")

        return cursor.fetchall()

    def atualizar_tarefas(self, id):
        '''
        Alterar dados de uma tabela
        '''
        conexao, cursor = GerenciadorTarefas.criacao_tabela_db(self)

        cursor.execute("UPDATE Tarefas SET tarefa_concluida = 'Sim' WHERE id = ?", (id,))
        conexao.commit()

    def deletar_tarefa(self, id):
        '''
        Como excluir dados de uma tabela
        '''
        conexao, cursor = GerenciadorTarefas.criacao_tabela_db(self)

        cursor.execute("DELETE FROM Tarefas WHERE id = ?", (id,))
        conexao.commit()
        
    def menu(self):
        '''
        Menu
        '''
        print('###############################')
        print('# [black][on white]Menu Gerenciador de Tarefas[/][/] #')
        print('###############################')
        print('')
        print('1 - Adicionar Tarefas')
        print('2 - Visualizar Tarefas')
        print('3 - Marcar Tarefas como Concluídas')
        print('4 - Remover Tarefas')
        print('')
        print('[red]0 - Sair[/]')
        print('')

    def opcao_1(self):
        '''
        Adicionar Tarefas
        '''
        print('')
        print('[black][on white]Adicionar Tarefas[/][/]')
        print('-----------------')
        print('')

        tarefa = str(input('Digite a Tarefa: '))

        GerenciadorTarefas.inserir_tarefa(self, tarefa, self.tarefa_nao_concluida, self.horario_atual)

        print('')
        print('[green]Tarefa Adicionada[/]')
        print('')
        nova_tarefa = input('Adicinar outra Tarefa? Digite s/n: ')
        if nova_tarefa == 's':
            GerenciadorTarefas.opcao_1(self)
        else:
            GerenciadorTarefas.criacao_tabela_db(self)
            GerenciadorTarefas.programa(self)

    def opcao_2(self):
        '''
        Vizualizar todas as Tarefas
        '''
        print('')
        print('[black][on white]Tarefas[/][/]')
        print('-------')
        print('')
        cursor = GerenciadorTarefas.selecionar_todas_tarefas(self)

        console = Console()
        table = Table()

        table.add_column('ID')
        table.add_column('Tarefas')
        table.add_column('Tarefa Concluída')
        table.add_column('Data de Criação')

        for row in cursor:
            id, tarefa, tarefa_concluida, dataCriacao = row
            table.add_row(str(id), tarefa, tarefa_concluida, dataCriacao)
        
        return console.print(table)

    def opcao_3(self):
        '''
        Concluir Tarefas
        '''
        print('')
        print('[black][on white]Concluir Tarefa[/][/]')
        print('---------------')
        print('')

        GerenciadorTarefas.opcao_2(self)
        print('')

        id = int(input('Digite o ID da Tarefa que deseja Concluir: '))
        print('')

        GerenciadorTarefas.atualizar_tarefas(self, id)

        print('')
        print('[green]Tarefa Concluída[/]')
        print('')
        nova_tarefa = input('Concluir outra Tarefa? Digite s/n: ')
        if nova_tarefa == 's':
            GerenciadorTarefas.opcao_3(self)
        else:
            GerenciadorTarefas.criacao_tabela_db(self)
            GerenciadorTarefas.programa(self)

    def opcao_4(self):
        '''
        Deletar Tarefas
        '''
        print('')
        print('[black][on white]Deletar Tarefa[/][/]')
        print('--------------')
        print('')

        GerenciadorTarefas.opcao_2(self)
        print('')

        id = int(input('Digite o ID da Tarefa que deseja Deletar: '))
        print('')

        GerenciadorTarefas.deletar_tarefa(self, id)

        print('')
        print('[red]Tarefa Deletada[/]')
        print('')
        deletar_outra_tarefa = input('Deletar outra Tarefa? Digite s/n: ')
        if deletar_outra_tarefa == 's':
            GerenciadorTarefas.opcao_4(self)
        else:
            GerenciadorTarefas.criacao_tabela_db(self)
            GerenciadorTarefas.programa(self)

    def programa(self):
        GerenciadorTarefas.menu(self)

        try:
            opcao = int(input('Escolha uma das Opções: '))
            if opcao == 0:
                print('Programa Finalizado')
            elif opcao == 1:
                GerenciadorTarefas.opcao_1(self)
            elif opcao == 2:
                GerenciadorTarefas.opcao_2(self)
                print('')
                nova_tarefa = input('Voltar ao Menu? Digite s/n: ')
                if nova_tarefa == 's':
                    GerenciadorTarefas.programa(self)
                else:
                    print('Programa Finalizado')
            elif opcao == 3:
                GerenciadorTarefas.opcao_3(self)   
            elif opcao == 4:
                GerenciadorTarefas.opcao_4(self)                         
            else:
                print('Digite somente uma das opções acima.')
                print('')
                sleep(1)
                GerenciadorTarefas.programa(self)
        except ValueError as erro:
            print('Digite somente numeros.')
            print('')
            sleep(1)
            GerenciadorTarefas.programa(self)


self = GerenciadorTarefas()
self.criacao_tabela_db()
self.programa()