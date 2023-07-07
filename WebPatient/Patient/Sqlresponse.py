import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebPatient.settings')
django.setup()

from django.db import connection

def execute_custom_query():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * '
                       'FROM "Patient_patient"'
                       'WHERE id BETWEEN 1 and 5 ')
        results = cursor.fetchall()
        return results

# Вызов функции и вывод результатов в терминале
query_results = execute_custom_query()
for row in query_results:
    print(row)