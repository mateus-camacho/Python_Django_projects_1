from models import Conta, engine, Bancos
from sqlmodel import Session,select
#uma função que vai ser pra criar a conta que vai receber como parametro uma conta tendo que ter os pontos da conta
def criar_conta(conta: Conta):
    #cria uma conexão com o banco e é feito dessa forma que quando sai do contexto 
    with Session(engine) as session:
        #faz uma query para ver se tem algum banco igual ao que está sendo passado
        statement = select(Conta).where(Conta.banco == conta.banco)
        results = session.exec(statement).all
        if(results):
            print("Banco já existe")
        #adiciona a conta no banco de dados, porém ele não comita direto já que é sql logo estruturada
        #session.add(conta)
        #então tem que só fazer um comite 
        #session.commit()

conta = Conta(valor=1000, banco=Bancos.NUBANK)
criar_conta(conta)