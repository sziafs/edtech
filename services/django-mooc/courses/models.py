from django.db import models
# Create your models here.


class CourseManager(models.Manager):
    def search(self, query):
        '''
        Para facilitar as pesquisas
        A busca é feita no nome e na descrição
        --
        parameters
        query: para fazer uma consulta, onde se passa os parametros
        '''

        '''
        #aqui é um AND ( & )
        return self.get_queryset().filter(
            name__icontains=query,
            description__icontains=query
        )
        '''

        #Fazer um OR ( | )
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | 
            models.Q(description__icontains=query)
        )


class Course(models.Model):
    # nivel prog = nivel usuario
    name = models.CharField(
        verbose_name='Nome',
        max_length=100
    )

    slug = models.SlugField(
        verbose_name='Atalho'
    )

    description = models.TextField(
        verbose_name='Descrição Simples',
        blank=True
    )
    # blank=true é campo não obrigatório

    about = models.TextField(
        verbose_name='Sobre o Curso',
        blank=True
    )

    start_date = models.DateField(
        verbose_name='Data de inicio',
        blank=True,
        null=True
    )

    # imagem (django nao armazena imagens no db e sim seu path para um caminho fisico)
    # imagem que o usuario vai fazer upload
    # vai contatenar a partir do MEDIA_ROOT
    image = models.ImageField(
        upload_to='courses/images',
        verbose_name='Imagem',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    # auto_now_add = cria automaticamente a data e hora atual

    updated_at = models.DateTimeField(
        'Atualizado em',
        auto_now=True
    )
    # auto_now = pega automaticamente a data da hora atual e atualiza por cima da já criada

    objects = CourseManager()
    # .objects não fica mais o padrao do django e sim o customizado
    # Model tem o CourseManager como seu gerenciador agora
    
    def __str__(self):
        '''
        Para mostrar o nome do objeto no admin e nao o nome do tipo desse objeto
        '''
        return self.name

    def get_absolute_url(self):
        return "/courses/%s/" % self.slug

    class Meta:
        '''
        Arrumar o nome do model
        O django por padrão adiciona um S no final do nome
        '''
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['name'] #-name
