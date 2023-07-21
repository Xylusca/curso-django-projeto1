# Curso Django Projeto
Este é um projeto desenvolvido enquanto eu estava aprendendo Django e Pytest. 
O objetivo do projeto é criar uma página onde as pessoas possam visualizar receitas já publicadas, 
fazer login, logar e cadastrar novas receitas, sendo que a publicação estará sujeita à permissão do administrador.

## Funcionalidades Principais
* Visualização de receitas já publicadas.
* Sistema de login e autenticação.
* Cadastro de novas receitas com controle de permissão de publicação.

## Tecnologias Utilizadas
* Python
* Django
* HTML
* Bootstrap
  
## Executando a Aplicação
Para executar a aplicação localmente, siga os passos abaixo:

1 - Certifique-se de ter o Python instalado em sua máquina.
2 - Clone este repositório em um diretório de sua preferência:

```shel
git clone https://github.com/Xylusca/curso-django-projeto1.git
```
3 - Acesse o diretório do projeto:

```shel
cd curso-django-projeto
```

4 - Instale as dependências do projeto (recomendado criar e ativar um ambiente virtual antes):

```shel
pip install -r requirements.txt
```

5 - Realize as migrações do banco de dados:

```shel
python manage.py migrate
```

6 - Crie um superusuário para ter acesso às funcionalidades de administrador:

```shel
python manage.py createsuperuser
```
7 - Execute o servidor de desenvolvimento:

```shel
python manage.py runserver
```

Agora você pode acessar a aplicação localmente em seu navegador através do endereço http://localhost:8000/.

## Como Contribuir
Se tiver interesse em contribuir com o projeto, fique à vontade para abrir issues, enviar pull requests ou entrar em contato através do meu perfil no GitHub: [Xylusca](https://github.com/Xylusca)

Sinta-se à vontade para fazer sugestões, correções ou melhorias. Toda contribuição é bem-vinda!
