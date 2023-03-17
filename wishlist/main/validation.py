from typing import Optional

from django.http import HttpResponse


def validate_request(request) -> Optional[HttpResponse]:
    if request.method != 'POST':
        return HttpResponse('Method not allowed', 'text/plain', 400)

    pk = request.POST.get('id')
    if not pk:
        return HttpResponse('id parameter is required', 'text/plain', 400)
    return None
