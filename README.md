# Google Snake Game Replica

Um clone do clássico jogo da cobrinha do Google (Google Snake), feito em Python com [Pygame](https://www.pygame.org/).

## 🎮 Sobre o projeto

O jogo reproduz a mecânica e a estética do Snake que aparece na busca do Google: a cobra se move por um tabuleiro em xadrez verde, coletando maçãs para crescer, com placar de pontos atuais e recorde na tela.

## 🖼️ Recursos

- `Recursos/Imagens/` — spritesheets da cobra/fruta, ícones (maçã e troféu) e telas de fundo/início.
- `Recursos/Sons/` — música de fundo do menu, música de fundo do jogo e efeito sonoro ao comer a fruta.

## ▶️ Como jogar

**Pré-requisitos:**
- Python 3
- Pygame

```bash
pip install pygame
```

**Executando:**

```bash
python main.py
```

**Controles:**

| Ação          | Teclas           |
|---------------|------------------|
| Mover cima    | `↑` ou `W`       |
| Mover baixo   | `↓` ou `S`       |
| Mover esquerda| `←` ou `A`       |
| Mover direita | `→` ou `D`       |
| Iniciar jogo  | Qualquer tecla   |
| Sair          | `Esc` (no menu)  |

## 🧠 Como funciona

- O mapa é representado por uma matriz onde cada célula indica se é espaço livre, parede, fruta ou parte da cobra.
- A cobra se move em blocos (tiles), com direção controlada por uma fila de trajetos, permitindo curvas suaves entre uma célula e outra.
- Ao comer a fruta, a cobra cresce, o placar aumenta e uma nova fruta é sorteada em uma posição livre do mapa.
- O jogo acaba (voltando ao menu) quando a cobra colide com uma parede ou com o próprio corpo, ou quando todo o espaço livre do mapa é preenchido.

## 📁 Estrutura

```
.
├── main.py              # Lógica principal do jogo
└── Recursos/
    ├── Imagens/         # Sprites e telas
    └── Sons/            # Músicas e efeitos sonoros
```
