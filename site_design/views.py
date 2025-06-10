from django.shortcuts import render
from .models import InformacaoSite, ImagensSite,Barbearia


def index(request):

    barbearia_atual = Barbearia.objects.first()

    queryConteudo = (
        InformacaoSite.objects
        .filter(barbearia=barbearia_atual,categoria=InformacaoSite.Categoria.CONTEUDO_SITE)
        .select_related("chave")
        .order_by("chave__chave")        
    )
    conteudo = {obj.chave.chave: obj.conteudo for obj in queryConteudo}

    queryImagem = (
    ImagensSite.objects
    .filter(barbearia=barbearia_atual)
    .order_by("-criado_em")
    )

    for img in queryImagem:
        conteudo[img.chave.chave] = img.imagem.url

    context = {"conteudo": conteudo}
    print(context)
    return render(request, "site_design/index.html", context)
