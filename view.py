#só para saber pep8 é o "estilo certo" do python

from models import Conta, engine, Bancos, Status, Historico, Tipo
from sqlmodel import Session,select
from datetime import date, timedelta
#biblioteca de criar grafico(na teoria eu sabia ela)
import matplotlib.pyplot as plt

#uma função que vai ser pra criar a conta que vai receber como parametro uma conta tendo que ter os pontos da conta
def criar_conta(conta: Conta):
    #cria uma conexão com o banco e é feito dessa forma que quando sai do contexto 
    with Session(engine) as session:
        #faz uma query para ver se tem algum banco igual ao que está sendo passado (achei meio estranho)
        statement = select(Conta).where(Conta.banco == conta.banco)
        #results vai retornar uma lista de contas que tem o banco igual ao que está sendo passado
        results = session.exec(statement).all()
        #se tiver algum resultado em python é true então se tiver algum banco igual ele vai printar que o banco já existe
        if(results):
            print("Banco já existe")
            #no do cara aqui é só um return e não um else, mas eu vou fazer assim
            #seria só o return
            #e apagaria o else
        else:
            #adiciona a conta no banco de dados, porém ele não comita direto já que é sql logo estruturada
            session.add(conta)
            #então tem que só fazer um comite 
            session.commit()

def listar_contas():
    with Session(engine) as session:
        #faz apenas um query com select para pegar todas as contas
        statement = select(Conta)
        #results vai retornar uma lista de contas
        results = session.exec(statement).all()
        return results

def desativar_conta(id):
    with Session(engine) as session:
        #faz uma query para achar o que tem o id que vai ser desativado
        statement = select(Conta).where(Conta.id == id)
        #agora eu pego o primeiro resultado(já que sempre vai ter 1 por conta id unico), porque se tacar normal é uma lista, aí assim consegue manipular melhor
        conta = session.exec(statement).first()
        print(conta.valor)
        if conta.valor > 0:
            raise ValueError("Conta com saldo positivo não pode ser desativada")
        conta.status = Status.INATIVO
        session.commit()

def transferir_saldo(id_conta_saida,id_conta_entrada,valor):
    with Session(engine) as session:
        #faz uma query para achar o que tem o id que vai sair o dinheiro
        statement = select(Conta).where(Conta.id == id_conta_saida)
        #agora eu pego o primeiro resultado(já que sempre vai ter 1 por conta id unico), porque se tacar normal é uma lista, aí assim consegue manipular melhor
        conta_saida = session.exec(statement).first()
        #vai ter que ver se tem o dinheiro suficiente para fazer a transação
        print(conta_saida.valor)
        if conta_saida.valor < valor:
            raise ValueError("Saldo insuficiente")
        #agora só faço a mesma coisa para o de entrada
        statement = select(Conta).where(Conta.id == id_conta_entrada)
        conta_entrada = session.exec(statement).first()
        conta_entrada.valor = conta_entrada.valor + valor
        conta_saida.valor = conta_saida.valor - valor
        session.commit()

#vai ser tipo quando você quer comprar uma coisa ou receber de algo sem ser entre as contas 
def movimentar_dinheiro(historico: Historico):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id ==historico.conta_id)
        conta = session.exec(statement).first()
        #primeiro verifica se a conta ta ativa
        if conta.status == Status.INATIVO:
            raise ValueError("Conta inativa")
        #se for do tipo entrada então vai só receber o dinheiro
        if historico.tipo == Tipo.ENTRADA:
            conta.valor = conta.valor + historico.valor
        #se for do tipo saida vai tirar o dinheiro
        else:
            #vai tirar só se tiver o dinheiro necessário
            if conta.valor < historico.valor:
                raise ValueError("valor da conta insuficiente")
            else:
                conta.valor = conta.valor - historico.valor
        session.add(historico)
        session.commit()

#função para ver o dinheiro de todas as contas somadas
def total_contas():
    with Session(engine) as session:
        statement = select(Conta)
        contas = session.exec(statement).all()
        print(contas)
        valor_total = 0
        for conta in contas:
            valor_total = valor_total + conta.valor
        return valor_total

#vai retornar todos os históricos entre duas datas
def buscar_historicos_entre_datas(data_inicio : date, data_final: date):
    with Session(engine) as session:
        statement = select(Historico).where(
            Historico.data >= data_inicio, 
            Historico.data <= data_final
        )
        historicos = session.exec(statement).all()
        return historicos
#vai criar um grafico que vai ter os banco e em quanto dinheiro tem em cada um
def cria_grafico_por_conta():
    with Session(engine) as session:
        #vou só colocar no grafico as contas ativas
        statement = select(Conta).where(Conta.status == Status.ATIVO)
        contas = session.exec(statement).all()
        #primeiro cria uma lista de bancos
        bancos = []
        valores = []
        #e uma lista dos valores de cada banco
        for conta in contas:
            bancos.append(conta.banco.value)
            valores.append(conta.valor)
        #tem um jeito de fazer isso direto que eu não sei, falou list compression ou coisa assim
        #banco = [conta.banco.value for conta in contas]
        #valores = [conta.valor for conta in contas]

        #aí agora faz o grafico
        plt.bar(bancos, valores)
        plt.show()

#conta = Conta(valor=30, banco=Bancos.NUBANK)
#criar_conta(conta)
print(listar_contas())
#desativar_conta(1)
#transferir_saldo(1,2,20)
#historico = Historico(conta_id=2, tipo=Tipo.SAIDA,valor=5,data= date.today())
#movimentar_dinheiro(historico)
#total_contas()

#o timedelta é basicamente para colocar dias, então o que vc coloca como parametro é os dias, nesse meu caso to vendo entre ontem (hoje - 1 dia) e amanha(hoje + 1 dia) 
#x = buscar_historicos_entre_datas(date.today() - timedelta(1), date.today() + timedelta(1))
#print(x)


#cria_grafico_por_conta()