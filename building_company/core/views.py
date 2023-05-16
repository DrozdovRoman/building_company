from django.views import View
from django.shortcuts import render
from django.db import ProgrammingError
from django.db import connection
from django.http import Http404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm


def execute_raw_sql(query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
    except ProgrammingError:
        rows = None
    finally:
        cursor.close()
        return rows


def table_exist(table_name: str, pk_name: str, id, is_string: bool) -> bool:
    if is_string:
        query = f'''
        SELECT COUNT(*)
        FROM {table_name}
        WHERE {pk_name} = '{id}'
        '''
    else:
        query = f'''
        SELECT COUNT(*)
        FROM {table_name}
        WHERE {pk_name} = {id}
        '''
    if execute_raw_sql(query)[0][0] == 0:
        return False
    else:
        return True


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"


def index(request):
    return render(request, "index.html")


def entities(request):
    return render(request, "entities.html")


def tasks(request):
    return render(request, "tasks.html")


def task1(request):
    table_name = 'Задание 1'
    table1_rows = execute_raw_sql(
        '''
    SELECT construction.id, string_agg(first_name || ' ' || last_name, '')
    as director_names
    FROM construction
    INNER JOIN employee ON construction.director = employee.id
    GROUP BY construction.id;''')

    table2_rows = execute_raw_sql(
        '''
    SELECT region.cadastral_number,
    string_agg(first_name || ' ' || last_name, '') as chief_names
    FROM region
    INNER JOIN employee ON region.chief = employee.id
    GROUP BY region.cadastral_number;''')

    table1_columns = (
        'Номер строительного управления',
        'ФИО Руководителя'
    )
    table2_columns = (
        'Кадастровый номер участка',
        'ФИО Руководителя'
    )
    return render(request,
                  'task/task1.html',
                  {'table_name': table_name,
                   'table1_columns': table1_columns,
                   'table2_columns': table2_columns,
                   'table1_rows': table1_rows,
                   'table2_rows': table2_rows})


def task2(request):
    table_name = 'Задание 2'
    return render(request,
                  'task/task2.html',
                  {'table_name': table_name})


def task2_result(request):
    region = request.GET.get('region')
    construction = request.GET.get('construction')
    if region is not None:
        table_name = "Участок"
        if not table_exist(table_name='region', pk_name='cadastral_number',
                           id=region, is_string=True):
            raise Http404('Участка с данным номером не существует')

        table_columns = (
            'Руководитель',
            'Должность'
        )

        table_rows = execute_raw_sql(f'''
        SELECT string_agg(first_name || ' ' || last_name, '') as chief_names,
        employee.engineering_position_name
        FROM employee
        INNER JOIN region ON region.chief = employee.id
        WHERE cadastral_number = '{region}'
        GROUP BY engineering_position_name
        ''')

    if construction is not None:
        table_name = "Строительное управление"
        if not table_exist(table_name='construction', pk_name='id',
                           id=construction, is_string=False):
            raise Http404('Участка с данным номером не существует')

        table_columns = (
            'Руководитель',
            'Должность'
        )

        table_rows = execute_raw_sql(f'''
        SELECT string_agg(first_name || ' ' || last_name, '') as chief_names,
        region.chief AS comparison_field
        FROM employee
        JOIN region ON region.chief = employee.id
        WHERE region.construction_id = {construction}
        GROUP BY region.chief
        UNION
        SELECT string_agg(first_name || ' ' || last_name, '')
        as director_names,
        construction.director AS comparison_field
        FROM employee
        JOIN construction ON construction.director = employee.id
        WHERE construction.id = {construction}
        GROUP BY construction.director;
        ''')

    return render(request,
                  'task/result.html',
                  {'table_name': table_name,
                   'table_columns': table_columns,
                   'table_rows': table_rows})


def task3(request):
    table_name = 'Задание 3'
    return render(request,
                  'task/task3.html',
                  {'table_name': table_name})


def task3_result(request):
    region = request.GET.get('region')
    construction = request.GET.get('construction')
    if region is not None:
        table_name = "Участок"
        if not table_exist(table_name='region', pk_name='cadastral_number',
                           id=region, is_string=True):
            raise Http404('Участка с данным номером не существует')

        table_columns = (
            'Строительный объект',
            'Название технологии',
            'Номер бригады',
            'Дата начала',
            'Дата окончания',
            'Факт начало',
            'Факт конец',
        )

        table_rows = execute_raw_sql(f'''
        SELECT timetable.building_id, object_technology.technology_id,
        timetable.brigade_id, timetable.date_technology_start,
        timetable.date_technology_end, timetable.date_technology_fact_start,
        timetable.date_technology_fact_end
        FROM region
        INNER JOIN building ON region.cadastral_number = building.region_id
        INNER JOIN timetable ON building.id = timetable.building_id
        INNER JOIN object_technology ON
        object_technology.id = timetable.object_technology_id
        WHERE cadastral_number = '{region}'
        ORDER BY timetable.building_id, timetable.date_technology_start
        ''')

    if construction is not None:
        table_name = "Строительное управление"
        if not table_exist(table_name='construction', pk_name='id',
                           id=construction, is_string=False):
            raise Http404('Участка с данным номером не существует')

        table_columns = (
            'Строительный объект',
            'Название технологии',
            'Номер бригады',
            'Дата начала',
            'Дата окончания',
            'Факт начало',
            'Факт конец',
        )

        table_rows = execute_raw_sql(f'''
        SELECT timetable.building_id, object_technology.technology_id,
        timetable.brigade_id, timetable.date_technology_start,
        timetable.date_technology_end, timetable.date_technology_fact_start,
        timetable.date_technology_fact_end
        FROM construction
        INNER JOIN region ON construction.id = region.construction_id
        INNER JOIN building ON region.cadastral_number = building.region_id
        INNER JOIN timetable ON building.id = timetable.building_id
        INNER JOIN object_technology ON
        object_technology.id = timetable.object_technology_id
        WHERE construction.id = {construction}
        ORDER BY timetable.building_id, timetable.date_technology_start
        ''')

    return render(request,
                  'task/result.html',
                  {'table_name': table_name,
                   'table_columns': table_columns,
                   'table_rows': table_rows})


def task4(request):
    table_name = 'Задание 4'
    return render(request,
                  'task/task4.html',
                  {'table_name': table_name})


def task4_result(request):
    building = request.GET.get('building')

    if building is not None:
        table_name = "Строительный объект"
        if not table_exist(table_name='building', pk_name='id',
                           id=building, is_string=False):
            raise Http404('Участка с данным номером не существует')

        table_columns = (
            'Номер бригады',
            'Имя',
            'Фамилия',
            'Должность',
            'Начальник бригады',
        )

        table_rows = execute_raw_sql(f'''
        SELECT brigade_id, first_name,
        last_name, specialization_name, brigade_chief
        FROM (
        SELECT brigade_employee.brigade_id,
        employee.first_name, employee.last_name,
        employee.specialization_name, '-'::text as brigade_chief
        FROM timetable
        INNER JOIN brigade ON timetable.brigade_id = brigade.id
        INNER JOIN brigade_employee ON brigade.id = brigade_employee.brigade_id
        INNER JOIN employee ON brigade_employee.employee_id = employee.id
        WHERE timetable.building_id = {building}
        GROUP BY brigade_employee.brigade_id, employee.first_name,
        employee.last_name, employee.specialization_name
        UNION
        SELECT brigade.id, employee.first_name, employee.last_name,
        employee.specialization_name, '+'::text as brigade_chief
        FROM timetable
        INNER JOIN brigade ON timetable.brigade_id = brigade.id
        INNER JOIN employee ON brigade.supervisor = employee.id
        WHERE timetable.building_id = {building}
        GROUP BY brigade.id, employee.first_name,
        employee.last_name, employee.specialization_name
        ) AS result
        ORDER BY brigade_id, first_name;
        ''')

    return render(request,
                  'task/result.html',
                  {'table_name': table_name,
                   'table_columns': table_columns,
                   'table_rows': table_rows})


def task5(request):
    table_name = 'Задание 5'
    return render(request,
                  'task/task5.html',
                  {'table_name': table_name})


def task5_result(request):
    construction = request.GET.get('construction')

    if construction is not None:
        table_name = "Строительное управление"
        if not table_exist(table_name='construction', pk_name='id',
                           id=construction, is_string=False):
            raise Http404('Участка с данным номером не существует')

        table_columns = (
            'Тип техники',
            'Количество ',
        )

        table_rows = execute_raw_sql(f'''
        SELECT equipment_type_id, count
        FROM equipment_construction
        WHERE construction_id = {construction}
        ORDER BY equipment_type_id
        ''')

    return render(request,
                  'task/result.html',
                  {'table_name': table_name,
                   'table_columns': table_columns,
                   'table_rows': table_rows})


def task6(request):
    table_name = 'Задание 6'
    return render(request,
                  'task/task6.html',
                  {'table_name': table_name})


def task6_result(request):
    building = request.GET.get('building')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if building is not None:
        table_name = "Строительный объект"
        if not table_exist(table_name='building', pk_name='id',
                           id=building, is_string=False):
            raise Http404('Участка с данным номером не существует')

        table_columns = (
            'Тип техники',
            'Количество ',
            'Дата начала работ',
            'Дата окончания работ'
        )

        table_rows = execute_raw_sql(f'''
        SELECT equipment_type_id, count,
        sign_date, commissioning_date
        FROM equipment_building
        WHERE building_id = {building} AND
        sign_date >= '{start_date}' AND
        commissioning_date <= '{end_date}'
        ''')

    return render(request,
                  'task/result.html',
                  {'table_name': table_name,
                   'table_columns': table_columns,
                   'table_rows': table_rows})


def task7(request):
    table_name = 'Задание 7'
    return render(request,
                  'task/task7.html',
                  {'table_name': table_name})


def task7_result(request):
    building = request.GET.get('building')

    if building is not None:
        table_name = "Строительный объект"
        if not table_exist(table_name='building', pk_name='id',
                           id=building, is_string=False):
            raise Http404('Участка с данным номером не существует')

        table1_columns = (
            'Технология',
            'Номер бригады',
            'Дата начала',
            'Дата окончания',
        )

        table1_rows = execute_raw_sql(f'''
        SELECT object_technology.technology_id, timetable.brigade_id,
        timetable.date_technology_start, timetable.date_technology_end
        FROM timetable
        INNER JOIN object_technology ON
        timetable.object_technology_id = object_technology.id
        WHERE timetable.building_id = {building}
        ''')

        table2_columns = (
            'Технология',
            'Материал',
            'Единица измерения',
            'Количество',
            'Цена',
            'Примечание'
        )

        table2_rows = execute_raw_sql(f'''
        SELECT object_technology.technology_id,
        estimation.material_id, estimation.count,
        estimation.unit, estimation.price,
        estimation.note
        FROM timetable
        INNER JOIN object_technology ON
        timetable.object_technology_id = object_technology.id
        INNER JOIN estimation ON timetable.id = estimation.timetable_id
        WHERE timetable.building_id = {building}
        ''')

    return render(request,
                  'task/result_task7.html',
                  {'table_name': table_name,
                   'table1_columns': table1_columns,
                   'table1_rows': table1_rows,
                   'table2_columns': table2_columns,
                   'table2_rows': table2_rows})


def task8(request):
    table_name = 'Задание 8'
    return render(request,
                  'task/task8.html',
                  {'table_name': table_name})


def task8_result(request):
    building = request.GET.get('building')

    if building is not None:
        table_name = "Строительный объект"
        if not table_exist(table_name='building', pk_name='id',
                           id=building, is_string=False):
            raise Http404('Участка с данным номером не существует')

        table1_columns = (
            'Технология',
            'Номер бригады',
            'Дата начала факт',
            'Дата окончания факт',
        )

        table1_rows = execute_raw_sql(f'''
        SELECT object_technology.technology_id,
        timetable.brigade_id, timetable.date_technology_fact_start,
        timetable.date_technology_fact_end
        FROM timetable
        INNER JOIN object_technology ON
        timetable.object_technology_id = object_technology.id
        WHERE timetable.building_id = {building}
        ''')

        table2_columns = (
            'Технология',
            'Материал',
            'Единица измерения',
            'Количество факт',
            'Цена факт',
            'Примечание'
        )

        table2_rows = execute_raw_sql(f'''
        SELECT object_technology.technology_id,
        estimation_fact.material_id, estimation_fact.count,
        estimation_fact.unit, estimation_fact.price,
        estimation_fact.note
        FROM timetable
        INNER JOIN object_technology ON
        timetable.object_technology_id = object_technology.id
        INNER JOIN estimation_fact ON
        timetable.id = estimation_fact.timetable_id
        WHERE timetable.building_id = {building}
        ''')

    return render(request,
                  'task/result_task8.html',
                  {'table_name': table_name,
                   'table1_columns': table1_columns,
                   'table1_rows': table1_rows,
                   'table2_columns': table2_columns,
                   'table2_rows': table2_rows})


def task9(request):
    table_name = 'Задание 9'
    rows = execute_raw_sql('''
    SELECT name FROM technology
    ''')
    return render(request,
                  'task/task9.html',
                  {'table_name': table_name,
                   'rows': rows})


def task9_result(request):
    if not request.GET.get('construction') is None:
        construction = request.GET.get('construction')
    technology_name = request.GET.get('technology_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if construction is not None:
        table_name = "Строительный объект"
        if not table_exist(table_name='construction', pk_name='id',
                           id=construction, is_string=False):
            raise Http404('Участка с данным номером не существует')

        table_columns = (
            'Строительный объект',
            'Номер бригады',
            'Дата начала работ',
            'Дата окончания работ',
        )

        if request.GET.get('construction') is None:
            table_rows = execute_raw_sql(f'''
            SELECT timetable.building_id, timetable.brigade_id,
            timetable.date_technology_start, timetable.date_technology_end
            FROM construction
            INNER JOIN region ON construction.id = region.construction_id
            INNER JOIN building ON region.cadastral_number = building.region_id
            INNER JOIN timetable ON building.id = timetable.building_id
            INNER JOIN object_technology ON
            timetable.object_technology_id = object_technology.id
            WHERE object_technology.technology_id = '{technology_name}' AND
            date_technology_start >= '{start_date}' AND
            date_technology_end <= '{end_date}'
            ''')
        else:
            table_rows = execute_raw_sql(f'''
            SELECT timetable.building_id, timetable.brigade_id,
            timetable.date_technology_start, timetable.date_technology_end
            FROM construction
            INNER JOIN region ON construction.id = region.construction_id
            INNER JOIN building ON region.cadastral_number = building.region_id
            INNER JOIN timetable ON building.id = timetable.building_id
            INNER JOIN object_technology ON
            timetable.object_technology_id = object_technology.id
            WHERE object_technology.technology_id = '{technology_name}' AND
            date_technology_start >= '{start_date}' AND
            date_technology_end <= '{end_date}' AND
            construction.id = {construction}
            ''')

    return render(request,
                  'task/result.html',
                  {'table_name': table_name,
                   'table_columns': table_columns,
                   'table_rows': table_rows})


def task10(request):
    table_name = 'Задание 10'
    return render(request,
                  'task/task10.html',
                  {'table_name': table_name})


def task10_result(request):
    region = request.GET.get('region')
    construction = request.GET.get('construction')

    table_name = "Строительная организация"
    table_columns = (
        'Название технологии',
        'Дата начала работ',
        'Дата окончания работ',
        'Дата начала работ факт',
        'Дата окончания работ факт'
    )

    table_rows = execute_raw_sql('''
    SELECT object_technology.technology_id,
    timetable.date_technology_start,
    timetable.date_technology_end,
    timetable.date_technology_fact_start,
    timetable.date_technology_fact_end
    FROM timetable
    INNER JOIN object_technology ON
    timetable.object_technology_id = object_technology.id
    WHERE
    date_technology_start > date_technology_fact_start OR
    date_technology_end < date_technology_fact_end
    ''')

    if region is not None:
        table_name = "Участок"
        if not table_exist(table_name='region', pk_name='cadastral_number',
                           id=region, is_string=True):
            raise Http404('Участка с данным номером не существует')

        table_columns = (
            'Название технологии',
            'Дата начала работ',
            'Дата окончания работ',
            'Дата начала работ факт',
            'Дата окончания работ факт'
        )

        table_rows = execute_raw_sql(f'''
        SELECT object_technology.technology_id,
        timetable.date_technology_start,
        timetable.date_technology_end,
        timetable.date_technology_fact_start,
        timetable.date_technology_fact_end
        FROM region
        INNER JOIN building ON region.cadastral_number = building.region_id
        INNER JOIN timetable ON building.id = timetable.building_id
        INNER JOIN object_technology ON
        timetable.object_technology_id = object_technology.id
        WHERE region.cadastral_number = '{region}' AND
        (date_technology_start > date_technology_fact_start OR
        date_technology_end < date_technology_fact_end)
        ''')

    if construction is not None:
        table_name = "Строительное управление"
        if not table_exist(table_name='construction', pk_name='id',
                           id=construction, is_string=False):
            raise Http404('Участка с данным номером не существует')

        table_columns = (
            'Название технологии',
            'Дата начала работ',
            'Дата окончания работ',
            'Дата начала работ факт',
            'Дата окончания работ факт'
        )

        table_rows = execute_raw_sql(f'''
        SELECT object_technology.technology_id,
        timetable.date_technology_start,
        timetable.date_technology_end,
        timetable.date_technology_fact_start,
        timetable.date_technology_fact_end
        FROM construction
        INNER JOIN region ON construction.id = region.construction_id
        INNER JOIN building ON region.cadastral_number = building.region_id
        INNER JOIN timetable ON building.id = timetable.building_id
        INNER JOIN object_technology ON
        timetable.object_technology_id = object_technology.id
        WHERE construction.id = {construction} AND
        (date_technology_start > date_technology_fact_start OR
        date_technology_end < date_technology_fact_end)
        ''')

    return render(request,
                  'task/result.html',
                  {'table_name': table_name,
                   'table_columns': table_columns,
                   'table_rows': table_rows})


def task11(request):
    table_name = 'Задание 11'
    return render(request,
                  'task/task11.html',
                  {'table_name': table_name})


def task11_result(request):
    region = request.GET.get('region')
    construction = request.GET.get('construction')

    table_name = "Строительная организация"
    table_columns = (
        'Строительный объект',
        'Название материала',
        'Количество',
        'Количество факт',
        'Цена',
        'Цена факт'
    )

    table_rows = execute_raw_sql('''
    SELECT timetable.building_id,
    estimation.material_id,
    estimation.count, estimation_fact.count,
    estimation.price, estimation_fact.price
    FROM timetable
    INNER JOIN estimation ON timetable.id = estimation.timetable_id
    INNER JOIN estimation_fact ON timetable.id = estimation_fact.timetable_id
    WHERE estimation.material_id = estimation_fact.material_id AND
    (estimation.count < estimation_fact.count OR
    estimation.price < estimation_fact.price)
    ''')

    if region is not None:
        table_name = "Участок"
        if not table_exist(table_name='region', pk_name='cadastral_number',
                           id=region, is_string=True):
            raise Http404('Участка с данным номером не существует')

        table_columns = (
            'Строительный объект',
            'Название материала',
            'Количество',
            'Количество факт',
            'Цена',
            'Цена факт'
        )

        table_rows = execute_raw_sql(f'''
        SELECT timetable.building_id,
        estimation.material_id,
        estimation.count, estimation_fact.count as count_fact,
        estimation.price, estimation_fact.price as price_fact
        FROM region
        INNER JOIN building ON region.cadastral_number = building.region_id
        INNER JOIN timetable ON building.id = timetable.building_id
        INNER JOIN estimation ON timetable.id = estimation.timetable_id
        INNER JOIN estimation_fact
        ON timetable.id = estimation_fact.timetable_id
        WHERE region.cadastral_number = {region} AND
        estimation.material_id = estimation_fact.material_id AND
        (estimation.count < estimation_fact.count OR
        estimation.price < estimation_fact.price)
        ''')

    if construction is not None:
        table_name = "Строительное управление"
        if not table_exist(table_name='construction', pk_name='id',
                           id=construction, is_string=False):
            raise Http404('Участка с данным номером не существует')

        table_columns = (
            'Строительный объект',
            'Название материала',
            'Количество',
            'Количество факт',
            'Цена',
            'Цена факт'
        )

        table_rows = execute_raw_sql(f'''
        SELECT timetable.building_id,
        estimation.material_id,
        estimation.count, estimation_fact.count as count_fact,
        estimation.price, estimation_fact.price as price_fact
        FROM construction
        INNER JOIN region ON construction.id = region.construction_id
        INNER JOIN building ON region.cadastral_number = building.region_id
        INNER JOIN timetable ON building.id = timetable.building_id
        INNER JOIN estimation ON timetable.id = estimation.timetable_id
        INNER JOIN estimation_fact
        ON timetable.id = estimation_fact.timetable_id
        WHERE construction.id = {construction} AND
        estimation.material_id = estimation_fact.material_id AND
        (estimation.count < estimation_fact.count OR
        estimation.price < estimation_fact.price)
        ''')

    return render(request,
                  'task/result.html',
                  {'table_name': table_name,
                   'table_columns': table_columns,
                   'table_rows': table_rows})


def task12(request):
    table_name = 'Задание 12'
    return render(request,
                  'task/task12.html',
                  {'table_name': table_name})


def task12_result(request):
    brigade = request.GET.get('brigade')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if brigade is not None:
        table_name = "Бригада"
        if not table_exist(table_name='brigade', pk_name='id',
                           id=brigade, is_string=False):
            raise Http404('Участка с данным номером не существует')

        table_columns = (
            'Строительный объект',
            'Название технологии',
            'Дата начала',
            'Дата окончания'
        )

        table_rows = execute_raw_sql(f'''
        SELECT building_id, object_technology.technology_id,
        date_technology_start, date_technology_end
        FROM timetable
        INNER JOIN object_technology ON
        object_technology.id = timetable.object_technology_id
        WHERE brigade_id = {brigade} AND
        date_technology_start >= '{start_date}' AND
        date_technology_end <= '{end_date}'
        ''')

    return render(request,
                  'task/result.html',
                  {'table_name': table_name,
                   'table_columns': table_columns,
                   'table_rows': table_rows})


def task13(request):
    table_name = 'Задание 13'
    rows = execute_raw_sql('''
    SELECT name FROM technology
    ''')
    return render(request,
                  'task/task13.html',
                  {'table_name': table_name,
                   'rows': rows})


def task13_result(request):
    technology_name = request.GET.get('technology_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    table_name = 'Бригады'
    table_columns = (
        'Номер бригады', 'Строительный объект',
        'Дата начала работ', 'Дата окончания работ'
    )
    
    table_rows = execute_raw_sql(f'''
    SELECT timetable.brigade_id,
    timetable.building_id, timetable.date_technology_start,
    timetable.date_technology_end
    FROM timetable
    INNER JOIN object_technology ON
    timetable.object_technology_id = object_technology.id
    WHERE object_technology.technology_id = '{technology_name}' AND
    date_technology_start >= '{start_date}' AND
    date_technology_end <= '{end_date}'
    ''')

    return render(request,
                  'task/result.html',
                  {'table_name': table_name,
                   'table_columns': table_columns,
                   'table_rows': table_rows})


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


class ContractView(EntityView):
    table_name = 'contract'
    table_alias = 'Договор строительства объекта'
    column_name = (
        'Номер договора', 'Номер объекта',
        'Заказчик', 'Дата подписания',
        'Дата сдачи', 'Стоимость работ'
    )


class QualityView(EntityView):
    table_name = 'quality'
    table_alias = 'Характеристика'
    column_name = (
        'Название',
    )


class ObjectQualityView(EntityView):
    table_name = 'object_quality'
    table_alias = 'Характеристики объекта'
    column_name = (
        'ID', 'Тип объекта',
        'Характеристика', 'Еденица измерения',
        'Количество', 'Комментарий'
    )


class TechnologyView(EntityView):
    table_name = 'technology'
    table_alias = 'Технология'
    column_name = (
        'Название',
    )


class MaterialView(EntityView):
    table_name = 'material'
    table_alias = 'Материал'
    column_name = (
        'Название',
    )


class ObjectTechnologyView(EntityView):
    table_name = 'object_technology'
    table_alias = 'Технология объекта'
    column_name = (
        'ID',
        'Тип объекта',
        'Технология',
    )


class TechnologyMaterialView(EntityView):
    table_name = 'technology_material'
    table_alias = 'Материалы технологии'
    column_name = (
        'Название материала',
        'Технология'
    )


class EquipmentBuildingView(EntityView):
    table_name = 'equipment_building'
    table_alias = 'Техника строительного объекта'
    column_name = (
        'ID', 'Строительный объект',
        'Тип Техники', 'Строительной управление',
        'Кол-во техники', 'Дата начала работ',
        'Дата окончания работ'
    )


class TimetableView(EntityView):
    table_name = 'timetable'
    table_alias = 'Расписание'
    column_name = (
        'ID', 'Строительный объект',
        'Технология', 'Номер бригады',
        'Дата начала', 'Дата окончания',
        'Дата начала факт', 'Дата окончания факт',
    )


class EstimationView(EntityView):
    table_name = 'estimation'
    table_alias = 'Смета'
    column_name = (
        'ID', 'Материал',
        'Расписание ID', 'Еденица измерения',
        'Кол-во', 'Цена',
        'Примечание'
    )


class EstimationFactView(EntityView):
    table_name = 'estimation_fact'
    table_alias = 'Смета факт'
    column_name = (
        'ID', 'Материал',
        'Расписание ID', 'Еденица измерения',
        'Кол-во', 'Цена',
        'Примечание'
    )
