from models import Conta, engine, Bancos, Status, Historico, Tipo
from sqlmodel import Session,select
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
        if conta.valor < valor:
            raise ValueError("Saldo insuficiente")
        #agora só faço a mesma coisa para o de entrada
        statement = select(Conta).where(Conta.id == id_conta_entrada)
        conta_entrada = session.exec(statement).first()
        conta_entrada.valor = conta_entrada.valor + valor
        conta_saida.valor = conta_saida.valor - valor
        session.commit()
        
def movimentar_dinheiro(historico: Historico):
    with Session(engine) as session:
        

conta = Conta(valor=200, banco=Bancos.INTER)
criar_conta(conta)
#print(listar_contas())
#desativar_conta(1)
transferir_saldo(2,3,20)