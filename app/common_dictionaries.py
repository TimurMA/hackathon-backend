import uuid
from decimal import Decimal

from app.company.models import Company
from app.competence.models import CompetenceContiguity, Competence
from app.vacancy.models import Vacancy, Location, VacancyCompetence


competence_list = [
    Competence(id='SQL', name='SQL базы данных'),
    Competence(id='NoSQL', name='NoSQL базы данных'),
    Competence(id='parallel processing', name='Массово параллельная обработка и анализ данных'),
    Competence(id='Hadoop', name='Hadoop'),
    Competence(id='data preprocessing', name='Качество и предобработка данных, подходы и инструменты'),
    Competence(id='data streaming', name='Потоковая обработка данных'),
    Competence(id='ML on big data', name='Машинное обучение на больших данных'),
    Competence(id='working with a distributed cluster system', name='Работа с распределенной кластерной системой'),
    Competence(id='parallel computing to speed up ML', name='Массово параллельные вычисления для ускорения машинного обучения'),
    Competence(id='reinforcement learning', name='Обучение с подкреплением и глубокое обучение с подкреплением'),
    Competence(id='the basics of deep learning', name='Основы глубокого обучения'),
    Competence(id='ML for generation image and video', name='Глубокое обучение для анализа и генерации изображений, видео'),
    Competence(id='ML for generation natural language', name='Глубокое обучение для анализа и генерации естественного языка'),
    Competence(id='NLP', name='Анализ естественного языка'),
    Competence(id='Image and video analysis', name='Анализ изображений и видео'),
    Competence(id='recommendation systems', name='Рекомендательные системы'),
    Competence(id='information search', name='Информационный поиск'),
    Competence(id='optimization methods', name='Методы оптимизации'),
    Competence(id='ML methods', name='Методы машинного обучения'),
    Competence(id='Programming language', name='Языки программирования и библиотеки'),
    Competence(id='evaluating the work of Al methods', name='Оценка качества работы методов ИИ'),
    Competence(id='statistical methods', name='Статистические методы и первичный анализ данных'),
    Competence(id='methodology for developing Al solutions', name='Процесс, стадии и методологии разработки решений на основе ИИ'),
]

location_list = [
    Location(
        country = 'Россия',
        region = 'Москва',
        city = 'Москва'
    ),
    Location(
        country = 'Россия',
        region = 'Тюменская область',
        city = 'Тюмень'
    )
]

company = Company(
    name = 'Компания'
)

