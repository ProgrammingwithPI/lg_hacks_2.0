import customtkinter as ctk
import requests
import json
import time
import threading
import webbrowser
import random

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class NutritionPlannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🧬 DNA Buddy - Personalized Nutrition")
        self.geometry("1000x800")
        
        # API KEY - Get free key from https://console.groq.com
        self.GROQ_API_KEY = ""  # REPLACE THIS WITH YOUR OWN KEY! (couldn't get .env in time for submission)
        
        # Data storage
        self.nutrition_goals = {}
        self.current_dishes = []
        self.selected_dish = None
        self.chat_history = []
        self.ai_personality = "friendly and supportive"
        
        # Animation variables
        self.stars = []
        self.scroll_offset = 0
        self.animation_running = False
        
        # Show hero page first
        self.show_hero_page()
    
    def show_hero_page(self):
        """Display hero landing page with animations"""
        # Clear window
        for widget in self.winfo_children():
            widget.destroy()
        
        # Main hero container with gradient background
        hero_container = ctk.CTkFrame(self, fg_color=("#0a0a1f", "#0a0a1f"))
        hero_container.pack(fill="both", expand=True)
        
        # Top section with stars animation
        top_section = ctk.CTkFrame(
            hero_container, 
            height=350,
            fg_color="transparent"
        )
        top_section.pack(fill="x", pady=0)
        top_section.pack_propagate(False)
        
        # Create canvas for star animation
        self.star_canvas = ctk.CTkCanvas(
            top_section,
            bg="#0a0a1f",
            highlightthickness=0,
            height=350
        )
        self.star_canvas.pack(fill="both", expand=True)
        
        # Initialize stars
        self.init_stars()
        
        # Title with gradient effect (layered labels)
        title_frame = ctk.CTkFrame(top_section, fg_color="transparent")
        title_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Main title
        title_label = ctk.CTkLabel(
            title_frame,
            text="DNA BUDDY",
            font=ctk.CTkFont(size=72, weight="bold"),
            text_color=("#00ff88", "#00ff88")
        )
        title_label.pack(pady=10)
        
        # Subtitle with gradient colors
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Your Personalized Nutrition AI",
            font=ctk.CTkFont(size=24),
            text_color=("#88ddff", "#88ddff")
        )
        subtitle.pack(pady=5)
        
        # Tagline
        tagline = ctk.CTkLabel(
            title_frame,
            text="Science-backed meal planning • Tailored to your DNA • Powered by AI",
            font=ctk.CTkFont(size=14),
            text_color=("#aaaaaa", "#aaaaaa")
        )
        tagline.pack(pady=10)
        
        # Start button with hover effect
        start_btn = ctk.CTkButton(
            title_frame,
            text="Start Your Journey",
            command=self.start_app,
            height=60,
            width=300,
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color=("#00ff88", "#00cc66"),
            hover_color=("#00cc66", "#00aa55"),
            corner_radius=30
        )
        start_btn.pack(pady=20)
        
        # Bottom section - Static cards
        cards_section = ctk.CTkFrame(
            hero_container,
            fg_color=("#1a1a2e", "#1a1a2e"),
            corner_radius=20
        )
        cards_section.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Cards title
        cards_title = ctk.CTkLabel(
            cards_section,
            text="Why Health Matters",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#ffffff", "#ffffff")
        )
        cards_title.pack(pady=20)
        
        # Three cards in a row
        cards_container = ctk.CTkFrame(cards_section, fg_color="transparent")
        cards_container.pack(pady=20, padx=40, fill="both", expand=True)
        
        health_benefits = [
            {
                "title": "Live Longer & Stronger",
                "text": "Proper nutrition can add years to your life and improve your quality of life. Studies show that a balanced diet rich in whole foods reduces the risk of chronic diseases and helps you maintain vitality as you age."
            },
            {
                "title": "Boost Energy & Focus",
                "text": "What you eat directly impacts your energy levels and mental clarity. Nutrient-dense foods provide sustained energy throughout the day, improve cognitive function, and help you perform at your best in work and life."
            },
            {
                "title": "Strengthen Immunity",
                "text": "A well-balanced diet strengthens your immune system and helps your body fight off illness. Essential vitamins, minerals, and antioxidants from healthy foods support your body's natural defense mechanisms."
            }
        ]
        
        for i, benefit in enumerate(health_benefits):
            card = ctk.CTkFrame(
                cards_container,
                fg_color=("#2a2a3e", "#2a2a3e"),
                corner_radius=15,
                border_width=2,
                border_color=("#00ff88", "#00ff88")
            )
            card.grid(row=0, column=i, padx=15, pady=20, sticky="nsew")
            
            # Title
            title_label = ctk.CTkLabel(
                card,
                text=benefit['title'],
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=("#00ff88", "#00ff88"),
                wraplength=280,
                justify="center"
            )
            title_label.pack(pady=(25, 15), padx=15)
            
            # Description
            desc_label = ctk.CTkLabel(
                card,
                text=benefit['text'],
                font=ctk.CTkFont(size=13),
                text_color=("#cccccc", "#cccccc"),
                wraplength=280,
                justify="left"
            )
            desc_label.pack(pady=(0, 25), padx=15, fill="both", expand=True)
            
            cards_container.grid_columnconfigure(i, weight=1)
            cards_container.grid_rowconfigure(0, weight=1)
        
        # Start animations (only stars now)
        self.animation_running = True
        self.animate_stars()
    
    def init_stars(self):
        """Initialize star positions"""
        self.stars = []
        for _ in range(100):
            x = random.randint(0, 1000)
            y = random.randint(0, 350)
            size = random.randint(1, 3)
            speed = random.uniform(0.5, 2.0)
            self.stars.append({'x': x, 'y': y, 'size': size, 'speed': speed})
    
    def animate_stars(self):
        """Animate stars moving upward"""
        if not self.animation_running:
            return
        
        self.star_canvas.delete("all")
        
        for star in self.stars:
            color_intensity = random.randint(200, 255)
            color = f'#{color_intensity:02x}{color_intensity:02x}ff'
            
            self.star_canvas.create_oval(
                star['x'], star['y'],
                star['x'] + star['size'], star['y'] + star['size'],
                fill=color, outline=color
            )
            
            star['y'] -= star['speed']
            
            if star['y'] < 0:
                star['y'] = 350
                star['x'] = random.randint(0, 1000)
        
        self.after(50, self.animate_stars)
    
    def animate_cards(self):
        """Animate scrolling health cards with images"""
        if not self.animation_running:
            return
        
        self.cards_canvas.delete("all")
        
        card_width = 300
        card_height = 220
        spacing = 40
        total_width = len(self.health_cards) * (card_width + spacing)
        
        # Draw cards - they loop seamlessly
        for i, card in enumerate(self.health_cards):
            x = (i * (card_width + spacing) - self.scroll_offset) % total_width
            
            # Draw cards that are visible on screen
            if x > -card_width - spacing and x < 1000:
                # Card background
                self.cards_canvas.create_rectangle(
                    x, 20, x + card_width, 20 + card_height,
                    fill="#2a2a3e", outline="#00ff88", width=2
                )
                
                # Image placeholder (colored rectangle simulating image)
                # You can replace this with actual image loading using PIL
                image_colors = ["#ff6b6b", "#4ecdc4", "#ffe66d", "#95e1d3", "#a8e6cf", "#ffd3b6"]
                img_color = image_colors[i % 6]
                self.cards_canvas.create_rectangle(
                    x + 10, 30, x + card_width - 10, 30 + 120,
                    fill=img_color, outline=""
                )
                
                # White border for image
                self.cards_canvas.create_rectangle(
                    x + 10, 30, x + card_width - 10, 30 + 120,
                    fill="", outline="#ffffff", width=3
                )
                
                # Title
                self.cards_canvas.create_text(
                    x + card_width/2, 170,
                    text=card['title'],
                    font=("Arial", 16, "bold"),
                    fill="#ffffff"
                )
                
                # Description
                self.cards_canvas.create_text(
                    x + card_width/2, 205,
                    text=card['text'],
                    font=("Arial", 10),
                    fill="#aaaaaa",
                    width=card_width - 20
                )
        
        # Update scroll offset (slower for smoother scroll)
        self.scroll_offset += 2
        
        # Reset when one full cycle is complete
        if self.scroll_offset >= total_width / 3:
            self.scroll_offset = 0
        
        # Schedule next frame
        self.after(30, self.animate_cards)
    
    def start_app(self):
        """Start the main application"""
        self.animation_running = False
        
        for widget in self.winfo_children():
            widget.destroy()
        
        self.main_frame = ctk.CTkScrollableFrame(
            self, width=950, height=750, fg_color=("#0a0a1f", "#0a0a1f")
        )
        self.main_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        header_frame = ctk.CTkFrame(
            self.main_frame, fg_color=("#1a1a2e", "#1a1a2e"), corner_radius=15
        )
        header_frame.pack(pady=20, padx=20, fill="x")
        
        self.title_label = ctk.CTkLabel(
            header_frame, text="🧬 DNA BUDDY",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=("#00ff88", "#00ff88")
        )
        self.title_label.pack(pady=15)
        
        self.progress_frame = ctk.CTkFrame(
            self.main_frame, fg_color=("#1a1a2e", "#1a1a2e"), corner_radius=15
        )
        self.progress_frame.pack(pady=10, fill="x", padx=20)
        
        self.progress_labels = []
        progress_steps = ["1. Profile", "2. Goals", "3. Ingredients", "4. Dishes"]
        
        for i, step in enumerate(progress_steps):
            step_frame = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
            step_frame.grid(row=0, column=i, padx=5, pady=15, sticky="ew")
            
            label = ctk.CTkLabel(
                step_frame, text=step,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=("#666666", "#666666")
            )
            label.pack()
            
            self.progress_labels.append(label)
            self.progress_frame.grid_columnconfigure(i, weight=1)
        
        self.content_frame = ctk.CTkFrame(
            self.main_frame, fg_color=("#1a1a2e", "#1a1a2e"), corner_radius=15
        )
        self.content_frame.pack(pady=20, fill="both", expand=True, padx=20)
        
        self.show_step_1()
    
    def update_progress(self, step):
        """Update progress indicator"""
        for i, label in enumerate(self.progress_labels):
            if i < step:
                label.configure(text_color=("#00ff88", "#00ff88"))
            else:
                label.configure(text_color=("#666666", "#666666"))
    
    def clear_content(self):
        """Clear content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_loading(self, message):
        """Show loading spinner"""
        self.clear_content()
        
        loading_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        loading_frame.pack(expand=True)
        
        loading_label = ctk.CTkLabel(
            loading_frame, text=f"⏳ {message}",
            font=ctk.CTkFont(size=20), text_color=("#00ff88", "#00ff88")
        )
        loading_label.pack(pady=50)
        
        self.progress_bar = ctk.CTkProgressBar(
            loading_frame, mode="indeterminate",
            progress_color=("#00ff88", "#00ff88"), width=400
        )
        self.progress_bar.pack(pady=20)
        self.progress_bar.start()
    
    def show_step_1(self):
        """Step 1: DNA Profile Input"""
        self.clear_content()
        self.update_progress(1)
        
        section_frame = ctk.CTkFrame(
            self.content_frame, fg_color=("#2a2a3e", "#2a2a3e"), corner_radius=15
        )
        section_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        dna_label = ctk.CTkLabel(
            section_frame, text="📋 Enter Your Profile Information",
            font=ctk.CTkFont(size=20, weight="bold"), text_color=("#ffffff", "#ffffff")
        )
        dna_label.pack(pady=(30, 10))
        
        desc_label = ctk.CTkLabel(
            section_frame,
            text="Tell us about yourself - age, height, weight, activity level, dietary restrictions",
            font=ctk.CTkFont(size=12), text_color=("#aaaaaa", "#aaaaaa")
        )
        desc_label.pack(pady=5)
        
        self.dna_textbox = ctk.CTkTextbox(
            section_frame, height=150, border_width=2,
            border_color=("#00ff88", "#00ff88"), corner_radius=10
        )
        self.dna_textbox.pack(pady=15, padx=40, fill="x")
        self.dna_textbox.insert("1.0", "Age: 30, Height: 5'10\", Weight: 180lbs, Active lifestyle, No allergies")
        
        limit_label = ctk.CTkLabel(
            section_frame, text="(Maximum 500 characters)",
            font=ctk.CTkFont(size=10), text_color=("#666666", "#666666")
        )
        limit_label.pack(pady=(0, 10))
        
        goal_label = ctk.CTkLabel(
            section_frame, text="🎯 Select Your Fitness Goal",
            font=ctk.CTkFont(size=20, weight="bold"), text_color=("#ffffff", "#ffffff")
        )
        goal_label.pack(pady=(30, 10))
        
        self.goal_var = ctk.StringVar(value="weight loss")
        goal_options = ["weight loss", "muscle gain", "general health", "athletic performance", "maintenance"]
        
        self.goal_menu = ctk.CTkOptionMenu(
            section_frame, variable=self.goal_var, values=goal_options,
            width=400, height=45, font=ctk.CTkFont(size=14),
            fg_color=("#00ff88", "#00cc66"),
            button_color=("#00cc66", "#00aa55"),
            button_hover_color=("#00aa55", "#008844"),
            corner_radius=10
        )
        self.goal_menu.pack(pady=15)
        
        analyze_btn = ctk.CTkButton(
            section_frame, text="🧬 Analyze My Profile",
            command=self.analyze_dna, height=60, width=350,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=("#00ff88", "#00cc66"),
            hover_color=("#00cc66", "#00aa55"), corner_radius=30
        )
        analyze_btn.pack(pady=30)
    
    def analyze_dna(self):
        """Analyze DNA profile"""
        dna_text = self.dna_textbox.get("1.0", "end-1c").strip()
        
        if not dna_text or len(dna_text) < 10:
            self.show_error("Please enter your profile information")
            return
        
        if len(dna_text) > 500:
            self.show_error("Input too long. Using first 500 characters only.")
            dna_text = dna_text[:500]
        
        self.show_loading("Analyzing your profile with AI...")
        
        thread = threading.Thread(
            target=self._analyze_dna_thread,
            args=(dna_text, self.goal_var.get())
        )
        thread.daemon = True
        thread.start()
    
    def _analyze_dna_thread(self, dna_text, goal):
        """Thread for DNA analysis"""
        try:
            dna_text_limited = dna_text[:500]
            
            response = self.hackclub_ai(f"""DNA profile: {dna_text_limited}
