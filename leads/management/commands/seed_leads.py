from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from leads.models import Lead

class Command(BaseCommand):
    help = 'Seeds mock users and leads for demonstration purposes'

    def handle(self, *args, **options):
        self.stdout.write("Seeding data...")

        # 1. Create or get test users
        demo_user, created_demo = User.objects.get_or_create(username='demo')
        if created_demo:
            demo_user.set_password('password123')
            demo_user.email = 'demo@example.com'
            demo_user.save()
            self.stdout.write("Created user 'demo' with password 'password123'")
        else:
            self.stdout.write("User 'demo' already exists.")

        admin_user, created_admin = User.objects.get_or_create(username='admin', is_staff=True, is_superuser=True)
        if created_admin:
            admin_user.set_password('admin123')
            admin_user.email = 'admin@example.com'
            admin_user.save()
            self.stdout.write("Created superuser 'admin' with password 'admin123'")
        else:
            self.stdout.write("Superuser 'admin' already exists.")

        # 2. Clear existing leads for these users to ensure clean seeding
        Lead.objects.filter(owner__in=[demo_user, admin_user]).delete()
        self.stdout.write("Cleared existing leads for 'demo' and 'admin'")

        # 3. Mock data list
        demo_leads_data = [
            {
                'company_name': 'Acme Corporation',
                'contact_person': 'John Smith',
                'mobile_number': '+1-555-0199',
                'email': 'jsmith@acme.com',
                'location': 'New York, US',
                'lead_source': 'Web',
                'status': 'New',
                'notes': 'Submitted contact form asking about enterprise pricing plan.'
            },
            {
                'company_name': 'Global Tech Solutions',
                'contact_person': 'Sarah Jenkins',
                'mobile_number': '+44-20-7946-0958',
                'email': 'sjenkins@globaltech.co.uk',
                'location': 'London, UK',
                'lead_source': 'Referral',
                'status': 'In Progress',
                'notes': 'Referred by CEO. Interested in migration service.'
            },
            {
                'company_name': 'Apex Logistics',
                'contact_person': 'Carlos Mendoza',
                'mobile_number': '+52-55-1234-5678',
                'email': 'carlos.m@apexlogistics.mx',
                'location': 'Mexico City, MX',
                'lead_source': 'Cold Call',
                'status': 'Contacted',
                'notes': 'Called yesterday. carlos was friendly and requested a demo.'
            },
            {
                'company_name': 'Zenith Consulting',
                'contact_person': 'Kenji Tanaka',
                'mobile_number': '+81-3-5555-0143',
                'email': 'tanaka@zenith.jp',
                'location': 'Tokyo, JP',
                'lead_source': 'Social Media',
                'status': 'Closed Won',
                'notes': 'Deal closed! Contract signed for 1 year.'
            },
            {
                'company_name': 'Stellar Creative Agency',
                'contact_person': 'Chloe Dupont',
                'mobile_number': '+33-1-4227-7890',
                'email': 'chloe@stellaragency.fr',
                'location': 'Paris, FR',
                'lead_source': 'Email Campaign',
                'status': 'Closed Lost',
                'notes': 'Lost to competitor. Too high pricing.'
            },
            {
                'company_name': 'Nexus Retailers Ltd',
                'contact_person': 'David Brown',
                'mobile_number': '+1-415-555-2671',
                'email': 'dbrown@nexusretail.com',
                'location': 'San Francisco, US',
                'lead_source': 'Web',
                'status': 'New',
                'notes': 'Interested in e-commerce modules.'
            },
            {
                'company_name': 'Horizon Health Group',
                'contact_person': 'Emily Davis',
                'mobile_number': '+1-312-555-9122',
                'email': 'edavis@horizonhealth.org',
                'location': 'Chicago, US',
                'lead_source': 'Referral',
                'status': 'In Progress',
                'notes': 'Discussing compliance and HIPAA controls.'
            },
            {
                'company_name': 'Vanguard Finance',
                'contact_person': 'Oliver Schmidt',
                'mobile_number': '+49-69-123456',
                'email': 'o.schmidt@vanguard.de',
                'location': 'Frankfurt, DE',
                'lead_source': 'Cold Call',
                'status': 'Contacted',
                'notes': 'Invoiced sent for consulting workshop.'
            },
            {
                'company_name': 'Summit Industries',
                'contact_person': 'Robert Taylor',
                'mobile_number': '+61-2-9876-5432',
                'email': 'rtaylor@summitind.com.au',
                'location': 'Sydney, AU',
                'lead_source': 'Other',
                'status': 'Closed Won',
                'notes': 'Project kick-off scheduled next week.'
            },
            {
                'company_name': 'GreenTech Ventures',
                'contact_person': 'Anna Kowalski',
                'mobile_number': '+48-22-123-4567',
                'email': 'a.kowalski@greentech.pl',
                'location': 'Warsaw, PL',
                'lead_source': 'Social Media',
                'status': 'New',
                'notes': 'Follow up via LinkedIn.'
            }
        ]

        admin_leads_data = [
            {
                'company_name': 'Admin Exclusive Inc',
                'contact_person': 'Alice Cooper',
                'mobile_number': '+1-800-555-0100',
                'email': 'cooper@admininc.com',
                'location': 'Boston, US',
                'lead_source': 'Web',
                'status': 'New',
                'notes': 'Strictly confidential admin lead.'
            },
            {
                'company_name': 'Superuser Group',
                'contact_person': 'Bob Ross',
                'mobile_number': '+1-900-555-4321',
                'email': 'bob@superuser.org',
                'location': 'Miami, US',
                'lead_source': 'Referral',
                'status': 'Closed Won',
                'notes': 'Priceless lead. Won immediately.'
            }
        ]

        # Seed leads
        for lead in demo_leads_data:
            Lead.objects.create(owner=demo_user, **lead)
        self.stdout.write(f"Seeded {len(demo_leads_data)} leads for user 'demo'")

        for lead in admin_leads_data:
            Lead.objects.create(owner=admin_user, **lead)
        self.stdout.write(f"Seeded {len(admin_leads_data)} leads for user 'admin'")

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
