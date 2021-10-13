from django import forms
from django.forms import  ModelForm, ValidationError
from django.contrib import admin
from .models import *
from PIL import Image
class NotebookAdminForm(ModelForm):

    MIN_RES = 4000
    MIN_RES_2 = 4000


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = f'Загрузка изображения с мин. разрешением {self.MIN_RES} x {self.MIN_RES_2}'

    # def clean_image(self):
    #     image = self.cleaned_data['image']
    #     img = Image.open(image)
    #     print(img.width, img.height)
    #     return image
    #     min_height = self.MIN_RES
    #     min_width = self.MIN_RES_2
    #     if img.height < min_height or img.width < min_width or img.height < min_width or img.width < min_height:
    #         raise ValidationError('Слишком низкое разрешение')



class NotebookCategoryChoiceField(forms.ModelChoiceField):

    pass

class NotebookAdmin(admin.ModelAdmin):

    form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == 'category':
            return NotebookCategoryChoiceField(Category.objects.filter(slug= 'notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphonesCategoryChoiceField(forms.ModelChoiceField):
    pass

class SmartphonesAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == 'category':
            return SmartphonesCategoryChoiceField(Category.objects.filter(slug= 'smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphonesAdmin)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(CartProduct)



