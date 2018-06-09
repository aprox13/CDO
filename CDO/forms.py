from django import forms

from CDO.models import *
from CDO.vars import *


class UserLogIn(forms.ModelForm):
    user_login = forms.CharField(max_length=40,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control',
                                            'placeholder': 'Login',
                                            }
                                 ))
    user_password = forms.CharField(max_length=40,
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control',
                                               'placeholder': 'Password',
                                               }
                                    ))

    class Meta:
        model = User
        fields = ['user_login', 'user_password', ]


class UserSignIn(forms.ModelForm):
    user_login = forms.CharField(max_length=40,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control',
                                            'placeholder': 'Логин',
                                            }
                                 ))
    user_password = forms.CharField(max_length=40,
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-control',
                                               'placeholder': 'Пароль',
                                               }
                                    ))

    user_name = forms.CharField(max_length=40,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': 'Имя',
                                           }
                                ))
    user_surname = forms.CharField(max_length=40,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control',
                                              'placeholder': 'Фамилия',
                                              }
                                   ))

    user_permission = forms.IntegerField(widget=forms.RadioSelect(choices=PERMISSIONS))

    class Meta:
        model = User
        fields = ['user_login', 'user_password', 'user_name', 'user_surname', 'user_permission', ]


class OrgForm(forms.ModelForm):
    org_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'on'}))
    org_date = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'od'}))
    org_location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'ol'}))
    org_about = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'oa'}))
    org_dir_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'odn'}))
    org_dir_surname = forms.CharField(max_length=100,
                                      widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'ods'}))
    org_dir_birth = forms.CharField(max_length=100,
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'odb'}))

    def set_to_all_style(self, style):
        for field in self.fields:
            self.fields[field].widget.attrs.update({'style': style})

    def set_read_only(self):
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control-plaintext', 'readonly': 'true'})

    class Meta:
        model = Organisation
        exclude = []
