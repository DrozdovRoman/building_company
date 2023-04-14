from django.views import View
from django.shortcuts import render
from django.db import ProgrammingError
from django.db import connection
from django.http import Http404


def index(request):
    return render(request, "index.html")


def entity(request):
    return render(request, "entities.html")


class EntityView(View):
    table_name = None
    table_alias = None

    def get_table_name(self):
        assert self.table_name is not None, (
            "'%s' should either include a `table_name` attribute, "
            "or override the `get_table_name()` method."
            % self.__class__.__name__
        )
        table_name = self.table_name
        if isinstance(table_name, str):
            return table_name
        raise TypeError

    def get_table_alias(self):
        assert self.table_alias is not None, (
            "'%s' should either include a `table_alias` attribute, "
            "or override the `get_table_alias()` method."
            % self.__class__.__name__
        )
        table_alias = self.table_alias
        if isinstance(table_alias, str):
            return table_alias
        raise TypeError

    def __init__(self, **kwargs):
        self.get_table_name()
        self.get_table_alias()
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        try:
            with connection.cursor() as cursor:
                data = f'SELECT * FROM {self.table_name}'

                column_name = f'''SELECT column_name
                \nFROM information_schema.columns
                \nWHERE table_name = '{self.table_name}' '''

                cursor.execute(column_name)
                columns = cursor.fetchall()

                cursor.execute(data)
                rows = cursor.fetchall()
        except ProgrammingError:
            raise Http404
        finally:
            cursor.close()
        return render(request,
                      'entity.html',
                      {'columns': columns,
                       'rows': rows,
                       'table_name': self.table_alias})


class EquipmentTypeView(EntityView):
    table_name = 'equipment_type'
    table_alias = 'Тип техники'


# def equipment_type(request):
#     try:
#         with connection.cursor() as cursor:
#             data = 'SELECT * FROM equipment_type'

#             column_name = '''SELECT column_name
#             \nFROM information_schema.columns
#             \nWHERE table_name = 'equipment_type' '''

#             cursor.execute(column_name)
#             columns = cursor.fetchall()
#             print(column_name)

#             cursor.execute(data)
#             rows = cursor.fetchall()
#             print(data)
#     finally:
#         cursor.close()

#     return render(
#         request,
#         'entity.html',
#         {'columns': columns, 'rows': rows})
