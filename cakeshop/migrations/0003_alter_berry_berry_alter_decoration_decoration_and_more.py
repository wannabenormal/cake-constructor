# Generated by Django 4.0.4 on 2022-04-27 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakeshop', '0002_alter_cake_berry_alter_cake_decoration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='berry',
            name='berry',
            field=models.CharField(choices=[('bramble', 'Ежевика'), ('raspberry', 'Малина'), ('blueberry', 'Голубика'), ('strawberry', 'Клубника')], help_text='Клубника, голубика, ежевика, малина..', max_length=15, verbose_name='Ягода'),
        ),
        migrations.AlterField(
            model_name='decoration',
            name='decoration',
            field=models.CharField(choices=[('marz', 'Марципан'), ('pecan', 'Пекан'), ('hazel', 'Фундук'), ('bese', 'Безе'), ('pist', 'Фисташки'), ('marsh', 'Маршмеллоу')], help_text='Марципан, пекан, фундук, шоколадная крошка ..', max_length=10, verbose_name='Украшение'),
        ),
        migrations.AlterField(
            model_name='height',
            name='height',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3')], help_text='Высота торта в этажах (1, 2, 3 и т.д)', verbose_name='Высота'),
        ),
        migrations.AlterField(
            model_name='shape',
            name='shape',
            field=models.CharField(choices=[('C', 'Круг'), ('S', 'Квадрат'), ('R', 'Прямоугольник')], help_text='Форма торта (круг, шар, четырехмерный куб, бутылка Клейна и т.д)', max_length=15, verbose_name='Форма'),
        ),
        migrations.AlterField(
            model_name='topping',
            name='topping',
            field=models.CharField(choices=[('without', 'Без топинга'), ('white_sauce', 'Белый Соус'), ('caramel', 'Карамель'), ('maple', 'Кленовый'), ('blueberry', 'Черничный'), ('m_choco', 'Молочный шоколад')], help_text='Шоколадный, ванильный, медовый и т.д', max_length=15, verbose_name='Топпинг'),
        ),
    ]
