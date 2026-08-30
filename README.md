# 🎬 Old Phone Media Server

Um servidor de mídia **leve e simples**, desenvolvido com **Flask**, pensado para transformar um celular antigo em um servidor pessoal de filmes usando **Termux**.

O projeto permite armazenar, pesquisar e assistir filmes através do navegador em qualquer dispositivo conectado à mesma rede local.

---

## ✨ Funcionalidades

* 🎬 Listagem de filmes disponíveis
* 🔎 Pesquisa de filmes
* ▶️ Player de vídeo integrado
* ⏩ Controle de velocidade de reprodução
* 📐 Controle de proporção do vídeo
* ⬆️ Upload de novos filmes
* 🗑️ Exclusão de filmes
* 🌙 Interface escura
* 📱 Interface responsiva
* ⚡ Baixo consumo de recursos
* 📡 Acesso através da rede local
* 📲 Compatível com celulares antigos usando Termux

---

## 🛠️ Tecnologias

* **Python**
* **Flask**
* **HTML5**
* **CSS3**
* **JavaScript**
* **Termux** para execução em dispositivos Android

---

# 📱 Como executar no Termux

O projeto é executado diretamente em um celular Android usando o [Termux](https://termux.dev/).

## 1. Atualize os pacotes

```bash
pkg update && pkg upgrade -y
```

## 2. Instale Python e Git

```bash
pkg install python git
```

## 3. Permita o acesso ao armazenamento

```bash
termux-setup-storage
```

Conceda a permissão de armazenamento quando solicitado.

## 4. Clone o projeto

```bash
git clone https://github.com/n0x-http/Old-Phone-Media-Server.git
cd old-phone-media-server
```

## 5. Instale as dependências

**Importante:** o Flask não vem instalado junto com o Python. Instale as dependências antes de executar o servidor:

```bash
python -m pip install -r requirements.txt
```

O arquivo `requirements.txt` contém:

```text
Flask
```

Caso você não tenha o `requirements.txt`, instale o Flask diretamente:

```bash
python -m pip install flask
```

Você pode verificar se o Flask foi instalado corretamente com:

```bash
python -m pip show flask
```

## 6. Inicie o servidor

```bash
python app.py
```

O servidor estará rodando na porta `5000`.

---

# 🌐 Acessando pelo celular ou outro dispositivo

Para acessar o servidor a partir de outro dispositivo conectado à mesma rede Wi-Fi, descubra o endereço IP do celular.

No Termux, você pode utilizar:

```bash
ifconfig
```

ou:

```bash
ip addr
```

Procure pelo endereço IP da interface de rede, normalmente algo semelhante a:

```text
192.168.1.100
```

Depois, em outro dispositivo conectado à mesma rede, acesse:

```text
http://192.168.1.100:5000
```

> Substitua `192.168.1.100` pelo IP real do celular.

---

# 📁 Estrutura do projeto

```text
old-phone-media-server/
│
├── app.py
├── requirements.txt
│
├── movies/
│   ├── filme1.mp4
│   └── filme2.mp4
│
├── templates/
│   ├── index.html
│   ├── player.html
│   └── upload.html
│
└── README.md
```

### Arquivos principais

| Arquivo/Pasta           | Descrição                                |
| ----------------------- | ---------------------------------------- |
| `app.py`                | Aplicação principal Flask                |
| `requirements.txt`      | Dependências do projeto                  |
| `movies/`               | Diretório onde os filmes são armazenados |
| `templates/index.html`  | Página principal com a lista de filmes   |
| `templates/player.html` | Página do player                         |
| `templates/upload.html` | Página de upload                         |
| `README.md`             | Documentação do projeto                  |

---

# 🔒 Uso em rede local

O projeto foi pensado principalmente para **uso dentro de uma rede local**.

Isso significa que o servidor pode ser utilizado, por exemplo:

```text
📱 Celular antigo
      │
      │ Wi-Fi
      ▼
📺 Smart TV
💻 Notebook
🖥️ Computador
📱 Outro celular
```

Todos os dispositivos precisam estar conectados à mesma rede para acessar o servidor através do IP do celular.

---

# 🔋 Mantendo o servidor ativo no Termux

Em alguns celulares, o Android pode suspender processos em segundo plano para economizar bateria.

Para ajudar a impedir que o dispositivo entre em suspensão enquanto o servidor está funcionando, utilize:

```bash
termux-wake-lock
```

Depois inicie o servidor:

```bash
python app.py
```

Para liberar o bloqueio posteriormente:

```bash
termux-wake-unlock
```

> O comportamento pode variar dependendo da versão do Android e das configurações de economia de bateria do fabricante.

---

# ⚡ Dicas para aumentar a velocidade

Rodando em um celular via Termux, alguns ajustes fazem bastante diferença na velocidade de upload e streaming:

* **Ative o `termux-wake-lock`** antes de subir o servidor e **desative a otimização de bateria** do Termux nas configurações do Android (Config > Apps > Termux > Bateria > Sem restrições). O Doze mode é a causa mais comum de quedas de desempenho "aleatórias".
* **Desative o modo debug** e rode com threads ao iniciar o Flask:

  ```python
  app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
  ```

* **Evite salvar os filmes em armazenamento compartilhado** (`~/storage/shared/...`). Essa camada usa FUSE e é mais lenta. Prefira salvar direto na home do Termux:

  ```python
  MOVIES_FOLDER = Path.home() / "movies"
  ```

* **Use um servidor WSGI mais leve que o dev server do Flask**, como o `waitress`:

  ```bash
  pip install waitress
  ```

  ```python
  from waitress import serve
  serve(app, host="0.0.0.0", port=5000, threads=4)
  ```

* **Prefira Wi-Fi 5GHz e mantenha o celular perto do roteador** — o chipset Wi-Fi de celulares costuma ter upload mais fraco que o de notebooks/roteadores, especialmente em 2.4GHz.

---

# ⚠️ Observações

* Atualmente, o projeto foi pensado para trabalhar com arquivos **`.mp4`**.
* O servidor foi desenvolvido para **uso em rede local**.
* O desempenho depende do hardware do dispositivo utilizado como servidor.
* Celulares antigos podem apresentar limitações ao transmitir vídeos de alta resolução.
* O armazenamento disponível no celular limita a quantidade de filmes que podem ser armazenados.
* Recomenda-se utilizar uma rede Wi-Fi estável para reprodução dos vídeos.
* O servidor não foi projetado, por padrão, para ficar exposto diretamente à internet.
* Para evitar problemas de segurança, não exponha o servidor diretamente à internet sem implementar autenticação e outras medidas de proteção.

---

# 📄 Licença

Este projeto está disponível sob a licença **MIT**.

---
