# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.formats import number_format
from django.utils import timezone
from applib.lists import gender_list, status_room, status_res, type_person


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        _('criado em'), auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(
        _('modificado em'), auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True


class Pais(models.Model):
    codigo = models.IntegerField(unique=True, verbose_name=_(u'código'))
    nome_en = models.CharField(max_length=100, verbose_name=_(u'nome inglês'), blank=True)
    nome_pt = models.CharField(max_length=100, verbose_name=_(u'nome português'))
    sigla2 = models.CharField(max_length=2, verbose_name=_(u'sígla 2 dígitos'), blank=True)
    sigla3 = models.CharField(max_length=3, verbose_name=_(u'sígla 3 dígitoss'), blank=True)

    class Meta:
        ordering = ['nome_pt']
        verbose_name = "país"
        verbose_name_plural = u"países"

    def __unicode__(self):
        return self.nome_pt


class Estado(models.Model):
    pais = models.ForeignKey('Pais', verbose_name=_(u'país'))
    sigla = models.CharField(max_length=2, verbose_name=_(u'sígla'), blank=True)
    nome = models.CharField(max_length=100, verbose_name=_('nome'))

    class Meta:
        ordering = ['nome']
        verbose_name = "estado"
        verbose_name_plural = "estados"

    def __unicode__(self):
        return self.nome


class Cidade(models.Model):
    estado = models.ForeignKey('Estado', verbose_name=_('estado'))
    nome = models.CharField(max_length=100, verbose_name=_('nome'))

    class Meta:
        ordering = ['nome']
        verbose_name = "cidade"
        verbose_name_plural = "cidades"

    def __unicode__(self):
        return self.nome


class Endereco(models.Model):
    logradouro = models.CharField(max_length=100, verbose_name=_('logradouro'))
    numero = models.CharField(max_length=10, verbose_name=_(u'número'))
    complemento = models.CharField(max_length=100, verbose_name=_('complemento'), blank=True)
    bairro = models.CharField(max_length=100, verbose_name=_('bairro'), blank=True)
    cep = models.CharField(max_length=10, verbose_name=_('CEP'), blank=True)
    cidade = models.ForeignKey('Cidade', verbose_name=_('cidade'), blank=True)
    estado = models.ForeignKey('Estado', verbose_name=_('estado'), blank=True)
    pais = models.ForeignKey('Pais', verbose_name=_(u'país'), blank=True)
    principal = models.BooleanField(verbose_name=_('principal'), blank=True)
    entrega = models.BooleanField(verbose_name=_('entrega'), blank=True)
    cobranca = models.BooleanField(verbose_name=_(u'cobrança'), blank=True)
    correspondencia = models.BooleanField(verbose_name=_(u'correspondência'), blank=True)
    pessoa = models.ForeignKey('Pessoa', verbose_name=_('pessoa'))

    class Meta:
        verbose_name = u"endereço"
        verbose_name_plural = u"endereços"

    def __unicode__(self):
        return self.logradouro


class Empresa(models.Model):
    fk_empresa = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('empresa'))
    razao_social = models.CharField(max_length=200, verbose_name=_(u'razão social'))
    nome_fantasia = models.CharField(max_length=200, verbose_name=_('nome fantasia'))
    cnpj = models.CharField(max_length=14, verbose_name=_(u'CNPJ'))
    inscricao_estadual = models.CharField(max_length=30, blank=True, null=True, verbose_name=_(u'inscrição estadual'))
    inscricao_estadual_st = models.CharField(max_length=30, blank=True, null=True, verbose_name=_(u'situação ie'))
    inscricao_municipal = models.CharField(max_length=30, blank=True, null=True, verbose_name=_(u'inscrição municipal'))
    tipo = models.CharField(max_length=1, verbose_name=_(u'tipo'), blank=True)
    data_cadastro = models.DateField(verbose_name=_(u'data de cadastro'))
    suframa = models.CharField(max_length=9, blank=True, null=True, verbose_name=_('SUFRAMA'))
    email = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('email'))
    imagem_logotipo = models.ImageField(verbose_name=_('logotipo'), blank=True)
    crt = models.IntegerField(blank=True, null=True, verbose_name=_('CRT'))
    tipo_regime = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('tipo de regime'))
    aliquota_pis = models.DecimalField(blank=True, null=True, verbose_name=_(
        u'alíquota pis'), max_digits=3, decimal_places=2)
    aliquota_confins = models.DecimalField(blank=True, null=True, verbose_name=_(
        u'alíquota confins'), max_digits=3, decimal_places=2)

    def __unicode__(self):
        return self.nome_fantasia

    def get_absolute_url(self):
        return reverse('empresa_edit', kwargs={'pk': self.pk})


class Pessoa(TimeStampedModel):
    nome = models.CharField(max_length=150, verbose_name=_('nome'))
    tipo = models.CharField(max_length=1, verbose_name=_('tipo'), editable=False, choices=type_person)
    email = models.CharField(max_length=250, verbose_name=_('email'), blank=True)
    telefone = models.CharField(max_length=20, verbose_name=_('telefone'), blank=True)
    site = models.CharField(max_length=250, verbose_name=_('site'), blank=True)