Goal: {goal}

Create a nutrition plan with daily targets. Return ONLY JSON:
{{"calories": <number>, "protein": <number>, "carbs": <number>, "fats": <number>, "exercise_plan": "<brief plan>"}}""")
            
            if '{' in response and '}' in response:
                json_start = response.index('{')
                json_end = response.rindex('}') + 1
                json_str = response[json_start:json_end]
                recommendations = json.loads(json_str)
            else:
                recommendations = {
                    "calories": 2000, "protein": 150, "carbs": 200,
                    "fats": 65, "exercise_plan": "Regular exercise recommended"
                }
            
            self.nutrition_goals = {
                'calories': float(recommendations.get('calories', 2000)),
                'protein': float(recommendations.get('protein', 150)),
                'carbs': float(recommendations.get('carbs', 200)),
                'fats': float(recommendations.get('fats', 65)),
                'exercise_plan': recommendations.get('exercise_plan', 'Regular exercise recommended')
            }
            
            self.after(0, self.show_step_2)
            
        except Exception as e:
            self.after(0, lambda: self.show_error(f"Failed to analyze profile: {str(e)}"))
    
    def show_step_2(self):
        """Step 2: Display Goals"""
        self.clear_content()
        self.update_progress(2)
        
        goals_container = ctk.CTkFrame(
            self.content_frame, fg_color=("#2a2a3e", "#2a2a3e"), corner_radius=15
        )
        goals_container.pack(pady=20, padx=30, fill="x")
        
        goals_title = ctk.CTkLabel(
            goals_container, text="✨ Your Personalized Nutrition Plan",
            font=ctk.CTkFont(size=24, weight="bold"), text_color=("#00ff88", "#00ff88")
        )
        goals_title.pack(pady=20)
        
        cards_frame = ctk.CTkFrame(goals_container, fg_color="transparent")
        cards_frame.pack(pady=10, padx=20)
        
        goals_data = [
            ("🔥", "Calories", f"{int(self.nutrition_goals['calories'])} kcal/day"),
            ("🥩", "Protein", f"{int(self.nutrition_goals['protein'])}g/day"),
            ("🌾", "Carbs", f"{int(self.nutrition_goals['carbs'])}g/day"),
            ("🥑", "Fats", f"{int(self.nutrition_goals['fats'])}g/day")
        ]
        
        for i, (icon, label, value) in enumerate(goals_data):
            row = i // 2
            col = i % 2
            
            card = ctk.CTkFrame(
                cards_frame, fg_color=("#3a3a4e", "#3a3a4e"),
                corner_radius=12, border_width=2, border_color=("#00ff88", "#00ff88")
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            
            ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=32)).pack(pady=(15, 5))
            ctk.CTkLabel(
                card, text=label, font=ctk.CTkFont(size=14, weight="bold"),
                text_color=("#aaaaaa", "#aaaaaa")
            ).pack()
            ctk.CTkLabel(
                card, text=value, font=ctk.CTkFont(size=18, weight="bold"),
                text_color=("#ffffff", "#ffffff")
            ).pack(pady=(5, 15))
            
            cards_frame.grid_columnconfigure(col, weight=1)
        
        exercise_frame = ctk.CTkFrame(
            goals_container, fg_color=("#3a3a4e", "#3a3a4e"),
            corner_radius=12, border_width=2, border_color=("#00ff88", "#00ff88")
        )
        exercise_frame.pack(pady=15, padx=20, fill="x")
        
        ctk.CTkLabel(
            exercise_frame, text="💪 Exercise Plan",
            font=ctk.CTkFont(size=16, weight="bold"), text_color=("#00ff88", "#00ff88")
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            exercise_frame, text=self.nutrition_goals['exercise_plan'],
            font=ctk.CTkFont(size=13), text_color=("#ffffff", "#ffffff"), wraplength=700
        ).pack(pady=(5, 15), padx=20)
        
        ingredients_container = ctk.CTkFrame(
            self.content_frame, fg_color=("#2a2a3e", "#2a2a3e"), corner_radius=15
        )
        ingredients_container.pack(pady=20, padx=30, fill="both", expand=True)
        
        ingredients_label = ctk.CTkLabel(
            ingredients_container, text="🥗 What Ingredients Do You Have?",
            font=ctk.CTkFont(size=20, weight="bold"), text_color=("#ffffff", "#ffffff")
        )
        ingredients_label.pack(pady=(30, 10))
        
        desc_label = ctk.CTkLabel(
            ingredients_container, text="Enter ingredients separated by commas",
            font=ctk.CTkFont(size=12), text_color=("#aaaaaa", "#aaaaaa")
        )
        desc_label.pack(pady=5)
        
        self.ingredients_textbox = ctk.CTkTextbox(
            ingredients_container, height=100, border_width=2,
            border_color=("#00ff88", "#00ff88"), corner_radius=10
        )
        self.ingredients_textbox.pack(pady=15, padx=40, fill="x")
        self.ingredients_textbox.insert("1.0", "chicken, broccoli, rice, eggs, olive oil")
        
        limit_label = ctk.CTkLabel(
            ingredients_container, text="(First 10 ingredients will be used)",
            font=ctk.CTkFont(size=10), text_color=("#666666", "#666666")
        )
        limit_label.pack(pady=(0, 10))
        
        generate_btn = ctk.CTkButton(
            ingredients_container, text="🍳 Generate Meal Recommendations",
            command=self.generate_dishes, height=60, width=400,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=("#00ff88", "#00cc66"),
            hover_color=("#00cc66", "#00aa55"), corner_radius=30
        )
        generate_btn.pack(pady=30)
    
    def generate_dishes(self):
        """Generate dish recommendations"""
        ingredients_text = self.ingredients_textbox.get("1.0", "end-1c").strip()
        ingredients = [i.strip() for i in ingredients_text.split(',') if i.strip()]
        
        if not ingredients:
            self.show_error("Please enter at least one ingredient")
            return
        
        self.show_loading("Creating personalized meal recommendations...")
        
        thread = threading.Thread(target=self._generate_dishes_thread, args=(ingredients,))
        thread.daemon = True
        thread.start()
    
    def _generate_dishes_thread(self, ingredients):
        """Thread for dish generation"""
        try:
            meal_calories = self.nutrition_goals['calories'] / 3
            meal_protein = self.nutrition_goals['protein'] / 3
            meal_carbs = self.nutrition_goals['carbs'] / 3
            meal_fats = self.nutrition_goals['fats'] / 3

            ingredients_limited = ingredients[:10]

            prompt = f"""Generate 20 meal dishes using these ingredients: {', '.join(ingredients_limited)}.
