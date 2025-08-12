from django.contrib.auth.models import User
from django.db import models
import uuid

from django.forms import ValidationError
from django.core.validators import RegexValidator


hex_color_validator = RegexValidator(
    r'^#(?:[0-9a-fA-F]{3}){1,2}$',
    'Informe a cor em HEX. Ex.: #A1B2C3'
)

class Barbearia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)  # Upload local
    cor_primaria   = models.CharField(
        "Cor primária", max_length=7, blank=True, null=True,
        validators=[hex_color_validator]
    )
    cor_secundaria = models.CharField(
        "Cor secundária", max_length=7, blank=True, null=True,
        validators=[hex_color_validator]
    )
    cor_destaque   = models.CharField(
        "Cor de destaque", max_length=7, blank=True, null=True,
        validators=[hex_color_validator]
    )
    telefone_whatsapp = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    google_maps_url = models.TextField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    proprietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="barbearias")
    def __str__(self):
        return self.nome 

class ChaveConteudo(models.Model):
    id     = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chave  = models.CharField(max_length=50, unique=True)
    descricao = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.chave

class Profissional(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    barbearia = models.ForeignKey(Barbearia, on_delete=models.CASCADE, related_name="profissionais")
    nome = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='profissionais/', blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)

    servicos = models.ManyToManyField(
        "Servico",
        through="ProfissionalServico",
        related_name="profissionais",
    )

class Servico(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    barbearia = models.ForeignKey(Barbearia, on_delete=models.CASCADE, related_name="servicos")
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    imagem = models.ImageField(upload_to='servicos/', blank=True, null=True)

class ProfissionalServico(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profissional= models.ForeignKey(Profissional, on_delete=models.CASCADE)
    servico= models.ForeignKey(Servico,on_delete=models.CASCADE)

    duracao_min  = models.PositiveIntegerField(blank=True, null=True) 
    preco_especial = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        unique_together = [("profissional", "servico")]
        ordering = ["profissional", "servico"]

    def __str__(self):
        return f"{self.profissional.nome} – {self.servico.nome}"

class PromocaoEvento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    barbearia = models.ForeignKey(Barbearia, on_delete=models.CASCADE, related_name="promocoes_eventos")
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='promocoes_eventos/', blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)

class InformacaoSite(models.Model):
    class Categoria(models.TextChoices):
        CONTEUDO_SITE = "CONTEUDO_SITE", "Conteúdo do site"
        REDES_SOCIAIS = "REDES_SOCIAIS", "Redes sociais"
        PROMOCOES     = "PROMOCOES",     "Promoções"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    barbearia = models.ForeignKey(Barbearia, on_delete=models.CASCADE,
                                  related_name="informacoes_site")
    categoria = models.CharField(max_length=50, choices=Categoria.choices)

    # chave de layout (só faz sentido quando categoria = CONTEUDO_SITE)
    chave = models.ForeignKey(ChaveConteudo, on_delete=models.CASCADE,
                              blank=True, null=True)

    # campos genéricos – preencha apenas os que se aplicarem
    conteudo    = models.TextField(blank=False, null=True)

    # URL simples (ex.: link da rede social)
    url = models.URLField(blank=True, null=True)

    # datas – úteis para promoções
    data_inicio = models.DateField(blank=True, null=True)
    data_fim    = models.DateField(blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["categoria", "chave", "conteudo"]
        unique_together = [
            ("barbearia", "categoria", "chave"),  # evita duplicar a mesma info
        ]

    def __str__(self):
        return f"{self.barbearia.nome} | {self.get_categoria_display()} | {self.chave or self.conteudo}"
    
    def clean(self):
        super().clean()

        if self.categoria == self.Categoria.PROMOCOES:
            if not self.data_inicio or not self.data_fim:
                raise ValidationError(
                    "Promoções precisam de “data início” e “data fim”."
                )
        else:
            if self.data_inicio or self.data_fim:
                raise ValidationError(
                    "Os campos de data só podem ser preenchidos quando a categoria é PROMOCOES."
                )

class ImagensSite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    barbearia = models.ForeignKey(Barbearia, on_delete=models.CASCADE,
                                  related_name="imagens_site")
    imagem = models.ImageField(upload_to="imagens_site/")
    criado_em = models.DateTimeField(auto_now_add=True)
    # chave de layout (só faz sentido quando categoria = CONTEUDO_SITE)
    chave = models.ForeignKey(ChaveConteudo, on_delete=models.CASCADE,
                              blank=True, null=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.barbearia.nome} | {self.imagem.name}"
