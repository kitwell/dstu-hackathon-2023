from datetime import datetime
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.core.files import File
from .models import *
from transliterate import translit




admin.site.register(Category)
admin.site.register(Contact)


@admin.register(Articles)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        slug = slugify(translit(obj.title, 'ru', reversed=True))
        now = datetime.now()
        obj.slug = f'{slug}-{now.strftime("%m-%d")}'
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(obj.slug)
        qr.make(fit=True)
        qrcode_image = qr.make_image()
        qrcode_path = f'media/{obj.slug}.png'
        qrcode_image.save(qrcode_path)

        # Attach QRCode to article
        obj.qr_code.save(f'{obj.slug}.png', File(open(qrcode_path, 'rb')))


admin.site.register(Review)
admin.site.register(Comment)