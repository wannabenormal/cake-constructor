from django.db import models


class Height(models.Model):
    height = models.CharField(
        'Высота',
        max_length=25,
        help_text='Высота торта в этажах (1, 2, 3 и т.д)',
    )
    price = models.PositiveIntegerField(
        'Цена'
    )

    def __str__(self):
        return self.height

    class Meta:
        verbose_name = 'Этаж торта'
        verbose_name_plural = 'Этажи торта'


class Shape(models.Model):
    shape = models.CharField(
        'Форма',
        max_length=25,
        help_text='Форма торта (круг, шар, четырехмерный куб, бутылка Клейна и т.д)',
    )
    price = models.PositiveIntegerField(
        'Цена'
    )

    def __str__(self):
        return self.shape

    class Meta:
        verbose_name = 'Форма торта'
        verbose_name_plural = 'Формы тортов'


class Topping(models.Model):
    topping = models.CharField(
        'Топпинг',
        max_length=25,
        help_text='Шоколадный, ванильный, медовый и т.д',
    )
    price = models.PositiveIntegerField(
        'Цена'
    )

    def __str__(self):
        return self.topping

    class Meta:
        verbose_name = 'Топпинг'
        verbose_name_plural = 'Топпинги'


class Berry(models.Model):
    berry = models.CharField(
        'Ягода',
        max_length=25,
        help_text='Клубника, голубика, ежевика, малина..',
    )
    price = models.PositiveIntegerField(
        'Цена'
    )

    def __str__(self):
        return self.berry

    class Meta:
        verbose_name = 'Ягода'
        verbose_name_plural = 'Ягоды'


class Decoration(models.Model):
    decoration = models.CharField(
        'Украшение',
        max_length=10,
        help_text='Марципан, пекан, фундук, шоколадная крошка ..',
    )
    price = models.PositiveIntegerField(
        'Цена'
    )

    def __str__(self):
        return self.decoration

    class Meta:
        verbose_name = 'Украшение'
        verbose_name_plural = 'Украшения'


class Advertisement(models.Model):
    title = models.CharField(
        'Название рекламной акции',
        max_length=100
    )
    start_date = models.DateTimeField(
        'Начало рекламной акции',
        auto_now=True,
    )
    end_date = models.DateTimeField(
        'Конец рекламной акции',
        blank=True
    )
    unique_link = models.CharField(
        'Уникальная ссылка-идентификатор для рекламной акции',
        max_length=255
    )

    def __str__(self):
        return f' Рекламная акция "{self.title}" от {self.start_date}'

    class Meta:
        verbose_name = 'Рекламная акция'
        verbose_name_plural = 'Рекламные акции'


class Customer(models.Model):
    name = models.CharField(
        'Имя',
        max_length=150,
        help_text='Имя',
    )
    email = models.CharField(
        'Почта',
        max_length=200,
        help_text='username@mail.ru',
    )
    phonenumber = models.CharField(
        'Номер телефона',
        max_length=50,
        help_text='+79987651244',
    )
    referral = models.ForeignKey(
        Advertisement,
        verbose_name='Реклама, по которой перешел пользователь',
        on_delete=models.CASCADE,
        max_length=100,
        blank=True,
        null=True
    )
    address = models.CharField(
        'Адрес заказчика',
        max_length=100,
    )

    def __str__(self):
        return f'{self.name} - {self.phonenumber}'

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'


class Cake(models.Model):
    name = models.CharField(
        'Название торта',
        max_length=200,
        help_text='Название',
    )
    description = models.CharField(
        'Описание',
        max_length=200,
        help_text='Описание',
        blank=True
    )
    height = models.ForeignKey(
        Height,
        verbose_name='Высота торта в этажах',
        on_delete=models.CASCADE,
        related_name='cake_height'
    )
    shape = models.ForeignKey(
        Shape,
        verbose_name='Форма торта',
        on_delete=models.CASCADE,
        related_name='cake_shape',
    )
    topping = models.ForeignKey(
        Topping,
        verbose_name='Топпинг',
        on_delete=models.CASCADE,
        related_name='cake_topping'
    )
    berry = models.ForeignKey(
        Berry,
        verbose_name='Ягоды',
        on_delete=models.CASCADE,
        related_name='cake_berry',
        blank=True,
        null=True
    )
    decoration = models.ForeignKey(
        Decoration,
        verbose_name='Украшение',
        on_delete=models.CASCADE,
        related_name='cake_decoration',
        blank=True,
        null=True
    )
    inscription = models.CharField(
        'Надпись',
        max_length=50,
        help_text='Надпись на торте',
        blank=True,
        null=True
    )

    def add_price(self):
        self.price = 0
        attributes = [self.shape, self.height, self.topping, self.berry, self.decoration]
        # FIXME 'hardcode'
        for attribute in attributes:
            try:
                self.price += attribute.price
            except AttributeError:
                pass
        return self

    def __str__(self):
        return f'Торт {self.name}'

    class Meta:
        verbose_name = 'Торт'
        verbose_name_plural = 'Торты'


class Order(models.Model):
    STATUSES = (
        ('В обработке', 'В обработке'),
        ('Готовится', 'Готовится'),
        ('Доставлен', 'Доставлен'),
    )
    customer = models.ForeignKey(
        Customer,
        verbose_name='Заказчик',
        on_delete=models.CASCADE,
        related_name='customer',
    )
    cake = models.ForeignKey(
        Cake,
        verbose_name='Торт',
        on_delete=models.CASCADE,
        related_name='cake',
    )
    status = models.CharField(
        'Статус',
        choices=STATUSES,
        max_length=255,
        db_index=True
    )
    price = models.IntegerField(
        'Общая стоимость'
    )
    creation_time = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
    )
    delivery_datetime = models.DateTimeField(
        'Дата и время доставки',
        db_index=True
    )
    delivery_address = models.CharField(
        'Адрес доставки',
        max_length=255,
        db_index=True
    )
    comment = models.CharField(
        'Комментарии',
        max_length=300,
        blank=True
    )
    is_urgent = models.BooleanField(
        'Срочный?',
        default=False,
        db_index=True
    )

    def __str__(self):
        return f'Заказ №{self.id} покупателя {self.customer.name} на адрес {self.customer.address}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'