vacancy_list = [
    {
        'name': 'Аналитик данных',
        'description':   '''
                        Специалист, который работает с данными компании, анализирует их и разрабатывает решения на основе ИИ.
                        Совместно с техническими аналитиками формирует технические метрики, которые зависят от бизнес-метрик.
                        В процессе выполнения проекта специалист:
                            - Определяет лучший метод машинного обучения и способ его адаптации к специфике задачи
                            - Разрабатывает новые признаки (feature-engineering)
                            - Реализует общий пайплайн решения
                            - Формирует техническую часть документации проекта
                        ''',
        'url': 'https://www.sberbank.com/ru',
        'vacancy_competencies': [
            VacancyCompetence(competence_id = "methodology for developing Al solutions", level = Decimal('7')),
            VacancyCompetence(competence_id = "statistical methods", level = Decimal('7')),
            VacancyCompetence(competence_id = "evaluating the work of Al methods", level = Decimal('7')),
            VacancyCompetence(competence_id = "Programming language", level = Decimal('7')),
            VacancyCompetence(competence_id = "ML methods", level = Decimal('7')),
            VacancyCompetence(competence_id = "optimization methods", level = Decimal('7')),
            VacancyCompetence(competence_id = "information search", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "recommendation systems", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "Image and video analysis", level = Decimal('7')),
            VacancyCompetence(competence_id = "NLP", level = Decimal('7')),
            VacancyCompetence(competence_id = "the basics of deep learning", level = Decimal('7')),
            VacancyCompetence(competence_id = "ML for generation image and video", level = Decimal('7')),
            VacancyCompetence(competence_id = "ML for generation natural language", level = Decimal('7')),
            VacancyCompetence(competence_id = "reinforcement learning", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "working with a distributed cluster system", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "ML on big data", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "SQL", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "NoSQL", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "Hadoop", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "parallel processing", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "data preprocessing", level = Decimal('4.5'))
        ]
    },
    {
        'name': 'Инженер данных',
        'description':   '''
                        Специалист, который отвечает за сбор, анализ, очистку и подготовку данных для последующего
                        использования. Работает с системами хранения и анализа данных, обеспечивая их эффективное
                        функционирование, а также поддержку систем версионирования данных.
                        ''',
        'url': 'https://www.sberbank.com/ru',
        'vacancy_competencies': [
            VacancyCompetence(competence_id = "methodology for developing Al solutions", level = Decimal('7')),
            VacancyCompetence(competence_id = "statistical methods", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "evaluating the work of Al methods", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "Programming language", level = Decimal('7')),
            VacancyCompetence(competence_id = "ML methods", level = Decimal('7')),
            VacancyCompetence(competence_id = "optimization methods", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "information search", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "Image and video analysis", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "NLP", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "the basics of deep learning", level = Decimal('7')),
            VacancyCompetence(competence_id = "ML for generation image and video", level = Decimal('7')),
            VacancyCompetence(competence_id = "ML for generation natural language", level = Decimal('7')),
            VacancyCompetence(competence_id = "parallel computing to speed up ML", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "working with a distributed cluster system", level = Decimal('7')),
            VacancyCompetence(competence_id = "ML on big data", level = Decimal('7')),
            VacancyCompetence(competence_id = "data streaming", level = Decimal('7')),
            VacancyCompetence(competence_id = "SQL", level = Decimal('9')),
            VacancyCompetence(competence_id = "NoSQL", level = Decimal('9')),
            VacancyCompetence(competence_id = "Hadoop", level = Decimal('7')),
            VacancyCompetence(competence_id = "parallel processing", level = Decimal('7')),
            VacancyCompetence(competence_id = "data preprocessing", level = Decimal('9'))
        ]
    },
    {
        'name': 'Технический аналитик в ИИ',
        'description':  '''
                        Специалист, который обеспечивает эффективное взаимодействие между аналитиком данных и заказчиком.
                        Анализирует потребности бизнеса, подтверждает и уточняет проблематику, анализирует бизнес-процессы и
                        выявляет ключевые артефакты данных в них. Также специалист оценивает техническую реализуемость
                        запроса, формализует техническое задание, и в дальнейшем может участвовать в документировании
                        результатов экспериментов и итогового тестирования.
                        ''',
        'url': 'https://www.sberbank.com/ru',
        'vacancy_competencies':  [
            VacancyCompetence(competence_id = "methodology for developing Al solutions", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "statistical methods", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "evaluating the work of Al methods", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "Programming language", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "ML methods", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "recommendation systems", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "Image and video analysis", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "NLP", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "the basics of deep learning", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "ML for generation image and video", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "ML for generation natural language", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "SQL", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "NoSQL", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "data preprocessing", level = Decimal('4.5'))
        ]
    },
    {
        'name': 'Менеджер в ИИ',
        'description':   '''
                        Специалист, который обеспечивает общее выполнение проекта, работу по бюджету, ресурсам, срокам. 
                        Отвечает за конверсию и вывод решений в продуктив на организационном уровне. Также в круг его
                        обязанностей может входить обработка пользовательских отзывов и части документирования продукта.
                        ''',
        'url': 'https://www.sberbank.com/ru',
        'vacancy_competencies': [
            VacancyCompetence(competence_id = "methodology for developing Al solutions", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "evaluating the work of Al methods", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "ML methods", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "Image and video analysis", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "NLP", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "the basics of deep learning", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "ML for generation image and video", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "ML for generation natural language", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "SQL", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "NoSQL", level = Decimal('4.5')),
            VacancyCompetence(competence_id = "data preprocessing", level = Decimal('4.5'))
        ]
    },
]

competence_contiguity_list = [
    CompetenceContiguity(
        first_competence_id = "ML for generation image and video",
        second_competence_id = "Image and video analysis",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "ML for generation natural language",
        second_competence_id = "NLP",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "the basics of deep learning",
        second_competence_id = "ML methods",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "reinforcement learning",
        second_competence_id = "the basics of deep learning",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "ML methods",
        second_competence_id = "statistical methods",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "ML methods",
        second_competence_id = "optimization methods",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "ML methods",
        second_competence_id = "evaluating the work of Al methods",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "parallel computing to speed up ML",
        second_competence_id = "parallel processing",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "ML for generation image and video",
        second_competence_id = "the basics of deep learning",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "ML for generation natural language",
        second_competence_id = "the basics of deep learning",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "Image and video analysis",
        second_competence_id = "ML methods",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "NLP",
        second_competence_id = "ML methods",
        contiguity_coefficient = Decimal("1")
    ),
    CompetenceContiguity(
        first_competence_id = "ML on big data",
        second_competence_id = "ML methods",
        contiguity_coefficient = Decimal("1")
    )
]