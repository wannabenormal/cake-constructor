from django.db import migrations, models


def create_objs(apps, schema_editor):
    Berry = apps.get_model('cakeshop', 'Berry')
    Topping = apps.get_model('cakeshop', 'Topping')
    Shape = apps.get_model('cakeshop', 'Shape')
    Decoration = apps.get_model('cakeshop', 'Decoration')
    Height = apps.get_model('cakeshop', 'Height')

    Height.objects.bulk_create([
        Height(height="Один", height_codename="one", price=400),
        Height(height="Два", height_codename="two", price=750),
        Height(height="Три", height_codename="three", price=1100),
    ])

    Berry.objects.bulk_create([
        Berry(berry="Без ягод", berry_codename="without", price=0),
        Berry(berry="Ежевика", berry_codename="bramble", price=400),
        Berry(berry="Малина", berry_codename="rasp", price=300),
        Berry(berry="Голубика", berry_codename="blue", price=450),
        Berry(berry="Клубника", berry_codename="straw", price=500),
    ])

    Topping.objects.bulk_create([
        Topping(topping="Без топпинга", topping_codename="without", price=0),
        Topping(topping="Белый соус", topping_codename="white_sauce", price=200),
        Topping(topping="Карамельный", topping_codename="caramel", price=180),
        Topping(topping="Кленовый", topping_codename="maple", price=200),
        Topping(topping="Черничный", topping_codename="blueberry", price=300),
        Topping(topping="Молочный шоколад", topping_codename="white_choco", price=350),
    ])

    Decoration.objects.bulk_create([
        Decoration(decoration="Без декора", decoration_codename="without", price=0),
        Decoration(decoration="Фисташки", decoration_codename="pistachio", price=300),
        Decoration(decoration="Безе", decoration_codename="bese", price=400),
        Decoration(decoration="Фундук", decoration_codename="hazelnut", price=350),
        Decoration(decoration="Пекан", decoration_codename="pecan", price=300),
        Decoration(decoration="Маршмеллоу", decoration_codename="marsh", price=200),
        Decoration(decoration="Марципан", decoration_codename="marzipan", price=280),
    ])

    Shape.objects.bulk_create([
        Shape(shape="Круг", shape_codename="c", price=600),
        Shape(shape="Квадрат", shape_codename="s", price=400),
        Shape(shape="Прямоугольник", shape_codename="r", price=1000),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('cakeshop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_objs),
    ]
