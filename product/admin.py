from django.contrib import admin
from .models import Estate, PaymentOrder, FeedbackResponse, Feedback, Category, Card, Image, Favourite, City, District, ApartmentSale, ApartmentRent, HouseSale, GarageforSaleOrRent, CommercialProperties


class EstateAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'city', 'created_at', 'is_active')
    list_category = ('category', 'city', 'district')
    search_fields = ('title', 'category', 'city', 'district')

admin.site.register(Category)
admin.site.register(PaymentOrder)
admin.site.register(FeedbackResponse)
admin.site.register(Feedback)
admin.site.register(Card)
admin.site.register(Image)
admin.site.register(Favourite)
admin.site.register(City)
admin.site.register(District)
admin.site.register(Estate, EstateAdmin)
admin.site.register(ApartmentSale)
admin.site.register(ApartmentRent)
admin.site.register(HouseSale)
admin.site.register(GarageforSaleOrRent)
admin.site.register(CommercialProperties)





