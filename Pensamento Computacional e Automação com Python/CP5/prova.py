'''usuarios = {
    'ana' : 5,
    'bruno' : 0,
    'carla' : 3
}

for usuario, acessos in usuarios.items():
    if acessos == 0:
        del usuarios[usuario]

print(usuarios)'''

'''status= {
    '/login' : 200,
    '/usuarios' : 404,
}

print('/login' in status,
      200 in status,
      ('/login', 200) in status.items()
)''' 

'''registro = ('API-01', [200, 200, 500])

registro[1].append(404)

print(registro)'''

'''partidas = (
    ("Ana", 10),
    ("Bruno", 7),
    ("Carlos", 8),
    ("Ana", 5),
    ("Bruno", 10),
    ("Carlos", 4),
    ("Ana", -2)
)

pontos = {}

for jogador, valor in partidas:
    if jogador not in pontos:
        pontos[jogador] = 0

    pontos[jogador] += valor

campeao = ""
maior_pontuacao = None

for jogador in pontos:

    if maior_pontuacao is None or pontos[jogador] > maior_pontuacao:
        maior_pontuacao = pontos[jogador]
        campeao = jogador

print(pontos)
print("Campeão:", campeao, "-", maior_pontuacao, "pontos")'''

def registrar_acesso(dados):
    dados['acessos'] += 1
    return dados

sistema = {
    'acessos': 10
}

resultado = registrar_acesso(sistema)

resultado['acessos'] += 5

print(sistema['acessos'])