Strictly follow this format for each dish (one per line):

DishNameWithoutColonsOrCommas: Calories, Protein (g), Carbs (g), Fats (g)

Example:
Grilled Chicken Salad: 400, 30, 20, 15
Quinoa Veggie Bowl: 350, 15, 50, 10
"""
            ai_response = self.hackclub_ai(prompt)

            dishes = []
            for line in ai_response.strip().split('\n'):
                if ':' not in line:
                    continue
                try:
                    name_part, nutrients_part = line.split(':', 1)
                    nutrients = [n.strip() for n in nutrients_part.split(',')]

                    if len(nutrients) != 4:
                        continue

                    dishes.append({
                        "name": name_part.strip(),
                        "description": "",
                        "calories": float(nutrients[0]),
                        "protein": float(nutrients[1]),
                        "carbs": float(nutrients[2]),
                        "fats": float(nutrients[3])
                    })
                except:
                    continue

            if not dishes:
                raise Exception("No valid dishes returned from AI.")

            goals = [meal_calories, meal_protein, meal_carbs, meal_fats]
            recipe_nutrients = [[d['calories'], d['protein'], d['carbs'], d['fats']] for d in dishes]

            scored = self.calculate_score(goals, recipe_nutrients)

            for idx, score in scored:
                dishes[idx]['score'] = round(score, 3)
                dishes[idx]['dish_id'] = idx

            dishes.sort(key=lambda x: x['score'], reverse=True)
            self.current_dishes = dishes

            self.after(0, self.show_step_3)

        except Exception as ex:
            self.after(0, lambda ex=ex: self.show_error(f"Failed to generate dishes: {ex}"))
    
    def show_step_3(self):
        """Step 3: Display Dishes"""
        self.clear_content()
        self.update_progress(4)
        
        header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header_frame.pack(pady=20)
        
        title = ctk.CTkLabel(
            header_frame, text="🍽️ Your Personalized Meal Options",
            font=ctk.CTkFont(size=26, weight="bold"), text_color=("#00ff88", "#00ff88")
        )
        title.pack(pady=10)
        
        subtitle = ctk.CTkLabel(
            header_frame, text="Click 'View Recipe' to see the full recipe on Google",
            font=ctk.CTkFont(size=14), text_color=("#aaaaaa", "#aaaaaa")
        )
        subtitle.pack(pady=5)
        
        dishes_frame = ctk.CTkScrollableFrame(
            self.content_frame, height=450, fg_color="transparent"
        )
        dishes_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        for i, dish in enumerate(self.current_dishes[:12]):
            dish_card = ctk.CTkFrame(
                dishes_frame, fg_color=("#2a2a3e", "#2a2a3e"),
                corner_radius=15, border_width=2,
                border_color=("#00ff88" if i < 3 else "#3a3a4e", "#00ff88" if i < 3 else "#3a3a4e")
            )
            dish_card.pack(pady=12, padx=10, fill="x")
            
            if i < 3:
                badge_frame = ctk.CTkFrame(
                    dish_card, fg_color=("#00ff88", "#00cc66"), corner_radius=8, height=30
                )
                badge_frame.pack(pady=(10, 5), padx=15, anchor="w")
                
                badge_labels = ["🥇 BEST MATCH", "🥈 GREAT CHOICE", "🥉 TOP PICK"]
                badge_label = ctk.CTkLabel(
                    badge_frame, text=badge_labels[i],
                    font=ctk.CTkFont(size=11, weight="bold"), text_color=("#000000", "#000000")
                )
                badge_label.pack(padx=10, pady=5)
            
            name_frame = ctk.CTkFrame(dish_card, fg_color="transparent")
            name_frame.pack(pady=(10 if i >= 3 else 5, 5), padx=15, fill="x")
            
            name_label = ctk.CTkLabel(
                name_frame, text=f"🍽️ {dish['name']}",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=("#ffffff", "#ffffff"), anchor="w"
            )
            name_label.pack(side="left")
            
            nutrients_frame = ctk.CTkFrame(dish_card, fg_color="transparent")
            nutrients_frame.pack(pady=10, padx=15, fill="x")
            
            nutrient_data = [
                ("🔥", f"{int(dish['calories'])}", "kcal", "#ff6b6b"),
                ("🥩", f"{int(dish['protein'])}", "g protein", "#4ecdc4"),
                ("🌾", f"{int(dish['carbs'])}", "g carbs", "#ffe66d"),
                ("🥑", f"{int(dish['fats'])}", "g fats", "#95e1d3")
            ]
            
            for icon, value, label, color in nutrient_data:
                nutrient_box = ctk.CTkFrame(
                    nutrients_frame, fg_color=("#3a3a4e", "#3a3a4e"), corner_radius=8
                )
                nutrient_box.pack(side="left", padx=5, pady=5)
                
                ctk.CTkLabel(
                    nutrient_box, text=f"{icon} {value}",
                    font=ctk.CTkFont(size=13, weight="bold"), text_color=(color, color)
                ).pack(padx=10, pady=3)
                
                ctk.CTkLabel(
                    nutrient_box, text=label,
                    font=ctk.CTkFont(size=9), text_color=("#aaaaaa", "#aaaaaa")
                ).pack(padx=10, pady=(0, 5))
            
            bottom_frame = ctk.CTkFrame(dish_card, fg_color="transparent")
            bottom_frame.pack(pady=15, padx=15, fill="x")
            
            score_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
            score_frame.pack(side="left", fill="x", expand=True)
            
            score_label = ctk.CTkLabel(
                score_frame, text=f"Match Score: {int(dish['score'] * 100)}%",
                font=ctk.CTkFont(size=13, weight="bold"), text_color=("#00ff88", "#00ff88")
            )
            score_label.pack(anchor="w")
            
            score_bar = ctk.CTkProgressBar(
                score_frame, width=200, height=8, progress_color=("#00ff88", "#00cc66")
            )
            score_bar.pack(anchor="w", pady=5)
            score_bar.set(dish['score'])
            
            view_btn = ctk.CTkButton(
                bottom_frame, text="View Recipe 🔍",
                command=lambda name=dish['name']: webbrowser.open(f"https://www.google.com/search?q={name.replace(' ', '+')}+recipe"),
                width=150, height=40, font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=("#00ff88", "#00cc66"),
                hover_color=("#00cc66", "#00aa55"), corner_radius=20
            )
            view_btn.pack(side="right")
        
        # Chat with DNA Buddy button
        chat_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        chat_frame.pack(pady=30)
        
        chat_btn = ctk.CTkButton(
            chat_frame,
            text="💬 Chat with DNA Buddy",
            command=self.show_chat_window,
            height=60,
            width=400,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=("#00ff88", "#00cc66"),
            hover_color=("#00cc66", "#00aa55"),
            corner_radius=30
        )
        chat_btn.pack()
    
    def show_chat_window(self):
        """Show chat window with AI personality options"""
        chat_window = ctk.CTkToplevel(self)
        chat_window.title("Chat with DNA Buddy")
        chat_window.geometry("900x700")
        chat_window.configure(fg_color=("#0a0a1f", "#0a0a1f"))
        
        # Main container
        main_container = ctk.CTkFrame(
            chat_window,
            fg_color=("#1a1a2e", "#1a1a2e"),
            corner_radius=15
        )
        main_container.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        title = ctk.CTkLabel(
            main_container,
            text="💬 Chat with DNA Buddy",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#00ff88", "#00ff88")
        )
        title.pack(pady=20)
        
        # Personality selector
        personality_frame = ctk.CTkFrame(
            main_container,
            fg_color=("#2a2a3e", "#2a2a3e"),
            corner_radius=12,
            border_width=2,
            border_color=("#00ff88", "#00ff88")
        )
        personality_frame.pack(pady=10, padx=30, fill="x")
        
        personality_label = ctk.CTkLabel(
            personality_frame,
            text="🎭 AI Personality Style",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#00ff88", "#00ff88")
        )
        personality_label.pack(pady=(15, 10))
        
        personality_options = [
            "friendly and supportive",
            "professional nutritionist",
            "enthusiastic fitness coach",
            "wise health mentor",
            "casual buddy",
            "pirate chef",
            "zen wellness guru",
            "scientific researcher"
        ]
        
        self.personality_var = ctk.StringVar(value=self.ai_personality)
        
        personality_menu = ctk.CTkOptionMenu(
            personality_frame,
            variable=self.personality_var,
            values=personality_options,
            width=500,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=("#3a3a4e", "#3a3a4e"),
            button_color=("#00cc66", "#00aa55"),
            button_hover_color=("#00aa55", "#008844"),
            command=self.update_personality
        )
        personality_menu.pack(pady=(0, 15), padx=20)
        
        # Chat history display
        self.chat_display = ctk.CTkTextbox(
            main_container,
            height=350,
            font=ctk.CTkFont(size=13),
            wrap="word",
            border_width=2,
            border_color=("#00ff88", "#00ff88")
        )
        self.chat_display.pack(pady=15, padx=30, fill="both", expand=True)
        self.chat_display.configure(state="disabled")
        
        # Display existing chat history
        self.refresh_chat_display()
        
        # Input frame
        input_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        input_frame.pack(pady=(10, 20), padx=30, fill="x")
        
        self.chat_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Ask me anything about nutrition, recipes, or health...",
            height=50,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color=("#00ff88", "#00ff88")
        )
        self.chat_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Bind Enter key
        self.chat_input.bind("<Return>", lambda e: self.send_chat_message(chat_window))
        
        send_btn = ctk.CTkButton(
            input_frame,
            text="Send",
            command=lambda: self.send_chat_message(chat_window),
            width=120,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#00ff88", "#00cc66"),
            hover_color=("#00cc66", "#00aa55"),
            corner_radius=25
        )
        send_btn.pack(side="right")
        
        # Clear chat button
        clear_btn = ctk.CTkButton(
            main_container,
            text="Clear Chat History",
            command=self.clear_chat,
            width=150,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color=("#ff6b6b", "#ff4444"),
            hover_color=("#ff4444", "#ff2222"),
            corner_radius=20
        )
        clear_btn.pack(pady=(0, 15))
    
    def update_personality(self, choice):
        """Update AI personality"""
        self.ai_personality = choice
    
    def refresh_chat_display(self):
        """Refresh the chat display with history"""
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        
        if not self.chat_history:
            self.chat_display.insert("end", "Welcome! Ask me anything about nutrition, recipes, or your meal plan.\n\n", "welcome")
            self.chat_display.tag_config("welcome", foreground="#aaaaaa")
        else:
            for message in self.chat_history:
                if message['role'] == 'user':
                    self.chat_display.insert("end", "You: ", "user_label")
                    self.chat_display.insert("end", f"{message['content']}\n\n", "user_text")
                else:
                    self.chat_display.insert("end", "DNA Buddy: ", "ai_label")
                    self.chat_display.insert("end", f"{message['content']}\n\n", "ai_text")
            
            self.chat_display.tag_config("user_label", foreground="#00ff88")
            self.chat_display.tag_config("user_text", foreground="#ffffff")
            self.chat_display.tag_config("ai_label", foreground="#88ddff")
            self.chat_display.tag_config("ai_text", foreground="#cccccc")
        
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
    
    def send_chat_message(self, window):
        """Send a message to the AI"""
        message = self.chat_input.get().strip()
        
        if not message:
            return
        
        # Add user message to history
        self.chat_history.append({"role": "user", "content": message})
        
        # Clear input
        self.chat_input.delete(0, "end")
        
        # Refresh display
        self.refresh_chat_display()
        
        # Show loading
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", "DNA Buddy: ", "ai_label")
        self.chat_display.insert("end", "Thinking...\n\n", "thinking")
        self.chat_display.tag_config("ai_label", foreground="#88ddff")
        self.chat_display.tag_config("thinking", foreground="#aaaaaa")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
        
        # Get AI response in thread
        thread = threading.Thread(
            target=self._get_chat_response_thread,
            args=(message,)
        )
        thread.daemon = True
        thread.start()
    
    def _get_chat_response_thread(self, message):
        """Get AI response in thread"""
        try:
            # Build context with personality and nutrition goals
            context = f"You are a {self.ai_personality} nutrition AI assistant named DNA Buddy. "
            
            if self.nutrition_goals:
                context += f"\n\nUser's nutrition goals:\n"
                context += f"- Daily calories: {int(self.nutrition_goals['calories'])} kcal\n"
                context += f"- Protein: {int(self.nutrition_goals['protein'])}g\n"
                context += f"- Carbs: {int(self.nutrition_goals['carbs'])}g\n"
                context += f"- Fats: {int(self.nutrition_goals['fats'])}g\n"
            
            if self.current_dishes:
                context += f"\n\nRecommended dishes: {', '.join([d['name'] for d in self.current_dishes[:5]])}\n"
            
            # Personality prefix
            personality_prefixes = {
                "pirate chef": "Respond like a pirate chef. Use pirate language and cooking terms. ",
                "zen wellness guru": "Respond like a zen wellness guru. Be calm, peaceful, and mindful. ",
                "scientific researcher": "Respond like a scientific researcher. Use technical terms and cite studies. ",
                "enthusiastic fitness coach": "Respond like an enthusiastic fitness coach. Be energetic and motivating! ",
                "wise health mentor": "Respond like a wise health mentor. Be thoughtful and share wisdom. ",
                "casual buddy": "Respond like a casual friend. Be relaxed and conversational. ",
            }
            
            personality_prefix = personality_prefixes.get(self.ai_personality, "")
            full_prompt = personality_prefix + context + f"\n\nUser question: {message}"
            
            # Get response
            response = self.hackclub_ai(full_prompt)
            
            # Add AI response to history
            self.chat_history.append({"role": "assistant", "content": response})
            
            # Update UI
            self.after(0, self.refresh_chat_display)
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.chat_history.append({"role": "assistant", "content": error_msg})
            self.after(0, self.refresh_chat_display)
    
    def clear_chat(self):
        """Clear chat history"""
        self.chat_history = []
        self.refresh_chat_display()
    
    def show_error(self, message):
        """Show error message"""
        error_window = ctk.CTkToplevel(self)
        error_window.title("Notice")
        error_window.geometry("450x200")
        error_window.configure(fg_color=("#1a1a2e", "#1a1a2e"))
        
        error_frame = ctk.CTkFrame(
            error_window, fg_color=("#2a2a3e", "#2a2a3e"), corner_radius=15
        )
        error_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        error_label = ctk.CTkLabel(error_frame, text="⚠️", font=ctk.CTkFont(size=40))
        error_label.pack(pady=(20, 10))
        
        message_label = ctk.CTkLabel(
            error_frame, text=message, font=ctk.CTkFont(size=14),
            text_color=("#ffffff", "#ffffff"), wraplength=380
        )
        message_label.pack(pady=10)
        
        ok_btn = ctk.CTkButton(
            error_frame, text="OK", command=error_window.destroy,
            width=120, height=40, font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#00ff88", "#00cc66"),
            hover_color=("#00cc66", "#00aa55"), corner_radius=20
        )
        ok_btn.pack(pady=20)
    
    def hackclub_ai(self, prompt, retries=3):
        """Call Groq API"""
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "openai/gpt-oss-20b",
            "messages": [
                {"role": "system", "content": "You are a helpful AI nutritionist."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
        }

        for attempt in range(retries):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=60)
                response.raise_for_status()
                result = response.json()
                message = result["choices"][0]["message"]["content"].strip()
                return message
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(2)
                else:
                    raise Exception(f"Failed after {retries} attempts: {e}")

    def quicksort(self, arr):
        """Quicksort algorithm"""
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return self.quicksort(left) + middle + self.quicksort(right)
    
    def binary_search(self, arr, target):
        """Binary search for closest value"""
        if not arr:
            return 0
        lower, higher = 0, len(arr) - 1
        while lower < higher:
            middle = (lower + higher) // 2
            if target == arr[middle]:
                return middle
            elif target > arr[middle]:
                lower = middle + 1
            else:
                higher = middle
        if lower >= len(arr):
            lower = len(arr) - 1
        if lower > 0 and abs(arr[lower] - target) > abs(arr[lower - 1] - target):
            lower -= 1
        return lower
    
    def calculate_score(self, goals, recipes):
        """Calculate recipe scores"""
        if not recipes or not goals:
            return []

        scores = [0.0] * len(recipes)

        for goal_idx in range(len(goals)):
            goal = goals[goal_idx]
            values = [recipe[goal_idx] for recipe in recipes]
            sorted_values = self.quicksort(values)
            closest_idx = self.binary_search(sorted_values, goal)
            ideal_value = sorted_values[closest_idx]

            for recipe_idx in range(len(recipes)):
                recipe_value = recipes[recipe_idx][goal_idx]
                diff = abs(ideal_value - recipe_value)
                score = 1 - (diff / goal) if goal != 0 else 1.0
                score = max(0.0, min(score, 1.0))
                scores[recipe_idx] += score

        scores = [score / len(goals) for score in scores]
        indexed_scores = [(i, scores[i]) for i in range(len(recipes))]
        indexed_scores.sort(key=lambda x: x[1], reverse=True)

        return indexed_scores


if __name__ == "__main__":
    app = NutritionPlannerApp()
    app.mainloop()
