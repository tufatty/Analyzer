from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import StringEntry
from .serializers import StringEntrySerializer

# Utility function to analyze the string
def analyze_string(value):
    length = len(value)
    is_palindrome = value.lower() == value[::-1].lower()
    is_natural = value.isalpha()
    vowels = sum(1 for ch in value.lower() if ch in "aeiou")
    consonants = sum(1 for ch in value.lower() if ch.isalpha() and ch not in "aeiou")

    return {
        "value": value,
        "length": length,
        "is_palindrome": is_palindrome,
        "is_natural": is_natural,
        "vowels": vowels,
        "consonants": consonants,
    }

# POST /api/strings
class StringListCreateView(APIView):
    def post(self, request):
        value = request.data.get("value")
        if not value:
            return Response(
                {"error": "Missing 'value' field."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check for duplicates
        if StringEntry.objects.filter(value=value).exists():
            return Response(
                {"error": "String already exists."},
                status=status.HTTP_409_CONFLICT,
            )

        data = analyze_string(value)
        serializer = StringEntrySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Optional query params: ?is_palindrome=true&min_length=3
        queryset = StringEntry.objects.all()

        is_palindrome = request.GET.get("is_palindrome")
        if is_palindrome:
            queryset = queryset.filter(is_palindrome=is_palindrome.lower() == "true")

        is_natural = request.GET.get("is_natural")
        if is_natural:
            queryset = queryset.filter(is_natural=is_natural.lower() == "true")

        min_length = request.GET.get("min_length")
        if min_length:
            queryset = queryset.filter(length__gte=int(min_length))

        serializer = StringEntrySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# GET /api/strings/<string_value>  and DELETE /api/strings/<string_value>
class StringDetailView(APIView):
    def get(self, request, string_value):
        try:
            entry = StringEntry.objects.get(value=string_value)
        except StringEntry.DoesNotExist:
            return Response(
                {"error": "String not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = StringEntrySerializer(entry)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, string_value):
        try:
            entry = StringEntry.objects.get(value=string_value)
        except StringEntry.DoesNotExist:
            return Response(
                {"error": "String not found."}, status=status.HTTP_404_NOT_FOUND
            )

        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
