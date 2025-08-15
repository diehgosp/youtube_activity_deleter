# YouTube Activity Deleter

Deleta todos os seus comentários no You Tube

---
##Uso

- Baixe o aplicativo em https://tinyurl.com/ytdeleter
- Duplo clique em deleter.exe
- Clique em Login e entre em sua conta, salvando o login.
- Clique em Deletar Atividade e aguarde o processo concluir.


---

## Recursos
- Login manual no seu perfil do Google (reutiliza o mesmo perfil depois).
- Deleção automatizada dos itens visíveis (“Delete activity item”).
- Rolagem progressiva para carregar mais resultados.
- Contador final de itens deletados.
- Ícone da janela via `favicon.ico` (opcional).

---

## Requisitos
- **Windows** (script usa caminhos e processo `browser.exe` específicos).
- **Python 3.9+**  
- Bibliotecas: `playwright`, `psutil`, `tkinter`.
- **Chromium** portátil renomeado para `browser.exe`.

---

## Estrutura de pastas esperada
```
seu_projeto/
├─ deleter.py
├─ favicon.ico (opcional)
├─ chrome/
│ └─ browser.exe (Chromium portátil renomeado)
└─ user_data/ (criada automaticamente; perfil do Chromium)
```

---

## Instalação
1. Crie/ative um venv (opcional).  
2. Instale dependências:
    ```bash
    pip install playwright psutil
    ```

> Observação: Baixe o chromium de https://github.com/Hibbiki/chromium-win64/releases/download/v138.0.7204.184-r1465706/chrome.sync.7z
Ou para uma versão atualizada, obtenha o "Archive" https://chromium.woolyss.com para Windows.

---

## Como usar
1. Rode o app:  
    ```bash
    python deleter.py
    ```
2. Clique **Login**:
   - Abre o Chromium com o perfil em `user_data/`.
   - Faça login no Google.
   - Feche a janela do Chromium quando terminar.
3. Clique **Deletar atividade**:
   - Fecha processos antigos do `browser.exe`.
   - Abre a página `https://myactivity.google.com/page?hl=en...`.
   - Clica em todos os “Delete activity item”.
   - Rola para carregar mais e repete até o fim.
   - Mostra um alerta com a contagem.

---

## Configuração
- **Caminhos**:
  - `CHROMIUM_PATH = .../chrome/browser.exe`
  - `USER_DATA_DIR = .../user_data`
- **URLs**:
  - `LOGIN_URL` e `ACTIVITY_URL`
- **Seletor**:
  - `SEL_DELETE = 'button[aria-label^="Delete activity item"]'`

---

## Solução de problemas
- **TclError: `bitmap "favicon.ico" not defined`**: arquivo não encontrado, ajuste o caminho.
- **Chromium não encontrado**: verifique `chrome/browser.exe`.
- **Nada é deletado**: confira idioma e seletor.
- **Bloqueios do Google**: faça login manual antes de deletar.

---

## Avisos
- Exclusões são permanentes.
- Mudanças no layout do Google podem exigir ajustes.
- Não nos responsabilizamos por qualquer uso indevido deste script.


