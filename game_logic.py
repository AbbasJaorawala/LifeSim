import random
from enum import Enum
from datetime import datetime

# Enums
class EducationLevel(Enum):
    NONE = 0
    HIGH_SCHOOL = 1
    COLLEGE = 2
    GRADUATE = 3

    def __str__(self):
        return self.name

class SocioEconomicClass(Enum):
    POOR = 1
    MIDDLE = 2
    WEALTHY = 3

    def __str__(self):
        return self.name

class Nationality(Enum):
    AMERICAN = "American"
    BRITISH = "British"
    CHINESE = "Chinese"
    INDIAN = "Indian"
    BRAZILIAN = "Brazilian"
    NIGERIAN = "Nigerian"
    JAPANESE = "Japanese"
    GERMAN = "German"

    def __str__(self):
        return self.value

class Religion(Enum):
    CHRISTIANITY = "Christianity"
    ISLAM = "Islam"
    HINDUISM = "Hinduism"
    BUDDHISM = "Buddhism"
    JUDAISM = "Judaism"
    SIKHISM = "Sikhism"
    NONE = "None"

    def __str__(self):
        return self.value

# Person class
class Person:
    def __init__(self, first_name, last_name, gender, birth_year, family_wealth=50000, family_education=EducationLevel.HIGH_SCHOOL, nationality=Nationality.AMERICAN, religion=Religion.NONE, health=80, intelligence=60):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birth_year = birth_year
        self.age = 0
        self.is_alive = True
        self.health = health
        self.happiness = 50
        self.intelligence = intelligence
        self.charisma = 50
        self.wealth = family_wealth * 0.2
        self.education = None
        self.job = None
        self.salary = 0
        self.spouse = None
        self.children = []
        self.family_wealth = family_wealth
        self.family_education = family_education
        self.nationality = nationality
        self.religion = religion
        self.is_married = False  # Track marriage status

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'birth_year': self.birth_year,
            'age': self.age,
            'is_alive': self.is_alive,
            'health': self.health,
            'happiness': self.happiness,
            'intelligence': self.intelligence,
            'charisma': self.charisma,
            'wealth': self.wealth,
            'education': str(self.education) if self.education else None,
            'job': self.job,
            'salary': self.salary,
            'spouse': self.spouse.to_dict() if self.spouse else None,
            'children': [child.to_dict() for child in self.children],
            'family_wealth': self.family_wealth,
            'family_education': str(self.family_education),
            'nationality': str(self.nationality),
            'religion': str(self.religion),
            'is_married': self.is_married
        }

    @classmethod
    def from_dict(cls, data):
        nationality_map = {str(n): n for n in Nationality}
        religion_map = {str(r): r for r in Religion}
        person = cls(
            first_name=data['first_name'],
            last_name=data['last_name'],
            gender=data['gender'],
            birth_year=data['birth_year'],
            family_wealth=data['family_wealth'],
            family_education=EducationLevel[data['family_education']] if data['family_education'] else EducationLevel.HIGH_SCHOOL,
            nationality=nationality_map.get(data.get('nationality', 'American'), Nationality.AMERICAN),
            religion=religion_map.get(data.get('religion', 'None'), Religion.NONE),
            health=data.get('health', random.randint(50, 90)),
            intelligence=data.get('intelligence', random.randint(40, 80))
        )
        person.age = data['age']
        person.is_alive = data['is_alive']
        person.happiness = data['happiness']
        person.charisma = data['charisma']
        person.wealth = data['wealth']
        if data['education']:
            person.education = EducationLevel[data['education']]
        person.job = data['job']
        person.salary = data['salary']
        if data['spouse']:
            person.spouse = cls.from_dict(data['spouse'])
        person.children = [cls.from_dict(child) for child in data.get('children', [])]
        person.is_married = data.get('is_married', False)
        return person

