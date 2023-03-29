from django import forms
from .models import Record
from django.forms.widgets import NumberInput
class RecordForm(forms.ModelForm):
    EXERCISE = [
            ('스쿼트','스쿼트'),
            ('푸쉬업','푸쉬업'),
            ('런지','런지'),
    ]
    exercise = forms.ChoiceField(choices=EXERCISE, widget=forms.Select())
    date = forms.DateTimeField(widget=NumberInput(attrs={'type': 'date'}), label="날짜")
    class Meta:
        model = Record
        # fields = ['excercise','count','time','date','perfect','good','bad']
        exclude = ('user',)

        # widgets = {
        #     "exercise" : forms.CharField(widget=
        #         attrs = {
        #             "class" : "form-control mt-2"
        #         }    
        #     ),
        #     "count" : forms.IntegerField(attrs={"class":"form-control mt-2"}),
        #     "time" : forms.IntegerField(attrs={"class":"form-control mt-2"}),
        #     "good" : forms.IntegerField(attrs={"class":"form-control mt-2"}),
        #     "bad" : forms.IntegerField(attrs={"class":"form-control mt-2"}),
        #     "date" : forms.DateField(attrs={"class":"form-control mt-2"}),
        # }