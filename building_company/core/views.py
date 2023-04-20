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
    column_name = None
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

    def get_column_name(self):
        assert self.column_name is not None, (
            "'%s' should either include a `table_name` attribute, "
            "or override the `get_table_name()` method."
            % self.__class__.__name__
        )
        column_name = self.column_name
        if isinstance(column_name, tuple):
            return column_name
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
        self.get_column_name()
        self.get_table_alias()
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        try:
            with connection.cursor() as cursor:
                data = f'SELECT * FROM {self.table_name}'
                cursor.execute(data)
                rows = cursor.fetchall()
        except ProgrammingError:
            raise Http404
        finally:
            cursor.close()
        return render(request,
                      'entity.html',
                      {'columns': self.column_name,
                       'rows': rows,
                       'table_name': self.table_alias})


class EquipmentTypeView(EntityView):
    table_name = 'equipment_type'
    table_alias = 'Тип техники'
    column_name = ('Название техники', )


class EquipmentConstructionTypeView(EntityView):
    table_name = 'equipment_construction'
    table_alias = 'Техника строительного управления'
    column_name = (
        'Тип техники', 'Номер строительного управления',
        'Количество (ед.)')


class SpecializationView(EntityView):
    table_name = 'specialization'
    table_alias = 'Специальность'
    column_name = ('Название специальности', )


class EngineeringPositionView(EntityView):
    table_name = 'engineering_position'
    table_alias = 'Тип инженерно-технической должности'
    column_name = ('Название должности', )


class ObjectTypeView(EntityView):
    table_name = 'object_type'
    table_alias = 'Тип объекта'
    column_name = ('Название типа объекта', )


class CustomerView(EntityView):
    table_name = 'customer'
    table_alias = 'Заказчик'
    column_name = (
        'Название компании', 'ОГРН', 'ИНН',
        'Адрес', 'Руководитель компании')


class EmployeeView(EntityView):
    table_name = 'employee'
    table_alias = 'Персонал'
    column_name = (
        'ID', 'Имя', 'Фамилия',
        'Дата рождения', 'Электронная почта',
        'Номер телефона', 'Специальность', 'Техническая должность')


class ConstructionView(EntityView):
    table_name = 'construction'
    table_alias = 'Строительное управление'
    column_name = (
        'Номер управления', 'ID директора'
    )


class RegionView(EntityView):
    table_name = 'region'
    table_alias = 'Участок'
    column_name = (
        'Кадастровый номер', 'Номер управления', 'ID Начальника участка',
        'Площадь (кв.м)',)


class BrigadeView(EntityView):
    table_name = 'brigade'
    table_alias = 'Бригада'
    column_name = (
        'Номер бригады', 'ID бригадира',)


class BrigadeEmployeeView(EntityView):
    table_name = 'brigade_employee'
    table_alias = 'Персонал бригады'
    column_name = (
        'ID работника бригады', 'Номер бригады', )


class BuildingView(EntityView):
    table_name = 'building'
    table_alias = 'Строительный объект'
    column_name = (
        'Номер строительного объекта', 'Тип объекта',
        'Кадастровый номер участка'
    )
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
