from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
import json
from .models import StringEntry


# Utility to check palindrome
def is_palindrome(value):
    cleaned = ''.join(ch.lower() for ch in value if ch.isalnum())
    return cleaned == cleaned[::-1]


@csrf_exempt
@require_http_methods(["GET", "POST"])
def string_list_create(request):
    if request.method == "GET":
        strings = StringEntry.objects.all()
        data = [{"value": s.value, "is_palindrome": s.is_palindrome} for s in strings]
        return JsonResponse(data, safe=False, status=200)

    # POST
    try:
        body = json.loads(request.body)
        value = body.get("value", "").strip()
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not value:
        return JsonResponse({"error": "Missing 'value' field"}, status=400)

    if not isinstance(value, str):
        return JsonResponse({"error": "'value' must be a string"}, status=400)

    # Check for duplicate
    if StringEntry.objects.filter(value=value).exists():
        return JsonResponse({"error": "String already exists"}, status=409)

    string_obj = StringEntry.objects.create(value=value, is_palindrome=is_palindrome(value),length=len(value))
    data = {"value": string_obj.value, "is_palindrome": string_obj.is_palindrome}
    return JsonResponse(data, status=201)


@csrf_exempt
@require_http_methods(["GET", "DELETE"])
def string_detail(request, string_value):
    try:
        string_obj = StringEntry.objects.get(value=string_value)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "String not found"}, status=404)

    if request.method == "GET":
        data = {"value": string_obj.value, "is_palindrome": string_obj.is_palindrome}
        return JsonResponse(data, status=200)

    # DELETE
    string_obj.delete()
    return JsonResponse({"message": "String deleted"}, status=200)


@require_http_methods(["GET"])
def filter_by_natural_language(request):
    query = request.GET.get("query", "").lower().strip()
    if not query:
        return JsonResponse({"error": "Missing query parameter"}, status=400)

    strings = StringEntry.objects.all()

    if "palindrome" in query:
        strings = strings.filter(is_palindrome=True)

    if "single word" in query:
        strings = [s for s in strings if " " not in s.value]

    results = [{"value": s.value, "is_palindrome": s.is_palindrome} for s in strings]
    return JsonResponse(results, safe=False, status=200)
