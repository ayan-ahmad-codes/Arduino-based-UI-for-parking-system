# Ayan's Project - Smart Parking GUI (Modern Enhanced Version)
# Redesigned with fresh color scheme and enhanced animations

import serial
import tkinter as tk
from tkinter import ttk, Canvas, Frame, Label, Button
import pygame
import threading
import time
from datetime import datetime
import math
import random

# CONFIGURATION
SERIAL_PORT = 'COM6'
BAUD_RATE = 9600
ALERT_SOUND = "alert.mp3"
NUM_SLOTS = 4

# New Modern Color Scheme
COLORS = {
    'bg_main': '#0f0f23',
    'bg_secondary': '#1a1a2e',
    'card_bg': '#16213e',
    'card_hover': '#1e3a5f',
    'accent_cyan': '#00fff9',
    'accent_lime': '#39ff14',
    'accent_pink': '#ff006e',
    'accent_gold': '#ffb700',
    'accent_purple': '#7209b7',
    'accent_coral': '#ff4081',
    'text_primary': '#ffffff',
    'text_secondary': '#94a3b8',
    'text_muted': '#64748b',
    'success': '#10b981',
    'warning': '#f59e0b',
    'error': '#ef4444',
    'gradient_start': '#667eea',
    'gradient_end': '#764ba2'
}

pygame.mixer.init()
def play_alert():
    try:
        pygame.mixer.music.load(ALERT_SOUND)
        pygame.mixer.music.play()
    except Exception as e:
        print("Sound error:", e)

class ModernParkingGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚗 AYAN'S SMART PARKING SYSTEM")
        self.root.geometry("1500x900")
        self.root.configure(bg=COLORS['bg_main'])
        self.root.resizable(True, True)
        
        # Animation variables
        self.animation_counter = 0
        self.pulse_phase = 0
        self.wave_phase = 0
        self.glow_intensity = 0
        self.rotation_angle = 0
        
        self.setup_ui()
        self.setup_serial()
        self.start_animations()

    def setup_ui(self):
        # Main container with padding
        main_container = Frame(self.root, bg=COLORS['bg_main'])
        main_container.pack(fill='both', expand=True, padx=25, pady=25)

        # ANIMATED HEADER SECTION
        self.create_header(main_container)
        
        # MAIN CONTENT AREA
        content_frame = Frame(main_container, bg=COLORS['bg_main'])
        content_frame.pack(fill='both', expand=True, pady=20)
        
        # Left side - Parking Slots
        self.create_parking_slots(content_frame)
        
        # Right side - Stats and Controls
        self.create_stats_panel(content_frame)
        
        # Bottom - Status Bar
        self.create_status_bar(main_container)

    def create_header(self, parent):
        header_frame = Frame(parent, bg=COLORS['bg_main'], height=120)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Main title with glow effect
        self.title_label = Label(
            header_frame, 
            text="🔥 AYAN'S SMART PARKING SYSTEM 🔥",
            font=("Segoe UI", 32, "bold"),
            fg=COLORS['accent_cyan'],
            bg=COLORS['bg_main']
        )
        self.title_label.pack(pady=(15, 5))
        
        # Subtitle with wave animation
        self.subtitle_label = Label(
            header_frame,
            text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            font=("Consolas", 10),
            fg=COLORS['accent_lime'],
            bg=COLORS['bg_main']
        )
        self.subtitle_label.pack()
        
        # Status indicator
        self.status_indicator = Label(
            header_frame,
            text="● SYSTEM ONLINE ● REAL-TIME MONITORING ACTIVE",
            font=("Segoe UI", 12, "bold"),
            fg=COLORS['success'],
            bg=COLORS['bg_main']
        )
        self.status_indicator.pack(pady=(5, 0))

    def create_parking_slots(self, parent):
        slots_frame = Frame(parent, bg=COLORS['bg_main'])
        slots_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))
        
        # Slots grid
        slots_container = Frame(slots_frame, bg=COLORS['bg_main'])
        slots_container.pack(expand=True)
        
        self.slot_frames = []
        self.slot_status_labels = []
        self.slot_canvases = []
        self.slot_animations = []
        
        for i in range(NUM_SLOTS):
            # Create animated slot card
            slot_card = Frame(
                slots_container,
                bg=COLORS['card_bg'],
                bd=0,
                relief='flat',
                width=280,
                height=200
            )
            slot_card.grid(row=i//2, column=i%2, padx=20, pady=20)
            slot_card.pack_propagate(False)
            
            # Slot header
            slot_header = Frame(slot_card, bg=COLORS['card_bg'], height=40)
            slot_header.pack(fill='x', pady=(10, 0))
            slot_header.pack_propagate(False)
            
            Label(
                slot_header,
                text=f"SLOT {i+1:02d}",
                font=("Segoe UI", 16, "bold"),
                fg=COLORS['text_primary'],
                bg=COLORS['card_bg']
            ).pack()
            
            # Animated canvas for slot visualization
            canvas = Canvas(
                slot_card,
                width=200,
                height=80,
                bg=COLORS['card_bg'],
                highlightthickness=0,
                bd=0
            )
            canvas.pack(pady=15)
            
            # Status label with modern styling
            status_label = Label(
                slot_card,
                text="AVAILABLE",
                font=("Segoe UI", 12, "bold"),
                fg=COLORS['success'],
                bg=COLORS['card_bg']
            )
            status_label.pack(pady=(0, 10))
            
            # Store references
            self.slot_frames.append(slot_card)
            self.slot_status_labels.append(status_label)
            self.slot_canvases.append(canvas)
            self.slot_animations.append({'pulse': 0, 'glow': 0})

    def create_stats_panel(self, parent):
        stats_frame = Frame(parent, bg=COLORS['bg_secondary'], width=350)
        stats_frame.pack(side='right', fill='y', padx=(0, 0))
        stats_frame.pack_propagate(False)
        
        # Stats header
        stats_header = Label(
            stats_frame,
            text="📊 LIVE STATISTICS",
            font=("Segoe UI", 18, "bold"),
            fg=COLORS['accent_gold'],
            bg=COLORS['bg_secondary']
        )
        stats_header.pack(pady=(20, 10))
        
        # Stats cards
        self.stat_cards = []
        stats_data = [
            ("TOTAL SLOTS", "4", COLORS['accent_purple']),
            ("AVAILABLE", "0", COLORS['success']),
            ("OCCUPIED", "0", COLORS['error']),
            ("OCCUPANCY RATE", "0%", COLORS['warning'])
        ]
        
        for title, value, color in stats_data:
            card = Frame(stats_frame, bg=COLORS['card_bg'], height=80)
            card.pack(fill='x', padx=20, pady=10)
            card.pack_propagate(False)
            
            value_label = Label(
                card,
                text=value,
                font=("Segoe UI", 24, "bold"),
                fg=color,
                bg=COLORS['card_bg']
            )
            value_label.pack(pady=(10, 0))
            
            title_label = Label(
                card,
                text=title,
                font=("Segoe UI", 10),
                fg=COLORS['text_secondary'],
                bg=COLORS['card_bg']
            )
            title_label.pack()
            
            self.stat_cards.append(value_label)
        
        # Control buttons
        self.create_control_panel(stats_frame)

    def create_control_panel(self, parent):
        controls_frame = Frame(parent, bg=COLORS['bg_secondary'])
        controls_frame.pack(fill='x', pady=(30, 0))
        
        Label(
            controls_frame,
            text="🎮 CONTROL PANEL",
            font=("Segoe UI", 16, "bold"),
            fg=COLORS['accent_coral'],
            bg=COLORS['bg_secondary']
        ).pack(pady=(0, 20))
        
        # Button configurations
        buttons_config = [
            ("🎲 SIMULATE", self.simulate_data, COLORS['accent_cyan']),
            ("🔄 RESET SYSTEM", self.reset_system, COLORS['success']),
            ("🚨 EMERGENCY", self.emergency_alert, COLORS['error'])
        ]
        
        for text, command, color in buttons_config:
            btn = Button(
                controls_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                font=("Segoe UI", 11, "bold"),
                bd=0,
                relief='flat',
                padx=20,
                pady=8,
                cursor='hand2'
            )
            btn.pack(fill='x', padx=20, pady=5)
            
            # Add hover effects
            btn.bind("<Enter>", lambda e, b=btn, c=color: self.on_button_hover(b, c))
            btn.bind("<Leave>", lambda e, b=btn, c=color: self.on_button_leave(b, c))

    def create_status_bar(self, parent):
        status_frame = Frame(parent, bg=COLORS['bg_secondary'], height=60)
        status_frame.pack(fill='x', pady=(20, 0))
        status_frame.pack_propagate(False)
        
        # Connection status
        self.connection_label = Label(
            status_frame,
            text="🔌 SERIAL: SEARCHING...",
            font=("Consolas", 10),
            fg=COLORS['warning'],
            bg=COLORS['bg_secondary']
        )
        self.connection_label.pack(side='left', padx=20, pady=20)
        
        # Clock with modern design
        self.time_label = Label(
            status_frame,
            text="",
            font=("Segoe UI", 12, "bold"),
            fg=COLORS['text_primary'],
            bg=COLORS['bg_secondary']
        )
        self.time_label.pack(side='right', padx=20, pady=20)

    def on_button_hover(self, button, color):
        # Create darker version of color for hover
        button.config(bg=color, relief='raised')
    
    def on_button_leave(self, button, color):
        button.config(bg=color, relief='flat')

    def setup_serial(self):
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            self.connection_label.config(text="🔌 SERIAL: CONNECTED", fg=COLORS['success'])
        except:
            self.ser = None
            self.connection_label.config(text="🔌 SERIAL: DISCONNECTED", fg=COLORS['error'])

    def update_slots(self, available):
        occupied = NUM_SLOTS - available
        
        for i in range(NUM_SLOTS):
            is_occupied = i < occupied
            canvas = self.slot_canvases[i]
            canvas.delete("all")
            
            if is_occupied:
                # Occupied slot - animated car
                self.draw_occupied_slot(canvas, i)
                self.slot_status_labels[i].config(text="🚗 OCCUPIED", fg=COLORS['error'])
                self.slot_frames[i].config(bg=COLORS['card_hover'])
            else:
                # Available slot - animated parking space
                self.draw_available_slot(canvas, i)
                self.slot_status_labels[i].config(text="✅ AVAILABLE", fg=COLORS['success'])
                self.slot_frames[i].config(bg=COLORS['card_bg'])
        
        # Update statistics
        self.stat_cards[0].config(text=str(NUM_SLOTS))
        self.stat_cards[1].config(text=str(available))
        self.stat_cards[2].config(text=str(occupied))
        self.stat_cards[3].config(text=f"{(occupied / NUM_SLOTS) * 100:.0f}%")

    def draw_occupied_slot(self, canvas, slot_index):
        # Animated car representation
        pulse = math.sin(self.pulse_phase + slot_index) * 5
        
        # Car body
        canvas.create_rectangle(
            50 + pulse, 30, 150 + pulse, 50,
            fill=COLORS['accent_pink'],
            outline=COLORS['accent_coral'],
            width=2
        )
        
        # Car wheels
        canvas.create_oval(60 + pulse, 45, 70 + pulse, 55, fill=COLORS['text_primary'])
        canvas.create_oval(130 + pulse, 45, 140 + pulse, 55, fill=COLORS['text_primary'])
        
        # Warning indicator
        canvas.create_text(
            100, 20,
            text="⚠️",
            font=("Arial", 12),
            fill=COLORS['warning']
        )

    def draw_available_slot(self, canvas, slot_index):
        # Animated parking space
        glow = math.sin(self.glow_intensity + slot_index * 0.5) * 3
        
        # Parking space outline
        canvas.create_rectangle(
            40, 25, 160, 55,
            outline=COLORS['success'],
            width=2 + int(glow),
            fill='',
            dash=(5, 5)
        )
        
        # Availability indicator
        canvas.create_text(
            100, 40,
            text="✨",
            font=("Arial", 16),
            fill=COLORS['accent_lime']
        )

    def read_serial(self):
        if self.ser and self.ser.in_waiting:
            try:
                line = self.ser.readline().decode().strip()
                if "SLOTS:" in line:
                    count = int(line.split(":")[1])
                    self.update_slots(count)
            except:
                pass
        self.root.after(500, self.read_serial)

    def start_animations(self):
        self.animate_elements()
        self.update_clock()
        self.read_serial()

    def animate_elements(self):
        # Update animation phases
        self.animation_counter += 1
        self.pulse_phase += 0.2
        self.wave_phase += 0.1
        self.glow_intensity += 0.15
        self.rotation_angle += 2
        
        # Animate title color
        title_colors = [COLORS['accent_cyan'], COLORS['accent_lime'], COLORS['accent_gold'], COLORS['accent_coral']]
        color_index = (self.animation_counter // 30) % len(title_colors)
        self.title_label.config(fg=title_colors[color_index])
        
        # Animate status indicator
        if self.animation_counter % 60 < 30:
            self.status_indicator.config(text="● SYSTEM ONLINE ● MONITORING ACTIVE")
        else:
            self.status_indicator.config(text="● LIVE DATA ● REAL-TIME UPDATES")
        
        # Continue animation
        self.root.after(50, self.animate_elements)

    def update_clock(self):
        now = datetime.now()
        time_str = now.strftime("🕐 %A, %B %d, %Y | %H:%M:%S")
        self.time_label.config(text=time_str)
        self.root.after(1000, self.update_clock)

    def simulate_data(self):
        slots = random.randint(0, NUM_SLOTS)
        self.update_slots(slots)
        print(f"Simulation: {slots} available slots")

    def reset_system(self):
        self.update_slots(NUM_SLOTS)
        print("System reset - all slots available")

    def emergency_alert(self):
        play_alert()
        self.update_slots(0)
        
        # Flash emergency colors
        original_bg = self.root.cget('bg')
        self.root.configure(bg=COLORS['error'])
        self.root.after(200, lambda: self.root.configure(bg=original_bg))
        print("Emergency alert activated!")

    def run(self):
        self.reset_system()
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernParkingGUI()
    app.run()