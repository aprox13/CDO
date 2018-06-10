from django.shortcuts import render, redirect, render_to_response

from CDO.forms import *
from CDO.support import *
from CDO.models import *
from django.core.exceptions import ObjectDoesNotExist
from CDO.Alert import *


def put_alert_to_session(request, type, title, message):
    write(request, ALERT_TOKEN, True)
    write(request, ALERT_TYPE, type)
    write(request, ALERT_TITLE, title)
    write(request, ALERT_MESSAGE, message)


def get_alert(request):
    if contain(request, ALERT_TOKEN):
        write(request, ALERT_TOKEN, None)
        return Alert(get(request, ALERT_TYPE), get(request, ALERT_TITLE), get(request, ALERT_MESSAGE))
    return None


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

    alert = get_alert(request)
    print(alert)
    return render(request, 'main.html',
                  {
                      'usr_name': get(request, USER_NAME),
                      'perm': get(request, USER_PERMISSION),
                      'organisations': Organisation.objects.all(),
                      Alert.ALERT_TAG: alert
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

    return render(request, 'users.html', {'form': UserSignIn({USER_PASSWORD: string_generator(8)})})


def about(request):
    print('about page')
    perm = get(request, USER_PERMISSION)
    if request.method == 'POST' and EDIT_TOKEN in request.POST and perm != PERM_GUEST: # Post to edit
        print('POST: ' + str(request.POST))
        id = int(request.POST['edit_id_token'])
        form = OrgForm(request.POST)
        token = int(request.POST[EDIT_TOKEN])
        if token == TOKEN_SAVE:  # Save request
            print('Token save')
            if form.is_valid():
                print('form is valid')
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

                    form1 = OrgForm(initial=org.get_initial())
                    form1.set_read_only()

                    form1.set_to_all_style('margin-left: 40px;')
                    put_alert_to_session(request, Alert.TYPE_SUCCESS, 'Успешно',
                                         'Информация о компании ' + org.org_name + ' успешно обновлена')
                    return redirect('/about?id=' + str(id))
                except ObjectDoesNotExist:
                    print('wtf. wrong post id')
        elif token == TOKEN_DELETE:  # Delete request
            
            print('token remove')
            org = Organisation.objects.get(org_id=id)
            put_alert_to_session(request, Alert.TYPE_DANGER, 'Успешно',
                                 'Информация о компании ' + org.org_name + ' успешно удалена')
            org.delete()
            return redirect('main_page')

    if request.method == 'GET' and 'id' in request.GET:  # Get by id request
        try:
            org = Organisation.objects.get(org_id=request.GET['id'])
            edit = True
            id = org.org_id
            form = OrgForm(initial=org.get_initial())

            if 'edit' not in request.GET or request.GET['edit'] != '1':
                form.set_read_only()
                edit = False

            if perm == PERM_GUEST:
                form.set_read_only()
                edit = False

            form.set_to_all_style('margin-left: 40px;')

            alert = get_alert(request)

            print(alert)

            return render(request, 'about.html', {
                'PAGE_TITLE': org.org_name,
                'form': form,
                'edit': edit,
                'id': id,
                'perm': perm,
                Alert.ALERT_TAG: alert
            })
        except ObjectDoesNotExist:
            return render(request, 'about.html', {
                'PAGE_TITLE': '404 not found', 'perm': perm
            })

    return redirect('root')


def redirect_support(request):
    return render(request, 'main.html')


def add(request):
    if request.method == 'POST':
        form = OrgForm(request.POST)
        if form.is_valid():
            form.save()
            put_alert_to_session(request, Alert.TYPE_SUCCESS, 'Успешно',
                                 'Организация ' + form.cleaned_data['org_name'] + ' успешно добавлена')
            return redirect('main_page')

    form = OrgForm()
    form.set_to_all_style('margin-left: 40px;')
    return render(request, 'add.html', {'form': form})
