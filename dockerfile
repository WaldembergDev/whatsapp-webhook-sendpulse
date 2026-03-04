# Imagem ultra-rápida com uv pré-instalado
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Diretório oficial da sua aplicação
WORKDIR /app

# Variáveis para otimizar o uv no Docker
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copia apenas os arquivos de trava primeiro (melhora o cache)
COPY pyproject.toml uv.lock ./

# Instala as dependências de forma otimizada
RUN uv sync --frozen --no-install-project --no-dev

# Copia o restante dos arquivos (incluindo o seu run.py)
COPY . .

# Expõe a porta que o Flask vai escutar
EXPOSE 5000

# Executa o projeto usando o uv
CMD ["uv", "run", "python", "run.py"]