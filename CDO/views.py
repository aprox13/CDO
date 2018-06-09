from django.shortcuts import render, redirect

from CDO.forms import *
from CDO.support import *
from CDO.models import *
from django.core.exceptions import ObjectDoesNotExist


def write_user(request, usr):
    write(request, USER_ID, usr.user_id)
    write(request, USER_NAME, usr.user_name)
    write(request, USER_PERMISSION, usr.user_permission)


def remove_active_user(request):
    remove(request, USER_NAME)
    remove(request, USER_PERMISSION)
    remove(request, USER_ID)


def is_unknown_user(request):
    return not contain(request, USER_ID)


def empty(request):
    print("empty")

    # remove_active_user(request)
    if request.method == 'POST':
        form = UserLogIn(request.POST)
        if form.is_valid():

            login = form.cleaned_data[USER_LOGIN]
            password = form.cleaned_data[USER_PASSWORD]
            try:
                usr = User.objects.get(user_login=login, user_password=password)
                write_user(request, usr)
                return redirect('main_page')
            except ObjectDoesNotExist:
                remove_active_user(request)
                pass

    if contain(request, USER_ID):
        return redirect('main_page')

    return render(request, 'start.html', {'form': UserLogIn})


def main_page(request):
    # print("main")
    if is_unknown_user(request):
        return redirect("root")
    # print(request.POST)
    if request.method == 'POST' and 'logout' in request.POST:
        remove_active_user(request)
        return redirect("root")

    return render(request, 'main.html',
                  {
                      'usr_name': get(request, USER_NAME),
                      'perm': get(request, USER_PERMISSION),
                      'organisations': Organisation.objects.all()
                  }
                  )


def users_editor(request):
    if is_unknown_user(request) or get(request, USER_PERMISSION) != PERM_ADMIN:
        return redirect("root")
    if request.method == 'POST' and 'logout' in request.POST:
        remove_active_user(request)
        return redirect("root")
    if request.method == 'POST':
        form = UserSignIn(request.POST)
        if form.is_valid():
            login = form.cleaned_data['user_login']
            print('login ' + login)
            try:
                u = User.objects.get(user_login=login)
                print('User with id ' + str(u.user_id))
                return render(request, 'users.html', {
                    'form': UserSignIn({USER_PASSWORD: string_generator(8)}),
                    'alert_class': 'alert-danger',
                    'add_title': "Ошибка!",
                    'add_message': "Пользователь с логином " + login + " уже существует."
                })

            except ObjectDoesNotExist:
                form.save()
                return render(request, 'users.html', {
                    'form': UserSignIn({USER_PASSWORD: string_generator(8)}),
                    'alert_class': 'alert-success',
                    'add_title': 'Успешно!',
                    'add_message': 'Пользователь ' + form.cleaned_data[
                        'user_name'] + ' успешно добавлен.'
                })
                pass

    return render(request, 'users.html', {'form': UserSignIn({USER_PASSWORD: string_generator(8)})})


def about(request):
    if request.method == 'GET' and 'id' in request.GET:
        try:
            org = Organisation.objects.get(org_id=request.GET['id'])
            edit = True
            id = org.org_id
            form = OrgForm(initial={
                'org_name': org.org_name,
                'org_about': org.org_about,
                'org_date': org.org_date,
                'org_location': org.org_location,
                'org_dir_name': org.org_dir_name,
                'org_dir_surname': org.org_dir_surname,
                'org_dir_birth': org.org_dir_birth,
            })

            if 'edit' not in request.GET or request.GET['edit'] != '1':
                form.set_read_only()
                edit = False

            form.set_to_all_style('margin-left: 40px;')

            return render(request, 'about.html', {
                'PAGE_TITLE': org.org_name,
                'form': form,
                'edit': edit,
                'id': id
            })
        except ObjectDoesNotExist:
            return render(request, 'about.html', {
                'PAGE_TITLE': '404 not found'
            })

    if request.method == 'POST' and 'edit_token' in request.POST and request.POST['edit_token'] == '1':
        id = int(request.POST['edit_id_token'])
        print('edit by id ' + str(id))
        form = OrgForm(request.POST)
        if form.is_valid():
            try:
                org = Organisation.objects.get(org_id=id)
                org.org_name = form.cleaned_data['org_name']
                org.org_dir_birth = form.cleaned_data['org_dir_birth']
                org.org_dir_surname = form.cleaned_data['org_dir_surname']
                org.org_location = form.cleaned_data['org_location']
                org.org_date = form.cleaned_data['org_date']
                org.org_about = form.cleaned_data['org_about']
                org.org_dir_name = form.cleaned_data['org_dir_name']
                org.save()

                form1 = OrgForm(initial={
                    'org_name': org.org_name,
                    'org_about': org.org_about,
                    'org_date': org.org_date,
                    'org_location': org.org_location,
                    'org_dir_name': org.org_dir_name,
                    'org_dir_surname': org.org_dir_surname,
                    'org_dir_birth': org.org_dir_birth,
                })
                form1.set_read_only()
                edit = False

                form1.set_to_all_style('margin-left: 40px;')

                return redirect('/about?id=' + str(id))

            except ObjectDoesNotExist:
                print('wtf')

    return redirect('root')
