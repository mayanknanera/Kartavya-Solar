from django.core.management.base import BaseCommand
from core.models import Product

# All available product images (cycled across products)
IMAGES = [
    "products/Gemini_Generated_Image_6z6tqg6z6tqg6z6t.png",
    "products/Gemini_Generated_Image_bzimk8bzimk8bzim.png",
    "products/Gemini_Generated_Image_fsew5rfsew5rfsew.png",
    "products/Gemini_Generated_Image_gj4yiggj4yiggj4y.png",
    "products/Gemini_Generated_Image_hixytthixytthixy.png",
    "products/Gemini_Generated_Image_jjhnwgjjhnwgjjhn.png",
    "products/Gemini_Generated_Image_qszrqvqszrqvqszr.png",
    "products/Gemini_Generated_Image_qtihgzqtihgzqtih.png",
    "products/Gemini_Generated_Image_v6p8quv6p8quv6p8.png",
    "products/Gemini_Generated_Image_y2n9tny2n9tny2n9.png",
    "products/Gemini_Generated_Image_z077zmz077zmz077.png",
]

PRODUCTS = [
    # ── Solar Panels (3) ──────────────────────────────────────────────────────
    {
        "name": "400W Polycrystalline Solar Panel",
        "slug": "400w-polycrystalline-solar-panel",
        "category": "SOLAR_PANELS",
        "price": 9500.00,
        "stock_quantity": 120,
        "min_order_quantity": 1,
        "max_order_quantity": 100,
        "description": (
            "Budget-friendly 400W polycrystalline panel with 18% efficiency. "
            "Ideal for small homes and rural electrification. "
            "Aluminium alloy frame, IP67 junction box, 10-year product warranty."
        ),
    },
    {
        "name": "540W Monocrystalline Solar Panel",
        "slug": "540w-monocrystalline-solar-panel",
        "category": "SOLAR_PANELS",
        "price": 15500.00,
        "stock_quantity": 100,
        "min_order_quantity": 1,
        "max_order_quantity": 50,
        "description": (
            "High-efficiency 540W monocrystalline panel with 21% efficiency. "
            "Anti-reflective coating, half-cut cell technology, and 25-year "
            "performance warranty. Ideal for residential and commercial rooftops."
        ),
    },
    {
        "name": "650W Bifacial Solar Panel",
        "slug": "650w-bifacial-solar-panel",
        "category": "SOLAR_PANELS",
        "price": 22000.00,
        "stock_quantity": 60,
        "min_order_quantity": 1,
        "max_order_quantity": 30,
        "description": (
            "Premium 650W bifacial panel that generates power from both sides. "
            "Up to 30% extra yield from reflected light. "
            "MNRE approved, 25-year linear power warranty, suitable for large commercial plants."
        ),
    },

    # ── Inverters (3) ─────────────────────────────────────────────────────────
    {
        "name": "3kW On-Grid Solar Inverter",
        "slug": "3kw-on-grid-solar-inverter",
        "category": "INVERTERS",
        "price": 28000.00,
        "stock_quantity": 40,
        "min_order_quantity": 1,
        "max_order_quantity": 10,
        "description": (
            "3kW single-phase grid-tied inverter with 97.5% efficiency. "
            "Supports net metering, built-in WiFi monitoring, and anti-islanding protection. "
            "5-year warranty. Perfect for small residential rooftop systems."
        ),
    },
    {
        "name": "5kW Hybrid Solar Inverter",
        "slug": "5kw-hybrid-solar-inverter",
        "category": "INVERTERS",
        "price": 48000.00,
        "stock_quantity": 35,
        "min_order_quantity": 1,
        "max_order_quantity": 10,
        "description": (
            "5kW hybrid inverter with MPPT technology supporting both on-grid "
            "and off-grid operation with battery backup. "
            "Built-in WiFi monitoring, touch LCD display, and 5-year warranty."
        ),
    },
    {
        "name": "10kW Three-Phase On-Grid Inverter",
        "slug": "10kw-three-phase-on-grid-inverter",
        "category": "INVERTERS",
        "price": 85000.00,
        "stock_quantity": 20,
        "min_order_quantity": 1,
        "max_order_quantity": 5,
        "description": (
            "10kW three-phase grid-tied inverter with 98.2% peak efficiency. "
            "Dual MPPT, real-time monitoring via app, and remote firmware updates. "
            "Ideal for commercial rooftops and industrial installations."
        ),
    },

    # ── Batteries (3) ─────────────────────────────────────────────────────────
    {
        "name": "100Ah Tubular Solar Battery",
        "slug": "100ah-tubular-solar-battery",
        "category": "BATTERIES",
        "price": 10500.00,
        "stock_quantity": 80,
        "min_order_quantity": 1,
        "max_order_quantity": 20,
        "description": (
            "100Ah tall tubular battery designed for solar applications. "
            "Deep discharge capability, 1200+ cycle life, and low water loss. "
            "Suitable for small homes and shops with 2–4 hour backup requirement."
        ),
    },
    {
        "name": "150Ah Tubular Solar Battery",
        "slug": "150ah-tubular-solar-battery",
        "category": "BATTERIES",
        "price": 16500.00,
        "stock_quantity": 60,
        "min_order_quantity": 1,
        "max_order_quantity": 20,
        "description": (
            "Heavy-duty 150Ah tubular battery for solar storage. "
            "1500+ cycle life, deep discharge capability, and excellent charge retention. "
            "Low maintenance design with 3-year warranty."
        ),
    },
    {
        "name": "200Ah Lithium-Ion Solar Battery",
        "slug": "200ah-lithium-ion-solar-battery",
        "category": "BATTERIES",
        "price": 95000.00,
        "stock_quantity": 18,
        "min_order_quantity": 1,
        "max_order_quantity": 8,
        "description": (
            "Advanced 200Ah LiFePO4 lithium battery for solar storage. "
            "Lightweight, 6000+ cycle life, fast charging, and built-in BMS protection. "
            "10-year warranty. Ideal for premium residential and commercial systems."
        ),
    },

    # ── Water Heaters (2) ─────────────────────────────────────────────────────
    {
        "name": "200L Solar Water Heater",
        "slug": "200l-solar-water-heater",
        "category": "WATER_HEATERS",
        "price": 22000.00,
        "stock_quantity": 30,
        "min_order_quantity": 1,
        "max_order_quantity": 5,
        "description": (
            "200-litre evacuated tube solar water heater for 3–5 family members. "
            "2.5mm GI inner tank with marine-grade coating, 50mm PUF insulation, "
            "and electric backup. 5-year warranty."
        ),
    },
    {
        "name": "300L Solar Water Heater",
        "slug": "300l-solar-water-heater",
        "category": "WATER_HEATERS",
        "price": 35000.00,
        "stock_quantity": 25,
        "min_order_quantity": 1,
        "max_order_quantity": 5,
        "description": (
            "300-litre solar water heater for 6–8 family members or small hotels. "
            "High-density PUF insulation, GI powder-coated stand, and electric backup. "
            "Kartavya Solar signature marine-grade inner coating. 5-year warranty."
        ),
    },

    # ── Mounting Structures (2) ───────────────────────────────────────────────
    {
        "name": "Galvanized Steel Rooftop Mounting Structure",
        "slug": "galvanized-steel-rooftop-mounting-structure",
        "category": "MOUNTING",
        "price": 6500.00,
        "stock_quantity": 80,
        "min_order_quantity": 1,
        "max_order_quantity": 50,
        "description": (
            "Heavy-duty hot-dip galvanized steel mounting structure for RCC rooftops. "
            "Wind-load tested up to 150 km/h, corrosion-resistant, and easy to install. "
            "Fits panels from 300W to 650W. Suitable for all Indian weather conditions."
        ),
    },
    {
        "name": "Aluminium Tin-Shed Mounting Structure",
        "slug": "aluminium-tin-shed-mounting-structure",
        "category": "MOUNTING",
        "price": 4800.00,
        "stock_quantity": 60,
        "min_order_quantity": 1,
        "max_order_quantity": 50,
        "description": (
            "Lightweight aluminium mounting structure designed for tin-shed and "
            "metal rooftops. Anodized finish for corrosion resistance, "
            "adjustable tilt angle (10°–30°), and compatible with all standard panel sizes."
        ),
    },

    # ── Accessories (3) ───────────────────────────────────────────────────────
    {
        "name": "Solar DC Cable 4mm² — 100m Roll",
        "slug": "solar-dc-cable-4mm-100m",
        "category": "ACCESSORIES",
        "price": 4500.00,
        "stock_quantity": 50,
        "min_order_quantity": 1,
        "max_order_quantity": 20,
        "description": (
            "4mm² TÜV-certified solar DC cable for outdoor use. "
            "UV resistant, flame retardant, and rated for -40°C to +90°C. "
            "100-metre roll. Suitable for all rooftop and ground-mount installations."
        ),
    },
    {
        "name": "60A MPPT Solar Charge Controller",
        "slug": "60a-mppt-solar-charge-controller",
        "category": "ACCESSORIES",
        "price": 18500.00,
        "stock_quantity": 55,
        "min_order_quantity": 1,
        "max_order_quantity": 15,
        "description": (
            "60A MPPT charge controller with colour LCD display and dual USB ports. "
            "98% tracking efficiency, supports 12V/24V/48V battery banks, "
            "and protects against overcharge, over-discharge, and short circuit."
        ),
    },
    {
        "name": "Solar MC4 Connector Set (10 Pairs)",
        "slug": "solar-mc4-connector-set-10-pairs",
        "category": "ACCESSORIES",
        "price": 850.00,
        "stock_quantity": 200,
        "min_order_quantity": 1,
        "max_order_quantity": 50,
        "description": (
            "IP67-rated MC4 solar connectors for secure panel-to-cable connections. "
            "Pack of 10 male + 10 female connectors. "
            "UV stabilised, rated for 1000V DC and 30A continuous current."
        ),
    },

    # ── Cleaning Systems (2) ──────────────────────────────────────────────────
    {
        "name": "Automatic Solar Panel Sprinkler System",
        "slug": "automatic-solar-panel-sprinkler-system",
        "category": "CLEANING",
        "price": 32000.00,
        "stock_quantity": 15,
        "min_order_quantity": 1,
        "max_order_quantity": 3,
        "description": (
            "Fully automatic sprinkler cleaning system for rooftop solar panels. "
            "Programmable timer controller, 360° rotating nozzles, and stainless steel pipes. "
            "Removes dust and bird droppings to maintain 100% panel output. "
            "Developed in-house by Kartavya Solar."
        ),
    },
    {
        "name": "Professional Solar Panel Cleaning Kit",
        "slug": "professional-solar-panel-cleaning-kit",
        "category": "CLEANING",
        "price": 5500.00,
        "stock_quantity": 40,
        "min_order_quantity": 1,
        "max_order_quantity": 10,
        "description": (
            "Manual cleaning kit with 6-metre telescopic pole, soft rotating brush, "
            "rubber squeegee, and 1-litre eco-friendly cleaning solution. "
            "Lightweight and easy to use. Ideal for residential rooftop systems."
        ),
    },
]


class Command(BaseCommand):
    help = "Seed the database with solar products (2–3 per category)."

    def handle(self, *args, **kwargs):
        created_count = 0
        updated_count = 0

        for index, data in enumerate(PRODUCTS):
            # Assign images by cycling through the available list
            data["image"] = IMAGES[index % len(IMAGES)]

            product, created = Product.objects.update_or_create(
                slug=data["slug"],
                defaults=data,
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  Created : {product.name}"))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f"  Updated : {product.name}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone — {created_count} created, {updated_count} updated "
                f"({created_count + updated_count} total products)."
            )
        )
