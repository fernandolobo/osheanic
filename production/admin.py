# -*- coding: utf-8 -*-
from django.contrib import admin
from production.models import Empresa
from production.models import Cliente
from production.models import Pais
from production.models import Estado
from production.models import Cidade
from production.models import GrupoQuarto
from production.models import Quarto
from production.models import Salao
from production.models import Grupo
from production.models import Endereco
from production.models import Alimentacao
from production.models import Contato


class ContatoInline(admin.StackedInline):
    model = Contato
    extra = 1
    fieldsets = ((u'Contato de Emergência', {'fields': (('nome', 'fone'),)}),)


class AlimentacaoInline(admin.StackedInline):
    model = Alimentacao
    extra = 1
    fieldsets = ((None, {'fields': (('restricao', 'especificacao'), ('vegetariano', 'vegano'), ('peixe', 'frango'),)}),)


class EnderecoInline(admin.StackedInline):
    model = Endereco
    extra = 0
    fieldsets = ((None, {'fields': (('logradouro', 'numero'), ('bairro', 'cep'), ('pais', 'estado', 'cidade'),)}),
                 (u'tipo de endereço', {'fields': (('principal', 'entrega', 'cobranca', 'correspondencia'),)}),)


class ClienteAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': (('nome', 'sobrenome', 'sannyas'),
                                    ('telefone'),
                                    ('email', 'site'),
                                    ('rg', 'orgao_rg', 'data_emissao_rg'),
                                    ('cpf'),
                                    ('data_nascimento', 'sexo'),
                                    ('desde'))}),
                 )
    inlines = [EnderecoInline, ContatoInline, AlimentacaoInline]
    date_hierarchy = 'created_at'
    list_display = ('nome', 'sobrenome', 'sannyas', 'email', 'telefone')
    list_filter = ('sexo',)
    search_fields = ('nome', 'sobrenome', 'sannyas')


admin.site.register(Empresa)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Pais)
admin.site.register(Estado)
admin.site.register(Cidade)
admin.site.register(GrupoQuarto)
admin.site.register(Quarto)
admin.site.register(Salao)
admin.site.register(Grupo)
