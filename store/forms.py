from django import forms

class PlacingAnOrderForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, label="Сумма", widget=forms.TextInput(attrs={'class': 'form-item__text'}))
    product_name = forms.CharField(max_length=255, label="Название курса", widget=forms.TextInput(attrs={'class': 'form-item__text'}))
    customer_name = forms.CharField(max_length=100, min_length=2, label="Ваше Имя", widget=forms.TextInput(attrs={'class': 'form-item__text'}))
    customer_email = forms.EmailField(label="Эл. почта", widget=forms.TextInput(attrs={'class': 'form-item__text'}))
    customer_phone = forms.CharField(max_length=20, min_length=7, label="Номер телефона", widget=forms.TextInput(attrs={'class': 'form-item__text'}))
    is_accepted = forms.BooleanField(initial=False, label="Согласие на обработку персональных данных", widget=forms.CheckboxInput(attrs={'class': 'form-item__text'}))
