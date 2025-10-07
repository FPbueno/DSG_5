"""
Modelos SQLAlchemy para o banco de dados MySQL
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Enum, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum

class TipoUsuario(str, enum.Enum):
    CLIENTE = "cliente"
    PRESTADOR = "prestador"

class StatusSolicitacao(str, enum.Enum):
    AGUARDANDO = "aguardando_orcamentos"
    COM_ORCAMENTOS = "com_orcamentos"
    FECHADA = "fechada"
    CANCELADA = "cancelada"

class StatusOrcamento(str, enum.Enum):
    AGUARDANDO = "aguardando"
    ACEITO = "aceito"
    RECUSADO = "recusado"
    REALIZADO = "realizado"

# ============= MODELOS DE USUÁRIOS =============

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    telefone = Column(String(20), nullable=True)
    cpf = Column(String(255), nullable=True)  # Será criptografado
    endereco = Column(Text, nullable=True)
    avaliacao_media = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    solicitacoes = relationship("Solicitacao", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente(id={self.id}, nome='{self.nome}', email='{self.email}')>"


class Prestador(Base):
    __tablename__ = "prestadores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    telefone = Column(String(20), nullable=True)
    cpf_cnpj = Column(String(255), nullable=True)  # Será criptografado
    categorias = Column(JSON, nullable=False, default=list)  # ["Pintura", "Elétrica"]
    regioes_atendimento = Column(JSON, nullable=False, default=list)  # ["Zona Sul", "Centro"]
    avaliacao_media = Column(Float, default=0.0)
    portfolio = Column(JSON, nullable=True)  # URLs de imagens, descrições
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    orcamentos = relationship("Orcamento", back_populates="prestador")

    def __repr__(self):
        return f"<Prestador(id={self.id}, nome='{self.nome}', email='{self.email}')>"


# ============= MODELOS DE SOLICITAÇÕES E ORÇAMENTOS =============

class Solicitacao(Base):
    __tablename__ = "solicitacoes"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    categoria = Column(String(100), nullable=False, index=True)
    descricao = Column(Text, nullable=False)
    localizacao = Column(String(255), nullable=False)
    prazo_desejado = Column(String(100), nullable=True)
    informacoes_adicionais = Column(Text, nullable=True)
    status = Column(
        Enum(StatusSolicitacao, native_enum=False, length=30),
        default=StatusSolicitacao.AGUARDANDO,
        nullable=False,
        index=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    cliente = relationship("Cliente", back_populates="solicitacoes")
    orcamentos = relationship("Orcamento", back_populates="solicitacao", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Solicitacao(id={self.id}, categoria='{self.categoria}', status='{self.status}')>"


class Orcamento(Base):
    __tablename__ = "orcamentos"

    id = Column(Integer, primary_key=True, index=True)
    solicitacao_id = Column(Integer, ForeignKey("solicitacoes.id"), nullable=False)
    prestador_id = Column(Integer, ForeignKey("prestadores.id"), nullable=False)
    
    # Valores do ML (internos)
    valor_ml_minimo = Column(Float, nullable=False)
    valor_ml_sugerido = Column(Float, nullable=False)
    valor_ml_maximo = Column(Float, nullable=False)
    
    # Valor do prestador (visível ao cliente)
    valor_proposto = Column(Float, nullable=False)
    
    prazo_execucao = Column(String(100), nullable=False)
    observacoes = Column(Text, nullable=True)
    condicoes = Column(Text, nullable=True)
    status = Column(
        Enum(StatusOrcamento, native_enum=False, length=20, values_callable=lambda x: [e.value for e in x]),
        default=StatusOrcamento.AGUARDANDO,
        nullable=False,
        index=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    solicitacao = relationship("Solicitacao", back_populates="orcamentos")
    prestador = relationship("Prestador", back_populates="orcamentos")

    def __repr__(self):
        return f"<Orcamento(id={self.id}, valor={self.valor_proposto}, status='{self.status}')>"


# ============= MODELO DE AVALIAÇÕES =============

class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)
    orcamento_id = Column(Integer, ForeignKey("orcamentos.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    prestador_id = Column(Integer, ForeignKey("prestadores.id"), nullable=False)
    estrelas = Column(Integer, nullable=False)  # 1 a 5
    comentario = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Avaliacao(id={self.id}, prestador_id={self.prestador_id}, estrelas={self.estrelas})>"