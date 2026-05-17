from django.core.management.base import BaseCommand
from django.db import connection
from salon.models import Service, Master, Review

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # video_url колонкасын кошуу
        with connection.cursor() as cursor:
            try:
                cursor.execute("ALTER TABLE salon_galleryphoto ADD COLUMN video_url VARCHAR(200) DEFAULT ''")
                self.stdout.write('video_url колонкасы кошулду!')
            except Exception:
                self.stdout.write('video_url мурун бар')
        
        Service.objects.all().delete()
        Master.objects.all().delete()
        
        # УСЛУГАЛАР
        services = [
            ('Маникюр без покрытия', 'nails', 400, 60),
            ('Маникюр с покрытием (шеллак)', 'nails', 800, 90),
            ('Наращивание ногтей', 'nails', 1500, 120),
            ('Коррекция ногтей', 'nails', 1000, 90),
            ('Ремонт ногтей', 'nails', 150, 20),
            ('Снятие покрытия', 'nails', 150, 30),
            ('Мужской маникюр', 'nails', 600, 60),
            ('Педикюр с покрытием', 'nails', 1500, 90),
            ('Гигиенический педикюр', 'nails', 800, 60),
            ('Smart педикюр', 'nails', 1000, 75),
            ('Мужской педикюр', 'nails', 1500, 90),
            ('Дизайн ногтей', 'nails', 200, 30),
            ('Стрижка', 'hair', 850, 60),
            ('Стрижка у топ мастера Айпери', 'hair', 950, 60),
            ('Вечерняя укладка', 'hair', 600, 60),
            ('Окрашивание в один тон', 'hair', 900, 120),
            ('Химическая завивка', 'hair', 2500, 180),
            ('Наращивание волос', 'hair', 3000, 240),
            ('Полировка волос', 'hair', 900, 60),
            ('Модное окрашивание (короткие)', 'hair', 6500, 180),
            ('Модное окрашивание (средние)', 'hair', 9000, 210),
            ('Модное окрашивание (длинные)', 'hair', 13500, 240),
            ('Кератиновое выпрямление (короткие)', 'hair', 3250, 120),
            ('Кератиновое выпрямление (средние)', 'hair', 4250, 150),
            ('Кератиновое выпрямление (длинные)', 'hair', 7000, 180),
            ('Экспресс локоны', 'hair', 700, 45),
            ('Вечерние локоны', 'hair', 900, 60),
            ('Собранные прически', 'hair', 900, 60),
            ('Макияж дневной', 'makeup', 1000, 60),
            ('Макияж вечерний', 'makeup', 1200, 75),
            ('Макияж возрастной', 'makeup', 800, 60),
            ('Макияж свадебный', 'makeup', 3000, 120),
            ('Накладные ресницы', 'makeup', 200, 30),
            ('Коррекция бровей', 'makeup', 200, 30),
            ('Наращивание ресниц классический объем', 'brows', 1000, 120),
            ('Наращивание ресниц 2D', 'brows', 1300, 150),
            ('Наращивание ресниц 3D', 'brows', 1500, 180),
            ('Наращивание ресниц Мега объем', 'brows', 1700, 210),
            ('Снятие ресниц', 'brows', 200, 30),
            ('Ламинирование ресниц', 'brows', 1000, 90),
        ]
        
        for name, cat, price, duration in services:
            Service.objects.create(name=name, category=cat, price=price, duration=duration)
        
        # МАСТЕРЛЕР
        masters = [
            ('Айпери Ибраимова', 'Топ мастер — стрижки, окрашивание', 5),
            ('Мастер маникюра', 'Маникюр, педикюр, наращивание', 3),
            ('Мастер макияжа', 'Макияж, брови, ресницы', 3),
        ]
        
        for name, spec, exp in masters:
            Master.objects.create(name=name, specialty=spec, experience_years=exp)
        
        # ОТЗЫВДАР
        reviews = [
            ('Айгуль М.', 5, 'Отличный салон! Мастера профессиональные, атмосфера приятная. Всем рекомендую!'),
            ('Нурзат К.', 5, 'Делаю маникюр только здесь. Всегда аккуратно и красиво. Спасибо Подружки!'),
            ('Жылдыз А.', 5, 'Айпери — лучший мастер по стрижкам в Оше! Очень довольна результатом.'),
        ]
        
        for name, rating, text in reviews:
            try:
                Review.objects.get_or_create(client_name=name, defaults={'rating': rating, 'text': text, 'is_approved': True})
            except Exception:
                pass
        
        self.stdout.write('Маалыматтар кошулду!')
