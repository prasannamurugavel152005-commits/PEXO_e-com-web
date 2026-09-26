from django.core.management.base import BaseCommand

from store.models import Category, Product


class Command(BaseCommand):
    help = 'Add sample INR-priced products to explore Pexo Market.'

    def handle(self, *args, **options):
        catalog = [
            {
                'category': 'Home & Living', 'name': 'Sculpted Ceramic Table Lamp', 'slug': 'sculpted-ceramic-table-lamp',
                'description': 'A softly sculpted ceramic base and warm linen shade bring an easy glow to a bedside or reading nook.',
                'price': '2499.00', 'stock': 18, 'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Home & Living', 'name': 'Sunday Morning Throw', 'slug': 'sunday-morning-throw',
                'description': 'A breathable, softly textured cotton throw for the sofa, the end of the bed, or a cool evening outside.',
                'price': '1899.00', 'stock': 24, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Tech & Audio', 'name': 'Studio Wireless Headphones', 'slug': 'studio-wireless-headphones',
                'description': 'Comfort-first over-ear headphones with balanced sound, simple controls, and a battery made for long days.',
                'price': '4999.00', 'stock': 14, 'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Tech & Audio', 'name': 'Pocket Bluetooth Speaker', 'slug': 'pocket-bluetooth-speaker',
                'description': 'A compact portable speaker with crisp everyday sound and an easy-to-pack shape for rooms and weekends away.',
                'price': '1999.00', 'stock': 30, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Style & Carry', 'name': 'Everywhere Canvas Tote', 'slug': 'everywhere-canvas-tote',
                'description': 'A sturdy, roomy canvas carryall with reinforced handles, ready for market mornings and daily errands.',
                'price': '799.00', 'stock': 36, 'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Style & Carry', 'name': 'Field Notes Watch', 'slug': 'field-notes-watch',
                'description': 'A clean, easy-to-read everyday watch with a quiet profile and a soft strap that wears comfortably all day.',
                'price': '3299.00', 'stock': 11, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Kitchen & Table', 'name': 'Daily Pour Coffee Set', 'slug': 'daily-pour-coffee-set',
                'description': 'A thoughtfully simple pour-over set for a slower first cup, including a ceramic dripper and matching server.',
                'price': '1599.00', 'stock': 16, 'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Kitchen & Table', 'name': 'Gather Round Serving Bowl', 'slug': 'gather-round-serving-bowl',
                'description': 'A generous stoneware bowl with a tactile glaze, equally at home holding fruit or sharing something warm.',
                'price': '1299.00', 'stock': 20, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Home & Living', 'name': 'Soft Grid Cushion Cover', 'slug': 'soft-grid-cushion-cover',
                'description': 'A textured cotton cushion cover in a calm woven grid, sized for a favorite chair or sofa.',
                'price': '899.00', 'stock': 28, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Home & Living', 'name': 'Pebble Planter Pair', 'slug': 'pebble-planter-pair',
                'description': 'Two small ceramic planters with a soft matte finish for herbs, succulents, and sunny windowsills.',
                'price': '1199.00', 'stock': 19, 'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1485955900006-10f4d324d411?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Home & Living', 'name': 'Oak Catchall Tray', 'slug': 'oak-catchall-tray',
                'description': 'A smooth solid-wood tray that keeps keys, jewelry, and everyday pocket things in one place.',
                'price': '999.00', 'stock': 22, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Tech & Audio', 'name': 'Everyday Wireless Earbuds', 'slug': 'everyday-wireless-earbuds',
                'description': 'Lightweight wireless earbuds with a pocket charging case and clear sound for calls and commutes.',
                'price': '2499.00', 'stock': 25, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Tech & Audio', 'name': 'Quiet Desk Wireless Mouse', 'slug': 'quiet-desk-wireless-mouse',
                'description': 'A comfortable, quiet-click wireless mouse with simple plug-and-play setup for work or study.',
                'price': '1199.00', 'stock': 31, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1527814050087-3793815479db?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Tech & Audio', 'name': 'Foldable Laptop Stand', 'slug': 'foldable-laptop-stand',
                'description': 'A sturdy adjustable stand that lifts your laptop for a more comfortable desk setup and folds flat for travel.',
                'price': '1799.00', 'stock': 17, 'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Style & Carry', 'name': 'Trailside Insulated Bottle', 'slug': 'trailside-insulated-bottle',
                'description': 'A double-wall stainless bottle that keeps drinks cold on the move and fits neatly in a day bag.',
                'price': '999.00', 'stock': 34, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Style & Carry', 'name': 'Weekender Zip Pouch', 'slug': 'weekender-zip-pouch',
                'description': 'A durable cotton zip pouch for travel essentials, chargers, stationery, or everyday bag organization.',
                'price': '549.00', 'stock': 40, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Style & Carry', 'name': 'Classic Everyday Sunglasses', 'slug': 'classic-everyday-sunglasses',
                'description': 'An easy-to-wear lightweight frame with UV-protective lenses for bright commutes and weekends out.',
                'price': '1499.00', 'stock': 21, 'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Kitchen & Table', 'name': 'Stackable Stoneware Mug', 'slug': 'stackable-stoneware-mug',
                'description': 'A comfortable everyday stoneware mug with a speckled glaze and a shape that stacks neatly in the cupboard.',
                'price': '499.00', 'stock': 42, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Kitchen & Table', 'name': 'Weekend Acacia Serving Board', 'slug': 'weekend-acacia-serving-board',
                'description': 'A warm-grain acacia board for serving breads, snacks, and easy weekend spreads.',
                'price': '1399.00', 'stock': 15, 'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Kitchen & Table', 'name': 'Clear Pantry Jar Set', 'slug': 'clear-pantry-jar-set',
                'description': 'A set of three clear storage jars to keep pantry staples visible, fresh, and easy to reach.',
                'price': '1099.00', 'stock': 23, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1603199506016-b9a594b593c0?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Home & Living', 'name': 'Linen Table Runner', 'slug': 'linen-table-runner',
                'description': 'A relaxed woven linen runner that brings a soft, natural finish to everyday meals and gatherings.',
                'price': '1299.00', 'stock': 16, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Home & Living', 'name': 'Ribbed Glass Vase', 'slug': 'ribbed-glass-vase',
                'description': 'A clear ribbed glass vase with a simple silhouette for fresh stems or a quiet shelf accent.',
                'price': '849.00', 'stock': 20, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1578500494198-246f612d3b3d?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Home & Living', 'name': 'Woven Storage Basket', 'slug': 'woven-storage-basket',
                'description': 'A sturdy woven basket for blankets, toys, or the everyday things that deserve a tidy home.',
                'price': '1599.00', 'stock': 13, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1595541242835-4d5d2c3a8e3f?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Home & Living', 'name': 'Rechargeable Table Light', 'slug': 'rechargeable-table-light',
                'description': 'A portable rechargeable lamp for warm, cordless light at the desk, bedside, or dinner table.',
                'price': '2199.00', 'stock': 12, 'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Home & Living', 'name': 'Cotton Hand Towel Set', 'slug': 'cotton-hand-towel-set',
                'description': 'A pair of absorbent cotton hand towels with a soft texture for the bathroom or kitchen.',
                'price': '699.00', 'stock': 32, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1620626011761-996317b8d101?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Tech & Audio', 'name': 'USB-C Fast Charger', 'slug': 'usb-c-fast-charger',
                'description': 'A compact USB-C wall charger for keeping phones, tablets, and other daily devices powered.',
                'price': '899.00', 'stock': 38, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Tech & Audio', 'name': 'Braided USB-C Cable', 'slug': 'braided-usb-c-cable',
                'description': 'A durable braided charging cable with a flexible finish for home, office, and travel bags.',
                'price': '399.00', 'stock': 55, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Tech & Audio', 'name': 'Compact Power Bank', 'slug': 'compact-power-bank',
                'description': 'A pocket-friendly backup battery to keep your everyday devices charged while away from a socket.',
                'price': '1899.00', 'stock': 19, 'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Tech & Audio', 'name': 'Adjustable Phone Stand', 'slug': 'adjustable-phone-stand',
                'description': 'A folding adjustable stand that keeps your phone at a comfortable angle for calls and watching.',
                'price': '649.00', 'stock': 29, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1586953208448-b95a79798f07?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Tech & Audio', 'name': 'Desk LED Light Bar', 'slug': 'desk-led-light-bar',
                'description': 'A slim adjustable LED light for focused desk work, late-night reading, and study sessions.',
                'price': '1599.00', 'stock': 15, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Style & Carry', 'name': 'Compact Travel Wallet', 'slug': 'compact-travel-wallet',
                'description': 'A slim travel wallet with room for cards, folded notes, and the small essentials for a day out.',
                'price': '899.00', 'stock': 24, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Style & Carry', 'name': 'Everyday Crossbody Bag', 'slug': 'everyday-crossbody-bag',
                'description': 'A lightweight crossbody bag with practical pockets for daily errands and easy hands-free carrying.',
                'price': '1899.00', 'stock': 18, 'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Style & Carry', 'name': 'Ribbed Knit Beanie', 'slug': 'ribbed-knit-beanie',
                'description': 'A soft ribbed knit beanie with a comfortable everyday fit for cool mornings and weekend walks.',
                'price': '699.00', 'stock': 27, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1576871337622-98d48d1cf531?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Style & Carry', 'name': 'Minimal Card Holder', 'slug': 'minimal-card-holder',
                'description': 'A compact card holder with a slim profile for carrying the cards you reach for every day.',
                'price': '549.00', 'stock': 35, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Style & Carry', 'name': 'Packable Day Backpack', 'slug': 'packable-day-backpack',
                'description': 'A light day backpack with a useful main compartment and a packable shape for commutes and day trips.',
                'price': '2299.00', 'stock': 14, 'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Kitchen & Table', 'name': 'Double-Wall Tea Glasses', 'slug': 'double-wall-tea-glasses',
                'description': 'A set of two double-wall glasses that keep tea warm while staying comfortable to hold.',
                'price': '899.00', 'stock': 22, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Kitchen & Table', 'name': 'Maple Cooking Spoon Set', 'slug': 'maple-cooking-spoon-set',
                'description': 'A useful set of smooth maple cooking spoons for stirring, serving, and everyday meal prep.',
                'price': '599.00', 'stock': 26, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Kitchen & Table', 'name': 'Cotton Kitchen Apron', 'slug': 'cotton-kitchen-apron',
                'description': 'A comfortable cotton apron with an adjustable neck strap and roomy front pocket for cooking days.',
                'price': '799.00', 'stock': 18, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Kitchen & Table', 'name': 'Stainless Spice Tin Set', 'slug': 'stainless-spice-tin-set',
                'description': 'A set of four lidded stainless tins to keep frequently used spices close at hand and neatly stored.',
                'price': '1099.00', 'stock': 20, 'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=900&q=80',
            },
            {
                'category': 'Kitchen & Table', 'name': 'Linen Dinner Napkin Set', 'slug': 'linen-dinner-napkin-set',
                'description': 'A set of four reusable linen-blend dinner napkins for everyday tables and relaxed hosting.',
                'price': '749.00', 'stock': 24, 'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=900&q=80',
            },
        ]
        for item in catalog:
            category, _ = Category.objects.get_or_create(name=item['category'])
            Product.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'category': category,
                    'name': item['name'],
                    'description': item['description'],
                    'price': item['price'],
                    'stock': item['stock'],
                    'featured': item['featured'],
                    'image_url': item['image_url'],
                    'available': True,
                },
            )
        self.stdout.write(self.style.SUCCESS(f'Loaded {len(catalog)} Pexo Market sample products.'))