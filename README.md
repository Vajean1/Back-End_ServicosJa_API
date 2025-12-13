# 🛠️ ServiçoJá - API Back-end

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_Rest_Framework-3.16-ff1709?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-black?style=for-the-badge&logo=json-web-tokens&logoColor=white)

> **ServiçoJá** é uma plataforma inovadora que conecta clientes a prestadores de serviços locais de forma rápida e eficiente. Este repositório contém a **API Rest** que alimenta o ecossistema, gerenciando desde a autenticação e geolocalização até o sistema de contratação e avaliações.

---

## 🚀 Sobre o Projeto Integrador (SENAC)

O **ServiçoJá** foi desenvolvido para resolver a dificuldade de encontrar profissionais nas proximidades. A API atua como o núcleo do sistema, orquestrando as regras de negócio e fornecendo dados para as interfaces (Web/Mobile).

### 🌟 Destaques Técnicos
*   **Geolocalização Automática**: Integração com **BrasilAPI**, **ViaCEP** e **Nominatim** para converter endereços em coordenadas (Latitude/Longitude) automaticamente, permitindo busca por proximidade.
*   **Sistema de Avaliação Robusto**: Cálculo de média de notas com cache no banco de dados para performance.
*   **Gestão de Mídia**: Upload e armazenamento de imagens (perfil, portfólio, ícones) integrado com **Cloudinary**.
*   **Documentação Automática**: Swagger/OpenAPI gerado dinamicamente com **DRF Spectacular**.

---

## ⚙️ Stack Tecnológica

O projeto foi construído utilizando as melhores práticas do ecossistema Python:

*   **Core Framework**: [Django 5.2](https://www.djangoproject.com/)
*   **API Toolkit**: [Django Rest Framework (DRF)](https://www.django-rest-framework.org/)
*   **Autenticação**: JWT (JSON Web Tokens) via `djangorestframework-simplejwt`
*   **Banco de Dados**: PostgreSQL (Produção) / SQLite (Desenvolvimento)
*   **Documentação**: DRF Spectacular (Swagger UI & Redoc)
*   **Armazenamento de Arquivos**: Cloudinary
*   **Utilitários**: Geopy, Whitenoise, Gunicorn, Dotenv.

---

## ⚡ Funcionalidades da API

### 👤 Gestão de Contas (`/accounts`)
*   Registro diferenciado para **Clientes** e **Prestadores**.
*   Perfis detalhados com foto, biografia e dados de contato.
*   Endereçamento inteligente: o sistema preenche cidade, bairro e coordenadas baseando-se no CEP.

### 🛠️ Serviços (`/servicos`)
*   Categorização de serviços (ex: Limpeza, Reformas, Tecnologia).
*   Associação de prestadores a múltiplos tipos de serviço.

### 🤝 Contratações (`/contratacoes`)
*   Fluxo de solicitação de contato.
*   Registro de serviços realizados.
*   Histórico completo de interações entre cliente e prestador.

### ⭐ Avaliações (`/avaliacoes`)
*   Sistema de review (1 a 5 estrelas) com comentários.
*   Vínculo estrito: apenas serviços contratados podem ser avaliados.

### 📸 Portfólio (`/portfolio`)
*   Galeria de imagens para prestadores exibirem seus trabalhos anteriores.

---

## 📖 Documentação da API

A API possui documentação interativa completa. Com o servidor rodando, acesse:

*   **Swagger UI**: `http://127.0.0.1:8000/api/docs/`
*   **ReDoc**: `http://127.0.0.1:8000/api/redoc/`

---

## 🔗 Links Úteis

*   **Repositório Front-end**: [Acessar Repositório](https://github.com/Marcsfic98/servicosja)