# LifeSimulator class
class LifeSimulator:
    def __init__(self):
        self.current_year = datetime.now().year - random.randint(0, 30)
        self.player = None
        self.game_active = True
        self.generation = 1
        self.game_speed = 1
        self.paused = True
        self.current_event = None
        self.notifications = []
        self.achievements = []
        self.family_assets = 0
        self.next_gen_name = None

    def get_currency(self):
        currency_map = {
            Nationality.AMERICAN: ("USD", "$"),
            Nationality.BRITISH: ("GBP", "£"),
            Nationality.CHINESE: ("CNY", "¥"),
            Nationality.INDIAN: ("INR", "₹"),
            Nationality.BRAZILIAN: ("BRL", "R$"),
            Nationality.NIGERIAN: ("NGN", "₦"),
            Nationality.JAPANESE: ("JPY", "¥"),
            Nationality.GERMAN: ("EUR", "€")
        }
        return currency_map[self.player.nationality] if self.player else ("USD", "$")

    def create_character(self, first_name, last_name, gender, socio_class=SocioEconomicClass.MIDDLE, nationality=Nationality.AMERICAN, religion=Religion.NONE):
        wealth_map = {
            SocioEconomicClass.POOR: random.randint(0, 20000),
            SocioEconomicClass.MIDDLE: random.randint(30000, 80000),
            SocioEconomicClass.WEALTHY: random.randint(100000, 500000)
        }
        education_map = {
            SocioEconomicClass.POOR: EducationLevel.NONE,
            SocioEconomicClass.MIDDLE: EducationLevel.HIGH_SCHOOL,
            SocioEconomicClass.WEALTHY: random.choice([EducationLevel.HIGH_SCHOOL, EducationLevel.COLLEGE])
        }
        self.family_assets = wealth_map[socio_class]
        self.player = Person(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            birth_year=self.current_year,
            family_wealth=self.family_assets,
            family_education=education_map[socio_class],
            nationality=nationality,
            religion=religion,
            health=random.randint(50, 90),
            intelligence=random.randint(40, 80)
        )
        self.add_notification(f"A new baby named {self.player.full_name()} is born!")
        self.current_event = {
            'title': "New Life Begins",
            'description': self.generate_birth_description(),
            'choices': [
                {'text': "Begin Life Journey", 'action': 'start_life'}
            ]
        }

    def generate_birth_description(self):
        if not self.player:
            return "No character created"
        class_desc = {
            SocioEconomicClass.POOR: "A struggling family with limited resources",
            SocioEconomicClass.MIDDLE: "A stable middle-class family",
            SocioEconomicClass.WEALTHY: "An affluent family with many opportunities"
        }
        socio_class = self.determine_socio_class()
        currency_code, currency_symbol = self.get_currency()
        return "\n".join([
            f"{self.player.full_name()} is born into the {self.player.last_name} family.",
            f"Birth year: {self.current_year}",
            f"Nationality: {self.player.nationality}",
            f"Religion: {self.player.religion}",
            "",
            "Family Background:",
            f"- {class_desc[socio_class]}",
            f"- Family wealth: {currency_symbol}{self.player.family_wealth:,} {currency_code}"
        ])

    def determine_socio_class(self):
        if self.player.family_wealth < 20000:
            return SocioEconomicClass.POOR
        elif self.player.family_wealth < 100000:
            return SocioEconomicClass.MIDDLE
        else:
            return SocioEconomicClass.WEALTHY

    def add_notification(self, message):
        self.notifications.append(message)
        if len(self.notifications) > 10:
            self.notifications = self.notifications[-10:]

    def update(self):
        if not self.game_active or self.paused or not self.player:
            return
        self.current_year += 1
        self.player.age += 1
        self.update_stats()
        if not self.check_death():
            self.process_year_events()

    def update_stats(self):
        if not self.player:
            return
        socio_class = self.determine_socio_class()
        health_mod = {'POOR': -0.5, 'MIDDLE': 0, 'WEALTHY': 0.5}
        wealth_mod = {'POOR': 0.8, 'MIDDLE': 1.0, 'WEALTHY': 1.2}

        if self.player.age < 20:
            self.player.intelligence = min(100, self.player.intelligence + 0.5)
            self.player.health = min(100, self.player.health + 0.2 + health_mod[socio_class.name])
            self.player.charisma = min(100, self.player.charisma + 0.3)
        elif self.player.age > 40:
            self.player.health = max(0, self.player.health - 0.5 - health_mod[socio_class.name])
            if self.player.age > 60:
                self.player.health = max(0, self.player.health - 1 - health_mod[socio_class.name])

        # Retirement at 60
        if self.player.age >= 60 and self.player.job:
            self.add_notification(f"{self.player.first_name} has retired from {self.player.job}.")
            self.player.job = None
            self.player.salary = 0
            # Optional pension: small income based on wealth
            if self.player.wealth > 0:
                self.player.wealth += min(self.player.wealth * 0.02, 1000)  # Up to 1000/month pension

        if self.player.job:
            self.player.wealth += (self.player.salary / 12) * wealth_mod[socio_class.name]
            self.family_assets += (self.player.salary / 12) * 0.1
            if self.player.job == "Athlete":
                self.player.health = min(100, self.player.health + 0.5)
            elif self.player.job == "Actor":
                self.player.charisma = min(100, self.player.charisma + 0.3)
            elif self.player.job == "Politician":
                self.player.intelligence = min(100, self.player.intelligence + 0.2)
                self.player.charisma = min(100, self.player.charisma + 0.2)

    def check_death(self):
        if not self.player:
            return False
        # Death guaranteed at age 100
        if self.player.age >= 100:
            self.player.is_alive = False
            self.handle_death()
            return True
        # Death possible if health < 20 and age >= 20
        if self.player.health < 20 and self.player.age >= 20:
            death_chance = (20 - self.player.health) * 0.01 + (self.player.age - 20) * 0.005
            socio_mod = {'POOR': 1.2, 'MIDDLE': 1.0, 'WEALTHY': 0.8}[self.determine_socio_class().name]
            if random.random() < death_chance * socio_mod:
                self.player.is_alive = False
                self.handle_death()
                return True
        return False

    def process_year_events(self):
        if not self.player:
            return
        age = self.player.age
        if age == 1:
            self.add_notification(f"{self.player.first_name} takes first steps!")
        elif age == 5:
            self.add_notification(f"{self.player.first_name} starts kindergarten!")
        elif age == 18:
            self.coming_of_age_event()
        elif age >= 20 and age <= 50 and random.random() < 0.1 and not self.player.spouse:
            self.relationship_event()
        elif age >= 20 and age <= 50 and random.random() < 0.1 and self.player.spouse and not self.player.is_married:
            self.marriage_event()
        elif age >= 22 and age <= 45 and random.random() < 0.05 and self.player.is_married:
            if self.player.gender == "Female" and self.player.spouse.gender == "Male":
                self.pregnancy_event()
            else:
                self.child_event()
        elif age >= 20 and age < 60 and random.random() < 0.1 and not self.player.job:
            self.job_event()
        elif age >= 25 and age < 60 and random.random() < 0.05:
            self.adoption_event()
        elif age >= 18 and random.random() < 0.03:
            self.gender_reassignment_event()
        elif age >= 25 and random.random() < 0.04:
            self.nationality_change_event()
        elif age >= 20 and random.random() < 0.04:
            self.religion_change_event()
        elif age >= 30 and age < 60 and random.random() < 0.06 and self.player.job:
            self.career_change_event()

    def coming_of_age_event(self):
        currency_code, currency_symbol = self.get_currency()
        options = [
            {'text': f"Work as Waiter ({currency_symbol}500/month)", 'action': 'job_waiter'},
            {'text': f"Work as Gardener ({currency_symbol}600/month)", 'action': 'job_gardener'},
            {'text': f"Work as Maid ({currency_symbol}550/month)", 'action': 'job_maid'},
            {'text': f"Work as Cashier ({currency_symbol}700/month)", 'action': 'job_cashier'}
        ]
        socio_class = self.determine_socio_class()
        if (self.player.intelligence >= 60 or self.player.wealth >= 20000) and socio_class != SocioEconomicClass.POOR and self.player.wealth >= 20000:
            options.append({'text': f"Go to College (-{currency_symbol}20,000)", 'action': 'college'})
        if self.player.wealth >= 10000 and socio_class == SocioEconomicClass.WEALTHY:
            options.append({'text': f"Travel the World (-{currency_symbol}10,000)", 'action': 'travel'})
        self.current_event = {
            'title': "Coming of Age",
            'description': f"{self.player.first_name} is now 18. What path will they choose?",
            'choices': options
        }

    def relationship_event(self):
        partner = self.generate_person(age=self.player.age + random.randint(-5, 5))
        compatibility = random.randint(30, 90)
        self.current_event = {
            'title': "Relationship Opportunity",
            'description': (
                f"{self.player.first_name} meets {partner.full_name()} at a {random.choice(['party', 'work', 'school'])}.\n"
                f"Shared interests: {random.choice(['music', 'art', 'sports'])}\n"
                f"Initial attraction: {compatibility}%"
            ),
            'choices': [
                {'text': f"Date {partner.first_name} ({compatibility}% match)", 'action': 'date'},
                {'text': "Remain single", 'action': 'single'}
            ]
        }

    def marriage_event(self):
        self.current_event = {
            'title': "Marriage Proposal",
            'description': f"{self.player.first_name} and {self.player.spouse.full_name()} are considering marriage.",
            'choices': [
                {'text': "Get married", 'action': 'marry'},
                {'text': "Stay unmarried", 'action': 'decline'}
            ]
        }

    def pregnancy_event(self):
        currency_code, currency_symbol = self.get_currency()
        self.current_event = {
            'title': "Pregnancy Decision",
            'description': f"{self.player.first_name} is considering starting a family with {self.player.spouse.first_name}.",
            'choices': [
                {'text': f"Try for a baby (-{currency_symbol}5,000)", 'action': 'have_child'},
                {'text': "Wait for now", 'action': 'wait'}
            ]
        }

    def adoption_event(self):
        currency_code, currency_symbol = self.get_currency()
        self.current_event = {
            'title': "Adoption Opportunity",
            'description': f"{self.player.first_name} considers adopting a child.",
            'choices': [
                {'text': f"Adopt a child (-{currency_symbol}15,000)", 'action': 'adopt'},
                {'text': "Not now", 'action': 'decline'}
            ]
        }

    def gender_reassignment_event(self):
        new_gender = random.choice(["Female" if self.player.gender == "Male" else "Male", "Non-Binary"])
        currency_code, currency_symbol = self.get_currency()
        self.current_event = {
            'title': "Gender Reassignment",
            'description': f"{self.player.first_name} is considering identifying as {new_gender}.",
            'choices': [
                {'text': f"Proceed with reassignment (-{currency_symbol}10,000)", 'action': 'reassign'},
                {'text': "Stay as is", 'action': 'decline'}
            ]
        }

    def nationality_change_event(self):
        new_nationality = random.choice([n for n in Nationality if n != self.player.nationality])
        currency_code, currency_symbol = self.get_currency()
        self.current_event = {
            'title': "Immigration Opportunity",
            'description': f"{self.player.first_name} has a chance to move and adopt {new_nationality} nationality.",
            'choices': [
                {'text': f"Immigrate to become {new_nationality} (-{currency_symbol}25,000)", 'action': 'immigrate', 'nationality': str(new_nationality)},
                {'text': "Stay in current country", 'action': 'decline'}
            ]
        }

    def religion_change_event(self):
        new_religion = random.choice([r for r in Religion if r != self.player.religion])
        self.current_event = {
            'title': "Spiritual Journey",
            'description': f"{self.player.first_name} is exploring {new_religion} and considering conversion.",
            'choices': [
                {'text': f"Convert to {new_religion}", 'action': 'convert', 'religion': str(new_religion)},
                {'text': "Keep current beliefs", 'action': 'decline'}
            ]
        }

    def career_change_event(self):
        if not self.player.job:
            return
        currency_code, currency_symbol = self.get_currency()
        promotion_salary = int(self.player.salary * 1.5)
        self.current_event = {
            'title': "Career Decision",
            'description': f"{self.player.first_name} faces a pivotal moment at work as {self.player.job}.",
            'choices': [
                {'text': f"Take on extra responsibility (Chance of promotion to {currency_symbol}{promotion_salary}/month)", 'action': 'promotion_risk'},
                {'text': "Disagree with the boss (Risk of being fired)", 'action': 'firing_risk'},
                {'text': "Maintain current role", 'action': 'decline'}
            ]
        }

    def get_available_jobs(self):
        socio_class = self.determine_socio_class()
        jobs = {
            SocioEconomicClass.POOR: [
                ("Cleaner", 800),
                ("Laborer", 1000),
                ("Cashier", 1200)
            ],
            SocioEconomicClass.MIDDLE: [
                ("Teacher", 2000),
                ("Nurse", 2500),
                ("Salesperson", 3000)
            ],
            SocioEconomicClass.WEALTHY: [
                ("Lawyer", 5000),
                ("Doctor", 6000),
                ("Entrepreneur", 8000)
            ]
        }
        if self.player.charisma >= 70 and socio_class != SocioEconomicClass.POOR:
            jobs[socio_class].append(("Actor", 10000))
        if self.player.intelligence >= 80 and socio_class == SocioEconomicClass.WEALTHY:
            jobs[socio_class].append(("Politician", 12000))
        if self.player.health >= 70 and self.player.charisma >= 60:
            jobs[socio_class].append(("Athlete", 9000))
        return jobs[socio_class]

    def job_event(self):
        available_jobs = self.get_available_jobs()
        currency_code, currency_symbol = self.get_currency()
        self.current_event = {
            'title': "Job Opportunity",
            'description': f"{self.player.first_name} has a chance to start working.",
            'choices': [
                {'text': f"Work as {job} ({currency_symbol}{salary}/month)", 'action': f'job_{i}'}
                for i, (job, salary) in enumerate(available_jobs)
            ]
        }

    def generate_person(self, age=None):
        gender_options = ["Male", "Female", "Non-Binary"]
        gender = random.choice(gender_options)
        first_name = random.choice(["James", "John", "Mary", "Jennifer", "Alex", "Taylor"]) if not self.next_gen_name else self.next_gen_name
        last_name = random.choice(["Smith", "Johnson", "Williams"])
        nationality = random.choice(list(Nationality)) if not age else self.player.nationality
        religion = random.choice(list(Religion)) if not age else self.player.religion
        self.next_gen_name = None
        return Person(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            birth_year=self.current_year - (age if age else random.randint(18, 40)),
            family_wealth=self.family_assets * 0.5,
            family_education=self.player.family_education if self.player else EducationLevel.HIGH_SCHOOL,
            nationality=nationality,
            religion=religion,
            health=random.randint(50, 90),
            intelligence=random.randint(40, 80)
        )

    def child_event(self):
        currency_code, currency_symbol = self.get_currency()
        self.current_event = {
            'title': "Family Planning",
            'description': f"{self.player.first_name} and {self.player.spouse.first_name} consider having a child.",
            'choices': [
                {'text': f"Have a baby (-{currency_symbol}5,000)", 'action': 'have_child'},
                {'text': "Wait for now", 'action': 'wait'}
            ]
        }

    def handle_choice(self, choice_index):
        if not self.current_event or choice_index >= len(self.current_event['choices']):
            return
        choice = self.current_event['choices'][choice_index]
        action = choice['action']

        currency_code, currency_symbol = self.get_currency()

        if action == 'start_life':
            self.paused = False
            self.current_event = None
        elif action == 'college':
            if self.player.wealth >= 20000:
                self.player.education = EducationLevel.COLLEGE
                self.player.wealth -= 20000
                self.family_assets -= 20000
                self.add_notification(f"{self.player.first_name} enrolled in college!")
            else:
                self.add_notification(f"{self.player.first_name} cannot afford college.")
            self.current_event = None
        elif action.startswith('job_'):
            if action == 'job_waiter':
                self.player.job = "Waiter"
                self.player.salary = 500
            elif action == 'job_gardener':
                self.player.job = "Gardener"
                self.player.salary = 600
            elif action == 'job_maid':
                self.player.job = "Maid"
                self.player.salary = 550
            elif action == 'job_cashier':
                self.player.job = "Cashier"
                self.player.salary = 700
            else:
                job_index = int(action.split('_')[1])
                available_jobs = self.get_available_jobs()
                self.player.job = available_jobs[job_index][0]
                self.player.salary = available_jobs[job_index][1]
            self.add_notification(f"{self.player.first_name} started working as {self.player.job}!")
            self.current_event = None
        elif action == 'have_child':
            if self.player.wealth >= 5000:
                child = self.generate_person(age=0)
                self.player.children.append(child)
                self.player.wealth -= 5000
                self.family_assets -= 5000
                self.add_notification(f"{self.player.first_name} and {self.player.spouse.first_name} had a baby named {child.first_name}!")
            else:
                self.add_notification(f"{self.player.first_name} cannot afford to have a child.")
            self.current_event = None
        elif action == 'adopt':
            if self.player.wealth >= 15000:
                child = self.generate_person(age=random.randint(0, 10))
                self.player.children.append(child)
                self.player.wealth -= 15000
                self.family_assets -= 15000
                self.add_notification(f"{self.player.first_name} adopted {child.full_name()}!")
            else:
                self.add_notification(f"{self.player.first_name} cannot afford to adopt.")
            self.current_event = None
        elif action == 'reassign':
            if self.player.wealth >= 10000:
                new_gender = self.current_event['description'].split('as ')[-1].strip('.')
                self.player.gender = new_gender
                self.player.wealth -= 10000
                self.family_assets -= 10000
                self.add_notification(f"{self.player.first_name} transitioned to {new_gender}!")
            else:
                self.add_notification(f"{self.player.first_name} cannot afford gender reassignment.")
            self.current_event = None
        elif action == 'immigrate':
            if self.player.wealth >= 25000:
                nationality_map = {str(n): n for n in Nationality}
                self.player.nationality = nationality_map[choice.get('nationality')]
                self.player.wealth -= 25000
                self.family_assets -= 25000
                self.add_notification(f"{self.player.first_name} immigrated and is now {self.player.nationality}!")
            else:
                self.add_notification(f"{self.player.first_name} cannot afford to immigrate.")
            self.current_event = None
        elif action == 'convert':
            religion_map = {str(r): r for r in Religion}
            self.player.religion = religion_map[choice.get('religion')]
            self.add_notification(f"{self.player.first_name} converted to {self.player.religion}!")
            self.current_event = None
        elif action == 'date':
            partner = self.generate_person(age=self.player.age)
            self.player.spouse = partner
            self.add_notification(f"{self.player.first_name} is now dating {partner.full_name()}!")
            self.current_event = None
        elif action == 'marry':
            self.player.is_married = True
            self.player.spouse.is_married = True
            if self.player.gender == "Female" and self.player.spouse.gender == "Male":
                self.player.last_name = self.player.spouse.last_name
                self.add_notification(f"{self.player.first_name} married {self.player.spouse.full_name()} and took the last name {self.player.spouse.last_name}!")
            elif self.player.spouse.gender == "Female" and self.player.gender == "Male":
                self.player.spouse.last_name = self.player.last_name
                self.add_notification(f"{self.player.spouse.first_name} married {self.player.full_name()} and took the last name {self.player.last_name}!")
            else:
                self.add_notification(f"{self.player.first_name} married {self.player.spouse.full_name()}!")
            self.current_event = None
        elif action == 'new_life':
            self.__init__()
            self.current_event = None
            self.add_notification("Starting a new life...")
        elif action == 'next_gen_prompt':
            self.current_event = {
                'title': "Name Your Child",
                'description': "Choose a name for your next generation character.",
                'choices': [
                    {'text': "Enter name", 'action': 'next_gen_name'}
                ]
            }
            return
        elif action == 'next_gen_name':
            self.next_gen_name = self.current_event.get('new_name', "Child")
            if self.next_generation():
                self.current_event = None
        elif action == 'restart':
            self.create_character(
                first_name=random.choice(["James", "John", "Mary", "Jennifer", "Alex", "Taylor"]),
                last_name=self.player.last_name,
                gender=random.choice(["Male", "Female", "Non-Binary"]),
                socio_class=self.determine_socio_class(),
                nationality=self.player.nationality,
                religion=self.player.religion
            )
            self.generation = 1
            self.current_event = None
            self.paused = False
        elif action == 'promotion_risk':
            success_chance = (self.player.intelligence + self.player.charisma) / 200
            if random.random() < success_chance:
                self.player.salary = int(self.player.salary * 1.5)
                self.add_notification(f"{self.player.first_name} was promoted! New salary: {currency_symbol}{self.player.salary}/month")
            else:
                self.add_notification(f"{self.player.first_name}'s extra effort went unnoticed.")
            self.current_event = None
        elif action == 'firing_risk':
            failure_chance = (100 - self.player.charisma) / 100
            if random.random() < failure_chance:
                self.add_notification(f"{self.player.first_name} was fired from {self.player.job}!")
                self.player.job = None
                self.player.salary = 0
            else:
                self.add_notification(f"{self.player.first_name} avoided trouble with the boss.")
            self.current_event = None
        else:
            self.current_event = None

    def handle_death(self):
        currency_code, currency_symbol = self.get_currency()
        summary = [
            f"{self.player.full_name()} has died at age {self.player.age}.",
            f"Born: {self.player.birth_year}",
            f"Died: {self.current_year}",
            f"Nationality: {self.player.nationality}",
            f"Religion: {self.player.religion}",
            f"Family wealth accumulated: {currency_symbol}{self.family_assets:,} {currency_code}"
        ]
        if self.player.spouse:
            summary.append(f"Spouse: {self.player.spouse.full_name()}")
        if self.player.children:
            summary.append(f"Children: {len(self.player.children)}")
        if self.player.job:
            summary.append(f"Career: {self.player.job}")
        choices = [
            {'text': "Start New Life (New Family)", 'action': 'new_life'},
            {'text': "Restart with New Character (Same Family)", 'action': 'restart'}
        ]
        if self.player.children:
            choices.insert(0, {'text': "Continue as a Child (Choose Name)", 'action': 'next_gen_prompt'})
        self.current_event = {
            'title': "Life Complete",
            'description': "\n".join(summary),
            'choices': choices
        }
        self.paused = True

    def next_generation(self):
        if not self.player or not self.player.children:
            return False
        self.generation += 1
        self.player = random.choice(self.player.children)
        self.player.age = self.current_year - self.player.birth_year
        self.player.wealth = self.family_assets * 0.5
        self.family_assets *= 0.5
        self.add_notification(f"Now playing as {self.player.full_name()} (Generation {self.generation})")
        self.paused = False
        return True

    def to_dict(self):
        return {
            'current_year': self.current_year,
            'player': self.player.to_dict() if self.player else None,
            'generation': self.generation,
            'game_speed': self.game_speed,
            'paused': self.paused,
            'current_event': self.current_event,
            'notifications': self.notifications,
            'achievements': self.achievements,
            'game_active': self.game_active,
            'family_assets': self.family_assets,
            'next_gen_name': self.next_gen_name
        }

    @classmethod
    def from_dict(cls, data):
        game = cls()
        game.current_year = data.get('current_year', datetime.now().year - 20)
        game.generation = data.get('generation', 1)
        game.game_speed = data.get('game_speed', 1)
        game.paused = data.get('paused', True)
        game.notifications = data.get('notifications', [])
        game.achievements = data.get('achievements', [])
        game.game_active = data.get('game_active', True)
        game.family_assets = data.get('family_assets', 0)
        game.next_gen_name = data.get('next_gen_name')
        if data.get('player'):
            game.player = Person.from_dict(data['player'])
        game.current_event = data.get('current_event')
        return game