from rest_framework.views import exception_handler
from rest_framework.exceptions import Throttled
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Chama o handler padrão do DRF primeiro para obter a resposta padrão
    response = exception_handler(exc, context)

    # Se for uma exceção de Throttling, personalizamos a mensagem
    if isinstance(exc, Throttled):
        wait_seconds = getattr(exc, 'wait', 0)
        custom_data = {
            'detail': f"Limite de requisições excedido. Tente novamente em {int(wait_seconds)} segundos.",
            'aguarde_segundos': int(wait_seconds)
        }
        return Response(custom_data, status=status.HTTP_429_TOO_MANY_REQUESTS)

    return response
