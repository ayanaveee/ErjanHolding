from django.db import models
from model_utils.managers import InheritanceManager
from django.contrib.auth import get_user_model

MyUser = get_user_model()

class Card(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=1)
    full_name = models.CharField(max_length=100, verbose_name='Ф.И.О.')
    number = models.PositiveSmallIntegerField(verbose_name='Номер карты')
    cvv = models.PositiveSmallIntegerField(verbose_name='CVV')
    expire_date = models.DateField(verbose_name='Годен до')

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'

    def __str__(self):
        return f"{self.number}"

class City(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

class District(models.Model):
        city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='Город')
        title = models.CharField(max_length=100, verbose_name='Название')

        def __str__(self):
            return self.title

        class Meta:
            verbose_name = 'Район'
            verbose_name_plural = 'Районы'

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    cover = models.ImageField(upload_to='category_covers/', verbose_name='Обложка категории')
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Родительская категория')

    def __str__(self):
        ancestors = []
        category = self
        while category:
            ancestors.append(category.title)
            category = category.parent_category
        return ' > '.join(reversed(ancestors))

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Estate(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    area = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Площадь')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name='Район')
    rooms = models.SmallIntegerField(verbose_name='Количество комнат')
    mail_cover = models.ImageField(upload_to='images/', verbose_name='Обложка', null=True, blank=True)
    geo = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    promo_video = models.FileField(upload_to='videos/', verbose_name='Видеоролик', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    objects = InheritanceManager()
    is_popular = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Недвижимость'
        verbose_name_plural = 'Недвижимости'

    def __str__(self):
        return f"{self.title}"

class ApartmentSale(Estate):
    floor = models.SmallIntegerField(verbose_name='Этаж')
    total_floors = models.IntegerField(verbose_name='Этажей в доме')

    class Meta:
        verbose_name = 'Квартира на продажу'
        verbose_name_plural = 'Квартиры на продажу'

class CommercialProperties(Estate):
    equipment = models.CharField(max_length=100, verbose_name='Оборудование')
    utilities = models.CharField(max_length=100, verbose_name='Коммуникации')

    class Meta:
        verbose_name = 'Коммерческое помещение'
        verbose_name_plural = 'Коммерческие помещения'

class GarageforSaleOrRent(Estate):
    building_material = models.CharField(max_length=100, verbose_name='Материал постройки')

    class Meta:
        verbose_name = 'Гараж'
        verbose_name_plural = 'Гаражи'

class ApartmentRent(Estate):
    rental_period = models.CharField(max_length=20, verbose_name='Срок аренды')

    class Meta:
        verbose_name = 'Квартира в аренду'
        verbose_name_plural = 'Квартиры в аренду'

class HouseSale(Estate):
    plot_size = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Площадь участка')
    floors = models.IntegerField(verbose_name='Количество этажей')
    garage = models.BooleanField(default=False, verbose_name='Гараж')

    class Meta:
        verbose_name = 'Дом на продажу'
        verbose_name_plural = 'Дома на продажу'

class PaymentOrder(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=1)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name='Карта')
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма')

    class Meta:
        verbose_name = 'Платёжное поручение'
        verbose_name_plural = 'Платёжные поручения'

class Feedback(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=1)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, verbose_name='Объект')
    comment = models.TextField(verbose_name='Комментарии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Комментарий от {self.user.username} к {self.estate.title}'

class FeedbackResponse(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=1)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE,related_name='responses', verbose_name='Отзыв')
    comment = models.TextField(verbose_name='Комментарии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Было создано')

    class Meta:
        verbose_name = 'Ответ на обратную связь'
        verbose_name_plural = 'Ответы на обратную связь'

class Favourite(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=1)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, verbose_name='Объект')

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural  = 'Избранные'

    def __str__(self):
        return f'{self.estate.title}'

class Image(models.Model):
    file = models.ImageField(upload_to= 'images/', null=True, blank=True)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    is_main = models.BooleanField()

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
