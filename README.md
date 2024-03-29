# Техническое задание:
## Информационная система строительной организации
**Строительное управление** - строительная организация состоит из строительных управлений, каждое строительное управление ведет работы на одном или нескольких участках. Строительным управлением возглавляет один директор он назначается из персонала строительной организации. За каждым управлением закреплена строительная техника.

__Участок__ - территория строительного управления на которой идет строительство одного или нескольких объектов. Каждый участок обладает уникальным кадастровым номером. За работу на участке отвечает начальник участка он назначается из персонала строительного управления.

__Строительный объект__ - объект на котором ведутся строительные работы различного рода. Каждый объект принадлежит к какому-то классу объектов: жилой дом, больница, мост, дорога. Каждая из перечисленных категорий объектов имеет характеристики, свойственные только этой или нескольким категориям: например, к характеристикам жилых домов относится этажность, тип строительного материала, число квартир, для мостов уникальными характеристиками являются тип пролетного строения, ширина, количество полос для движения.

__Заказчик__ - лицо (физическое или юридическое) заинтересованное в качественном выполнении исполнителем работ на строительном объекте. Перед выполнением возведения строительного объекта строительная организация заключает с заказчиком договор.

__Договор строительного подряда__ - строительная организация обязуется в установленный договором срок произвести все строительные работы заказчика, а заказчик обязуется создать подрядчику необходимые условия для выполнения работ, принять их результат и уплатить обусловленную цену.

__Персонал__ - За каждым работником закреплена его специальность. За каждой специальностью закреплен тип, к которой он относится. Например: инженерно-технического персонала (инженеры, технологи, техники) и рабочих (каменщики, бетонщики, отделочники, сварщики, электрики, шофера, слесари и пр.). В зависимости от типа, работник может занимать различного рода должности ( начальник участка, директор строительного управления, бригадир)

__Бригада__ - Рабочие объединяются в бригады, которыми руководят бригадиры. Бригадиры выбираются из числа рабочих. Каждая бригада имеет свой уникальный номер. Бригада не закреплена за строительным объектом, поэтому может выполнять работы на различных объектах, под управлением разных строительных управлений.

__Тип должности__ - разделение должностей на различные виды в зависимости от типа выполняемой деятельности (Инженерно-техническая, рабочая)

__График работы__ - Технология строительства того или иного объекта предполагает выполнение определенного набора видов работ, необходимых для сооружения данного типа объекта. Например, для жилого дома – это возведение фундамента, кирпичные работы, прокладка водоснабжения и т.д. Каждый вид работ на объекте выполняется одной бригадой. Для организации работ на объекте составляются графики работ, указывающие, в каком порядке и в какие сроки выполняются те или иные работы, а также смета, определяющая, какие строительные материалы и в каких количествах необходимы для сооружения объекта. По результатам выполнения работ составляется итоговая смета с указанием сроков выполнения работ и фактических расходов материалов.

## Список сущностей:
- Строительное управление
- Участок
- Персонал
- Специальность
- Тип должности
- Бригада
- Персонал бригады
- График работы
- Смета
- Смета факт
- Материал технологии
- Характеристика объекта
- Технология объекта
- Справочник характеристик
- Справочник материалов
- Тип объекта
- Строительный объект
- Договор
- Заказчик
- Тип техники
- Техника управления
- Техника строительного объекта

## Запросы в информационной системе:
1. Получите перечень строительных управлений и/или участков и их руководителей. 
2. Получите список специалистов инженерно-технического состава обозначенного участка или строительного управления с указанием их должностей. 
3. Получите перечень объектов, возводимых указанным строительным управлением и/или участком, и графики их возведения. 
4. Получите состав бригад, работавших (работающих) на строительстве указанного объекта. 
5. Получите перечень строительной техники, приданной указанному строительному управлению. 
6. Получите перечень строительной техники, выделенной на указанный объект либо работавшей на объекте в течение указанного периода времени. 
7. Получите график и смету на строительство указанного объекта. 
8. Получите отчет о сооружении указанного объекта. 
9. Получите перечень объектов, возводимых в некотором строительном управлении или в целом по организации, на которых в обозначенный период времени выполнялся указанный вид строительных работ. 
10. Получите перечень видов строительных работ, по которым имело место превышение сроков выполнения на указанном участке, строительном управлении или в целом по организации.
11. Получите перечень строительных материалов, по которым имело место превышение по смете на указанном участке, строительном управлении или в целом по организации. 
12. Получите перечень видов строительных работ, выполненных указанной бригадой в течение обозначенного периода времени с указанием объектов, где эти работы выполнялись.
13. Получите перечень бригад, выполнявших указанный вид строительных работ в течение обозначенного периода времени с указанием объектов, где эти работы выполнялись.




