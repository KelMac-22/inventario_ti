from db import conectar

conexao = conectar()
cursor = conexao.cursor()

cursor.execute("SELECT * FROM funcionarios")

for linha in cursor.fetchall():
    print(linha)

cursor.close()
conexao.close()