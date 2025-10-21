import hashlib
import json
from django.http import JsonResponse
from django.views import View
from .models import StringEntry
from .utils import analyze_string



class StringListView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            value = data.get('value')
            if not isinstance(value, str):
                return JsonResponse({'error': 'Invalid data type for "value"'}, status=422)

            sha256_hash = hashlib.sha256(value.encode()).hexdigest()

            if StringEntry.objects.filter(id=sha256_hash).exists():
                return JsonResponse({'error': 'String already exists'}, status=409)

            properties = analyze_string(value)
            entry = StringEntry.objects.create(id=sha256_hash, value=value, properties=properties)

            return JsonResponse({
                'id': entry.id,
                'value': entry.value,
                'properties': entry.properties,
                'created_at': entry.created_at.isoformat()
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    def get(self, request):
        params = request.GET
        queryset = StringEntry.objects.all()

        # Filtering logic
        if 'is_palindrome' in params:
            val = params['is_palindrome'].lower() == 'true'
            queryset = queryset.filter(properties__is_palindrome=val)

        if 'min_length' in params:
            queryset = [x for x in queryset if x.properties['length'] >= int(params['min_length'])]

        if 'max_length' in params:
            queryset = [x for x in queryset if x.properties['length'] <= int(params['max_length'])]

        if 'word_count' in params:
            queryset = [x for x in queryset if x.properties['word_count'] == int(params['word_count'])]

        if 'contains_character' in params:
            char = params['contains_character']
            queryset = [x for x in queryset if char in x.value]

        data = [{
            'id': x.id,
            'value': x.value,
            'properties': x.properties,
            'created_at': x.created_at.isoformat()
        } for x in queryset]

        return JsonResponse({
            'data': data,
            'count': len(data),
            'filters_applied': params.dict()
        })

class StringDetailView(View):
    def get(self, request, string_value):
        try:
            entry = StringEntry.objects.get(value=string_value)
            return JsonResponse({
                'id': entry.id,
                'value': entry.value,
                'properties': entry.properties,
                'created_at': entry.created_at.isoformat()
            })
        except StringEntry.DoesNotExist:
            return JsonResponse({'error': 'String not found'}, status=404)

    def delete(self, request, string_value):
        try:
            entry = StringEntry.objects.get(value=string_value)
            entry.delete()
            return JsonResponse({}, status=204)
        except StringEntry.DoesNotExist:
            return JsonResponse({'error': 'String not found'}, status=404)

# ========================
# NATURAL LANGUAGE FILTER
# ========================
class NaturalLanguageFilterView(View):
    def get(self, request):
        query = request.GET.get('query', '').lower()
        filters = {}

        if 'palindromic' in query:
            filters['is_palindrome'] = True
        if 'single word' in query:
            filters['word_count'] = 1
        if 'longer than' in query:
            parts = query.split('longer than')
            try:
                filters['min_length'] = int(parts[1].split()[0]) + 1
            except:
                pass
        if 'containing the letter' in query:
            filters['contains_character'] = query.split('containing the letter')[-1].strip()[0]

        if not filters:
            return JsonResponse({'error': 'Unable to parse natural language query'}, status=400)

        # Apply filters
        queryset = StringEntry.objects.all()
        if 'is_palindrome' in filters:
            queryset = queryset.filter(properties__is_palindrome=True)
        if 'word_count' in filters:
            queryset = [x for x in queryset if x.properties['word_count'] == filters['word_count']]
        if 'min_length' in filters:
            queryset = [x for x in queryset if x.properties['length'] >= filters['min_length']]
        if 'contains_character' in filters:
            char = filters['contains_character']
            queryset = [x for x in queryset if char in x.value]

        data = [{
            'id': x.id,
            'value': x.value,
            'properties': x.properties,
            'created_at': x.created_at.isoformat()
        } for x in queryset]

        return JsonResponse({
            'data': data,
            'count': len(data),
            'interpreted_query': {
                'original': query,
                'parsed_filters': filters
            }
        })