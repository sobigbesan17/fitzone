import tkinter as tk

class GymMainMenu:
    def __init__(self, title, icon=None, function=None):
        self.title = title
        self.icon = icon
        self.function = function
        self.submenu = []

    def addSubMenu(self, subitem):
        self.submenu.append(subitem)

    def has_subitems(self):
        return bool(self.submenu)


class GymUserDropdownMenu(tk.Frame):
    def __init__(self, parent, root_menu, **kwargs):
        super().__init__(parent, **kwargs)
        self.root_menu = root_menu
        self.buttons = []
        self._build_menu(self.root_menu, self)

    def _build_menu(self, menu_item, container):
        for sub in menu_item.submenu:
            btn = tk.Button(
                container,
                text=f"{sub.icon + ' ' if sub.icon else ''}{sub.title}",
                anchor="w",
                relief="flat",
                command=sub.function if sub.function else None
            )
            btn.pack(fill="x", padx=4, pady=2)
            self.buttons.append(btn)

            if sub.has_subitems():
                frame = tk.Frame(container)
                frame.pack(fill="x", padx=12)
                self._build_menu(sub, frame)


def create_menu_section():
    def p(msg): print(msg)

    home = GymMainMenu("Home", icon="⌂")

    about_us = GymMainMenu("About Us", function=lambda: p("About Us clicked"))
    mission = GymMainMenu("Mission", function=lambda: p("Mission clicked"))
    mission.addSubMenu(GymMainMenu("Staff & Team", function=lambda: p("Staff & Team clicked")))
    mission.addSubMenu(GymMainMenu("Testimonials", function=lambda: p("Testimonials clicked")))
    about_us.addSubMenu(mission)
    home.addSubMenu(about_us)

    services = GymMainMenu("Services", icon="⚛")
    training_program = GymMainMenu("Training Program")
    personal_training = GymMainMenu("Personal Training")
    personal_training.addSubMenu(GymMainMenu("Personal Trainer", function=lambda: p("Personal Trainer clicked")))
    personal_training.addSubMenu(GymMainMenu("Training Activities", function=lambda: p("Training Activities clicked")))
    personal_training.addSubMenu(GymMainMenu("Trainer Request", function=lambda: p("Trainer Request clicked")))
    training_program.addSubMenu(personal_training)
    services.addSubMenu(training_program)
    services.addSubMenu(GymMainMenu("Group Fitness Class", function=lambda: p("Group Fitness Class clicked")))
    services.addSubMenu(GymMainMenu("Sports Training", function=lambda: p("Sports Training clicked")))
    services.addSubMenu(GymMainMenu("Yoga and Pilates", function=lambda: p("Yoga and Pilates clicked")))
    services.addSubMenu(GymMainMenu("Nutrition Consultation", function=lambda: p("Nutrition Consultation clicked")))
    home.addSubMenu(services)

    membership = GymMainMenu("Membership", icon="♥")
    membership.addSubMenu(GymMainMenu("Membership Plan", function=lambda: p("Membership Plan clicked")))
    membership.addSubMenu(GymMainMenu("Membership Benefits", function=lambda: p("Membership Benefits clicked")))
    membership.addSubMenu(GymMainMenu("How To Join", function=lambda: p("How To Join clicked")))
    home.addSubMenu(membership)

    fitness_classes = GymMainMenu("Fitness Classes", icon="♪")
    fitness_classes.addSubMenu(GymMainMenu("Schedule", function=lambda: p("Schedule clicked")))
    fitness_classes.addSubMenu(GymMainMenu("Class Description", function=lambda: p("Class Description clicked")))
    fitness_classes.addSubMenu(GymMainMenu("Booking Class", function=lambda: p("Booking Class clicked")))
    home.addSubMenu(fitness_classes)

    amenities = GymMainMenu("Fitness Amenities", icon="♣")
    amenities.addSubMenu(GymMainMenu("Gym Equipment", function=lambda: p("Gym Equipment clicked")))
    amenities.addSubMenu(GymMainMenu("Cardio Machine", function=lambda: p("Cardio Machine clicked")))
    amenities.addSubMenu(GymMainMenu("Pool", function=lambda: p("Pool clicked")))
    amenities.addSubMenu(GymMainMenu("Sauna/Steam Room", function=lambda: p("Sauna/Steam Room clicked")))
    amenities.addSubMenu(GymMainMenu("Other Amenities", function=lambda: p("Other Amenities clicked")))
    home.addSubMenu(amenities)

    blogs = GymMainMenu("Blogs & Pages", icon="✎")
    all_blogs = GymMainMenu("All Blogs")
    blogs.addSubMenu(GymMainMenu("Meals Page", function=lambda: p("Meals Page clicked")))
    blogs.addSubMenu(GymMainMenu("Workouts Page", function=lambda: p("Workouts Page clicked")))
    blogs.addSubMenu(all_blogs)
    home.addSubMenu(blogs)

    all_blogs.addSubMenu(GymMainMenu("Home Workout", function=lambda: p("Home Workout clicked")))
    all_blogs.addSubMenu(GymMainMenu("Sports Improvement", function=lambda: p("Sports Improvement clicked")))
    all_blogs.addSubMenu(GymMainMenu("Exercise Routines", function=lambda: p("Exercise Routines clicked")))
    all_blogs.addSubMenu(GymMainMenu("Body Workout", function=lambda: p("Body Workout clicked")))
    all_blogs.addSubMenu(GymMainMenu("Beginner's Guide", function=lambda: p("Beginner's Guide clicked")))
    all_blogs.addSubMenu(GymMainMenu("Elderly Guide", function=lambda: p("Elderly Guide clicked")))
    all_blogs.addSubMenu(GymMainMenu("Women Workout", function=lambda: p("Women Workout clicked")))
    all_blogs.addSubMenu(GymMainMenu("Gym Latest Updates", function=lambda: p("Gym Latest Updates clicked")))

    contact = GymMainMenu("Contact Us", icon="✆")
    contact.addSubMenu(GymMainMenu("FAQs", function=lambda: p("FAQs clicked")))
    contact.addSubMenu(GymMainMenu("Membership Info", function=lambda: p("Membership Info clicked")))
    contact.addSubMenu(GymMainMenu("Contact Details", function=lambda: p("Contact Details clicked")))
    contact.addSubMenu(GymMainMenu("Social Media", function=lambda: p("Social Media clicked")))
    contact.addSubMenu(GymMainMenu("Reviews & Ratings", function=lambda: p("Reviews & Ratings clicked")))
    contact.addSubMenu(GymMainMenu("Contact Form", function=lambda: p("Contact Form clicked")))
    home.addSubMenu(contact)

    return home
