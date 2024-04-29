# Importing VernamCipher from encryption module
from .encryption import VernamCipher
# Importing render function from django.shortcuts module
from django.shortcuts import render
# Importing models from current package
from .models import Department, Region, MessageDepartment, MessageRegion
# Importing login_required decorator from django.contrib.auth.decorators module
from django.contrib.auth.decorators import login_required

@login_required
def chat(request):
    return render(request, 'chat/chat.html')  # Rendering chat.html template


@login_required
def departments(request):
    # Retrieving all departments from the database
    departments = Department.objects.raw('SELECT * FROM chat_Department')

    # Rendering departments.html template with departments data
    return render(request, 'chat/departments.html', {'departments': departments})


@login_required
def regions(request):
    # Retrieving all regions from the database
    regions = Region.objects.raw('SELECT * FROM chat_Region')

    # Rendering regions.html template with regions data
    return render(request, 'chat/regions.html', {'regions': regions})


@login_required
def department_message(request, slug):
    department = list(Department.objects.raw(
        # Retrieving department with matching slug from the database
        'SELECT * FROM chat_Department WHERE slug = %s', [slug]))[0]
    messages = list(MessageDepartment.objects.raw(
        # Retrieving latest 25 messages for the department
        'SELECT * FROM chat_MessageDepartment WHERE department_id = %s ORDER BY id DESC LIMIT 25', [department.id]))
    for message in messages:
        # Decrypting the content of each message
        message.content = VernamCipher.decrypt(message.content, message.key)

    # Reversing the list of messages
    messages = messages[::-1]

    # Rendering department_messages.html template with department and messages data
    return render(request, 'chat/department_messages.html', {'department': department, 'messages': messages})


@login_required
def regions_message(request, slug):
    region = list(Department.objects.raw(
        # Retrieving region with matching slug from the database
        'SELECT * FROM chat_Region WHERE slug = %s', [slug]))[0]
    messages = list(MessageRegion.objects.raw(
        # Retrieving latest 25 messages for the region
        'SELECT * FROM chat_MessageRegion WHERE region_id = %s ORDER BY id DESC LIMIT 25', [region.id]))
    for message in messages:
        # Decrypting the content of each message
        message.content = VernamCipher.decrypt(message.content, message.key)

    # Reversing the list of messages
    messages = messages[::-1]

    # Rendering region_messages.html template with region and messages data
    return render(request, 'chat/region_messages.html', {'region': region, 'messages': messages})