class PessoaFisica(Pessoa):
    sobrenome = models.CharField(max_length=150, verbose_name=_('sobrenome'), null=True, blank=True)
    sannyas = models.CharField(max_length=150, verbose_name=_('sannyas'), null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True, verbose_name=_('CPF'), null=True, blank=True)
    rg = models.CharField(max_length=25, unique=True, verbose_name=_('RG'), null=True, blank=True)
    orgao_rg = models.CharField(max_length=25, verbose_name=_(u'orgão RG'), null=True, blank=True)
    data_emissao_rg = models.DateField(verbose_name=_(u'data de emissão RG'), null=True, blank=True)
    data_nascimento = models.DateField(verbose_name=_('data de nascimento'), null=True, blank=True)
    sexo = models.CharField(max_length=1, verbose_name=_('sexo'), choices=gender_list, null=True, blank=True)
    profissao = models.CharField(max_length=150, verbose_name=_(u'profissão'), null=True, blank=True)
    Pessoa.tipo = 'F'

    class Meta:
        abstract = True


class PessoaJuridica(Pessoa):
    cnpj = models.CharField(max_length=14, unique=True, verbose_name=_('CNPJ'), blank=True)
    razao_social = models.CharField(max_length=150, verbose_name=_(u'razão social'), blank=True)
    inscricao_municipal = models.CharField(max_length=30, verbose_name=_(u'inscrição municipal'), blank=True)
    data_constituicao = models.DateField(verbose_name=_(u'data de constituição'), blank=True)
    Pessoa.tipo = 'J'

    class Meta:
        abstract = True


class Alimentacao(models.Model):
    restricao = models.BooleanField(verbose_name=_(u'restrição alimentar/alergia'), blank=True)
    especificacao = models.CharField(max_length=250, null=True, blank=True,
                                     verbose_name=_(u'especificação da restrição'))
    vegetariano = models.BooleanField(verbose_name=_('vegetariano'), blank=True)
    vegano = models.BooleanField(verbose_name=_('vegano'), blank=True)
    peixe = models.BooleanField(verbose_name=_('come peixe'), blank=True)
    frango = models.BooleanField(verbose_name=_('come frango'), blank=True)
    cliente = models.OneToOneField('cliente', verbose_name=_('cliente'))

    class Meta:
        verbose_name = u"informação alimentar"
        verbose_name_plural = u"informações alimentares"

    def __unicode__(self):
        return self.especificacao


class Contato(models.Model):
    nome = models.CharField(max_length=150, verbose_name=_('nome'), null=True, blank=True)
    fone = models.CharField(max_length=20, verbose_name=_('telefone'), null=True, blank=True)
    cliente = models.ForeignKey('cliente', verbose_name=_('cliente'), null=True, blank=True)

    class Meta:
        verbose_name = u"contato de emergência"
        verbose_name_plural = u"contatos de emergência"


class Cliente(PessoaFisica):
    desde = models.DateField(verbose_name=_('desde'), null=True, blank=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def __unicode__(self):
        return self.nome


class GrupoQuarto(models.Model):
    nome = models.CharField(max_length=150, verbose_name=_('nome'))

    class Meta:
        ordering = ["nome"]
        verbose_name = u"Grupo de Quarto"
        verbose_name_plural = u"Grupos de Quartos"

    def __unicode__(self):
        return self.nome


class Quarto(models.Model):
    codigo = models.CharField(max_length=100, verbose_name=_(u'codigo'), unique=True)
    nome = models.CharField(max_length=150, verbose_name=_('nome'))
    capacidade = models.IntegerField(verbose_name=_('capacidade'))
    status = models.CharField(max_length=1, verbose_name=_(u'situação'), choices=status_room, default='L')
    grupoquarto = models.ForeignKey('GrupoQuarto', verbose_name=_('grupo de quarto'))
    preco = models.DecimalField(verbose_name=_(u'preço'), max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["nome", "grupoquarto"]

    def __unicode__(self):
        return self.nome


class Salao(models.Model):
    nome = models.CharField(max_length=150, verbose_name=_('nome'))
    capacidade = models.IntegerField(verbose_name=_('capacidade'))

    class Meta:
        ordering = ["nome"]
        verbose_name = u"salão"
        verbose_name_plural = u"salões"

    def __unicode__(self):
        return self.nome


class Terapeuta(PessoaFisica):
    pass


class Grupo(TimeStampedModel):
    nome = models.CharField(max_length=150, verbose_name=_('nome'))
    vagas = models.PositiveIntegerField(verbose_name=_('vagas'))
    data_inicio = models.DateTimeField(verbose_name=_(u'data de início'))
    data_fim = models.DateTimeField(verbose_name=_('data de término'))
    valor_inscricao = models.DecimalField(verbose_name=_(u'valor de inscrição'), max_digits=10, decimal_places=2)
    valor_grupo = models.DecimalField(verbose_name=_(u'valor do grupo'), max_digits=10, decimal_places=2)
    taxa_producao = models.DecimalField(verbose_name=_(u'taxa de produção'), max_digits=3, decimal_places=2)
    taxa_terapeuta = models.DecimalField(verbose_name=_(u'taxa do terapeuta'), max_digits=3, decimal_places=2)

    class Meta:
        ordering = ["nome"]
        verbose_name = "grupo"
        verbose_name_plural = "grupos"

    def get_valor_inscricao(self):
        return u"R$ %s" % number_format(self.valor_inscricao, 2)

    def get_valor_grupo(self):
        return u"R$ %s" % number_format(self.valor_grupo, 2)

    def __unicode__(self):
        return self.nome


class Reserva(models.Model):
    cliente = models.ForeignKey(u'Cliente', verbose_name=(u'cliente'))
    quarto = models.ForeignKey(u'Quarto', verbose_name=(u'quarto'))
    criado = models.DateTimeField()
    reserva_de = models.DateTimeField(null=True, blank=True)
    reserva_ate = models.DateTimeField(null=True, blank=True)
    entrada = models.DateTimeField(null=True, blank=True)
    saida = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20,choices=status_res)

