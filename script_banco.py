import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `cadastro`;")

cursor.execute("CREATE DATABASE `cadastro`;")

cursor.execute("USE `cadastro`;")

# criando tabelas
TABLES = {}
TABLES['Produtos'] = ('''
      CREATE TABLE `produtos` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `descricao` varchar(70) NOT NULL,
      `disponibilidade` varchar(40) NOT NULL,
       `valor` FLOAT(10,2) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Douglas Benites", "DB", "admin"),
      ("Jose Felipe", "Felipo", "admin"),
      ("Newton", "Fma", "admin")
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from cadastro.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
produtos_sql = 'INSERT INTO produtos (nome, descricao, disponibilidade, valor) VALUES (%s, %s, %s, %s)'
produtos = [
      ('Copo', 'copo epox', 'disponivel',10),
      ('God of War', 'jogo de video game', 'indisponivel',50 ),
      ('Oculos', 'tipo aviador', 'disponivel',120 ),
      ('Faca de cozinha', 'tramontina a30', 'disponivel',68 ),
      ('Caneta bic', 'caneta de tinta esferiografica', 'disponivel',3 ),
      ('Need for Speed', ' jogo de Corrida', 'disponivel',220 ),
]
cursor.executemany(produtos_sql, produtos)

cursor.execute('select * from cadastro.produtos')
print(' -------------  Produtos:  -------------')
for produto in cursor.fetchall():
    print(produto[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()