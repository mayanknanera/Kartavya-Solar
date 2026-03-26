from django.core.management.base import BaseCommand
from core.models import Product


class Command(BaseCommand):
    help = 'Add solar products to the database'

    def handle(self, *args, **kwargs):
        products = [
            {
                'name': '540W Monocrystalline Solar Panel',
                'description': 'High-efficiency 540W monocrystalline solar panel with 21% efficiency. Features anti-reflective coating and 25-year performance warranty. Ideal for residential and commercial rooftop installations.',
                'category': 'SOLAR_PANELS',
                'price': 15500.00,
                'stock_quantity': 100,
                'min_order_quantity': 1,
                'max_order_quantity': 50,
                'image': 'products/ChatGPT_Image_Feb_23_2026_04_31_04_PM.png',
                'slug': '540w-monocrystalline-solar-panel',
            },
            {
                'name': '5kW Hybrid Solar Inverter',
                'description': 'Advanced 5kW hybrid inverter with MPPT technology. Supports both on-grid and off-grid operation with battery backup. Built-in WiFi monitoring and 5-year warranty.',
                'category': 'INVERTERS',
                'price': 48000.00,
                'stock_quantity': 35,
                'min_order_quantity': 1,
                'max_order_quantity': 10,
                'image': 'products/ChatGPT_Image_Feb_23_2026_04_33_17_PM.png',
                'slug': '5kw-hybrid-solar-inverter',
            },
            {
                'name': '150Ah Tubular Solar Battery',
                'description': 'Heavy-duty 150Ah tubular battery designed for solar applications. Deep discharge capability with 1500+ cycle life. Low maintenance and excellent charge retention.',
                'category': 'BATTERIES',
                'price': 16500.00,
                'stock_quantity': 60,
                'min_order_quantity': 1,
                'max_order_quantity': 20,
                'image': 'products/ChatGPT_Image_Feb_23_2026_04_34_30_PM.png',
                'slug': '150ah-tubular-solar-battery',
            },
            {
                'name': '10kW On-Grid Solar Inverter',
                'description': '10kW grid-tied solar inverter with 98% efficiency. Ideal for large residential and commercial rooftop systems. Supports net metering with real-time monitoring.',
                'category': 'INVERTERS',
                'price': 85000.00,
                'stock_quantity': 20,
                'min_order_quantity': 1,
                'max_order_quantity': 5,
                'image': 'products/ChatGPT_Image_Feb_23_2026_04_36_00_PM.png',
                'slug': '10kw-on-grid-solar-inverter',
            },
            {
                'name': 'Galvanized Steel Mounting Structure',
                'description': 'Heavy-duty galvanized steel mounting structure for rooftop solar installations. Corrosion-resistant, wind-load tested up to 150 km/h. Suitable for all weather conditions.',
                'category': 'MOUNTING',
                'price': 6500.00,
                'stock_quantity': 80,
                'min_order_quantity': 1,
                'max_order_quantity': 50,
                'image': 'products/ChatGPT_Image_Feb_23_2026_04_36_35_PM.png',
                'slug': 'galvanized-steel-mounting-structure',
            },
            {
                'name': '300L Solar Water Heater',
                'description': '300-liter solar water heater with evacuated tube technology. Energy-efficient heating for 6-8 family members. Includes electric backup and 5-year warranty.',
                'category': 'WATER_HEATERS',
                'price': 35000.00,
                'stock_quantity': 25,
                'min_order_quantity': 1,
                'max_order_quantity': 5,
                'image': 'products/ChatGPT_Image_Feb_23_2026_04_37_47_PM.png',
                'slug': '300l-solar-water-heater',
            },
            {
                'name': 'Solar DC Cable 4mm² (100m)',
                'description': 'High-quality 4mm² solar DC cable rated for outdoor use. UV resistant, flame retardant, and temperature resistant (-40°C to +90°C). 100-meter roll.',
                'category': 'ACCESSORIES',
                'price': 4500.00,
                'stock_quantity': 50,
                'min_order_quantity': 1,
                'max_order_quantity': 20,
                'image': 'products/ChatGPT_Image_Feb_23_2026_04_42_59_PM.png',
                'slug': 'solar-dc-cable-4mm-100m',
            },
            {
                'name': '15kW Off-Grid Solar System Package',
                'description': 'Complete 15kW off-grid solar power system. Includes 28x540W panels, 15kW inverter, 400Ah battery bank, mounting structure, and all accessories. Perfect for remote locations.',
                'category': 'INVERTERS',
                'price': 950000.00,
                'stock_quantity': 8,
                'min_order_quantity': 1,
                'max_order_quantity': 3,
                'image': 'products/ChatGPT_Image_Feb_23_2026_04_47_06_PM.png',
                'slug': '15kw-off-grid-solar-system-package',
            },
            {
                'name': 'Professional Solar Panel Cleaning Kit',
                'description': 'Complete solar panel cleaning kit with 6-meter telescopic pole, soft rotating brush, squeegee, and eco-friendly cleaning solution. Maintains optimal panel efficiency.',
                'category': 'CLEANING',
                'price': 5500.00,
                'stock_quantity': 40,
                'min_order_quantity': 1,
                'max_order_quantity': 10,
                'image': 'products/ChatGPT_Image_Feb_23_2026_04_51_21_PM.png',
                'slug': 'professional-solar-panel-cleaning-kit',
            },
            {
                'name': '200Ah Lithium-Ion Solar Battery',
                'description': 'Advanced 200Ah lithium-ion battery for solar storage. Lightweight design with 6000+ cycle life, fast charging, and built-in BMS. 10-year warranty.',
                'category': 'BATTERIES',
                'price': 95000.00,
                'stock_quantity': 18,
                'min_order_quantity': 1,
                'max_order_quantity': 8,
                'image': 'products/ChatGPT_Image_Feb_23_2026_04_56_06_PM.png',
                'slug': '200ah-lithium-ion-solar-battery',
            },
            {
                'name': '60A MPPT Solar Charge Controller',
                'description': '60A MPPT solar charge controller with LCD display and USB ports. Maximizes solar panel output with 98% efficiency. Protects batteries from overcharging and deep discharge.',
                'category': 'ACCESSORIES',
                'price': 18500.00,
                'stock_quantity': 55,
                'min_order_quantity': 1,
                'max_order_quantity': 15,
                'image': 'products/ChatGPT_Image_Feb_23_2026_04_59_24_PM.png',
                'slug': '60a-mppt-solar-charge-controller',
            },
        ]

        created_count = 0
        updated_count = 0

        for product_data in products:
            product, created = Product.objects.update_or_create(
                slug=product_data['slug'],
                defaults=product_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {product.name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'Updated: {product.name}'))

        self.stdout.write(self.style.SUCCESS(f'\nTotal: {created_count} created, {updated_count} updated'))
