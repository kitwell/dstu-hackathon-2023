from ckeditor.widgets import CKEditorWidget
from django import forms
from transliterate import translit
from .models import *


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'subtitle', 'content', 'category', 'slug', 'image_preview', 'image1', 'image2', 'image3', 'image4']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def save_model(self, request, obj, form, change):
        slug = slugify(translit(obj.title, 'ru', reversed=True))
        now = datetime.now()
        obj.slug = f'{slug}-{now.strftime("%m-%d")}'
        obj.save()
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


class AddContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('topic', 'message', 'name', 'email')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'text')