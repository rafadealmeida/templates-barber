from django.contrib import admin
from .models import (
    Barbearia,
    Profissional,
    Servico,
    InformacaoSite,
    ChaveConteudo,
    ImagensSite
)

@admin.register(Barbearia)
class BarbeariaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'proprietario', 'telefone_whatsapp', 'endereco')
    search_fields = ('nome', 'proprietario__username', 'telefone_whatsapp', 'endereco')
    list_filter = ('proprietario',)

@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'barbearia')
    search_fields = ('nome', 'barbearia__nome')
    list_filter = ('barbearia',)

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'barbearia', 'preco')
    search_fields = ('nome', 'barbearia__nome')
    list_filter = ('barbearia',)


@admin.register(InformacaoSite)
class InformacaoSiteAdmin(admin.ModelAdmin):
    list_display  = ("barbearia", "categoria", "chave", "conteudo")
    list_filter   = ("categoria", "barbearia")
    base_fields = [
        "barbearia", "categoria", "chave",
        "conteudo","url"]
    search_fields = ("conteudo",)

    def get_fields(self, request, obj=None):
        fields = self.base_fields.copy()

        categoria = (
            request.POST.get("categoria") or 
            getattr(obj, "categoria", None)
        )
        if categoria == InformacaoSite.Categoria.PROMOCOES:
            fields += ["data_inicio", "data_fim"]

        return fields

@admin.register(ChaveConteudo)
class ChaveConteudoAdmin(admin.ModelAdmin):
    list_display  = ("chave", "descricao")
    search_fields = ("chave",)

@admin.register(ImagensSite)
class ImagensSiteAdmin(admin.ModelAdmin):
    list_display  = ("barbearia", "imagem","chave" ,"criado_em")
    list_filter   = ("barbearia","chave")