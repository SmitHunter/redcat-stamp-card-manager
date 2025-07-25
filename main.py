import customtkinter as ctk
import requests
import json
import os

# --- Theme Setup ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# --- Configuration Loading ---
def load_config():
    """Load configuration from config.json"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Default configuration if file doesn't exist
        return {
            "api": {
                "base_url": "https://your-api-url.com/api/v1",
                "auth_type": "U"
            },
            "business": {
                "name": "Your Business",
                "stamps_per_card": 4,
                "default_coupon_id": 230,
                "default_coupon_name": "Reward Coupon",
                "allow_duplicate_coupons": true
            },
            "ui": {
                "stamp_emoji": "🍩",
                "empty_slot_emoji": "⭕"
            }
        }

# Load configuration
CONFIG = load_config()
BASE_URL = CONFIG["api"]["base_url"]

# --- API Helpers ---
def login(username, password):
    url = f"{BASE_URL}/login"
    payload = {"username": username, "psw": password, "auth_type": CONFIG["api"]["auth_type"]}
    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()
        response_data = r.json()
        if "token" not in response_data:
            raise ValueError(f"Login response missing token. Response: {response_data}")
        return response_data["token"]
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Login request failed: {e}")
    except KeyError as e:
        raise ValueError(f"Login response missing expected field: {e}. Response: {response_data}")

def find_stampcard_recid(token, member_id):
    """
    Authenticated GET /stampcard → find the card whose member_recid matches.
    """
    url = f"{BASE_URL}/stampcard"
    headers = {"X-Redcat-Authtoken": token}
    r = requests.get(url, headers=headers)
    r.raise_for_status()

    for card in r.json().get("data", []):
        if card.get("member_recid") == member_id:
            return card["recid"]

    raise ValueError(f"No stampcard found for member {member_id}")

def get_stampcard(token, member_id):
    """Locate the recid, then GET that specific stampcard."""
    recid = find_stampcard_recid(token, member_id)
    url = f"{BASE_URL}/stampcard/{recid}"
    headers = {"X-Redcat-Authtoken": token}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()["data"]

def assign_coupon(token, coupon_id, member_ids, allow_duplicates=None):
    """Assign a coupon to members"""
    url = f"{BASE_URL}/coupons/{coupon_id}/create"
    headers = {
        "X-Redcat-Authtoken": token,
        "Content-Type": "application/json"
    }
    payload = {
        "Members": member_ids,
        "HandleErrors": True,
        "ReturnAlias": True
    }
    
    # Add create_duplicate parameter if specified
    if allow_duplicates is not None:
        payload["create_duplicate"] = allow_duplicates
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def update_stampcard(token, member_id, stamps, cards_filled, rewards_earned):
    """Locate the recid, then PUT updated fields to that stampcard."""
    recid = find_stampcard_recid(token, member_id)
    url = f"{BASE_URL}/stampcard/{recid}"
    headers = {
        "X-Redcat-Authtoken": token,
        "Content-Type": "application/json"
    }
    payload = {
        "member_recid": member_id,
        "no_of_stamps": stamps,
        "no_of_cards_filled": cards_filled,
        "no_of_rewards_earned": rewards_earned
    }
    r = requests.put(url, headers=headers, json=payload)
    r.raise_for_status()
    return r.json()["data"]

# --- GUI App ---
class StampCardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"Stamp Card Manager - {CONFIG['business']['name']}")
        self.geometry("600x950")
        self.configure(fg_color="#1E1E1E")
        self.resizable(False, False)

        self.token = None
        self.stamps_per_card = CONFIG["business"]["stamps_per_card"]

        frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        frame.pack(expand=True, padx=20, pady=20, fill="both")

        # -- Configuration Info --
        config_frame = ctk.CTkFrame(frame, fg_color="#404040", corner_radius=10)
        config_frame.pack(pady=(10, 15), padx=20, fill="x")
        
        config_title = ctk.CTkLabel(config_frame, text="⚙️ Current Configuration", font=("Arial", 12, "bold"))
        config_title.pack(pady=(8, 5))
        
        config_info = ctk.CTkLabel(config_frame, 
            text=f"Business: {CONFIG['business']['name']}\nStamps per card: {self.stamps_per_card}\nAPI: {BASE_URL}", 
            font=("Arial", 10), justify="left", text_color="#CCCCCC")
        config_info.pack(pady=(0, 8))

        # -- Credentials --
        self.username_entry = ctk.CTkEntry(frame, placeholder_text="API Username", width=300)
        self.username_entry.pack(pady=(10, 5))
        self.password_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=300)
        self.password_entry.pack(pady=5)

        # -- Member ID & Fetch --
        self.member_id_entry = ctk.CTkEntry(frame, placeholder_text="Member ID", width=300)
        self.member_id_entry.pack(pady=(30, 5))
        self.fetch_button = ctk.CTkButton(frame, text="Fetch Stamp Card", command=self.fetch_stampcard)
        self.fetch_button.pack(pady=10)

        # -- Visual Stamp Card --
        self.stamp_card_frame = ctk.CTkFrame(frame, fg_color="#2B2B2B", corner_radius=10)
        self.stamp_card_frame.pack(pady=10, padx=20, fill="x")
        
        stamp_title = ctk.CTkLabel(self.stamp_card_frame, text="🎫 Stamp Card", font=("Arial", 16, "bold"))
        stamp_title.pack(pady=(10, 5))
        
        # Grid for stamps (dynamic based on config)
        self.stamps_grid_frame = ctk.CTkFrame(self.stamp_card_frame, fg_color="transparent")
        self.stamps_grid_frame.pack(pady=5)
        
        self.stamp_labels = []
        # Create stamps in rows of up to 5 per row
        max_per_row = 5
        for i in range(self.stamps_per_card):
            row = i // max_per_row
            col = i % max_per_row
            stamp_label = ctk.CTkLabel(self.stamps_grid_frame, text=CONFIG["ui"]["empty_slot_emoji"], 
                                     font=("Arial", 30), width=50, height=50)
            stamp_label.grid(row=row, column=col, padx=8, pady=5)
            self.stamp_labels.append(stamp_label)
        
        # Info labels
        self.info_frame = ctk.CTkFrame(self.stamp_card_frame, fg_color="transparent")
        self.info_frame.pack(pady=(5, 10))
        
        self.stamps_info = ctk.CTkLabel(self.info_frame, text=f"Stamps: 0/{self.stamps_per_card}", font=("Arial", 12))
        self.stamps_info.pack()
        
        self.cards_info = ctk.CTkLabel(self.info_frame, text="Cards Completed: 0 | Rewards Earned: 0", font=("Arial", 12))
        self.cards_info.pack()
        
        self.status_info = ctk.CTkLabel(self.info_frame, text="", font=("Arial", 12, "bold"))
        self.status_info.pack()

        # -- Stamp Card Fields --
        stamps_label = ctk.CTkLabel(frame, text=f"Update Current Stamps (0-{self.stamps_per_card}):", font=("Arial", 12, "bold"))
        stamps_label.pack(pady=(15, 2))
        self.stamps_entry = ctk.CTkEntry(frame, placeholder_text="Number of stamps on current card", width=300)
        self.stamps_entry.pack(pady=2)
        
        # Add coupon ID field for when stamps are completed
        coupon_label = ctk.CTkLabel(frame, text=f"Coupon ID (for {self.stamps_per_card}/{self.stamps_per_card} stamp rewards):", font=("Arial", 12))
        coupon_label.pack(pady=(10, 2))
        self.coupon_id_entry = ctk.CTkEntry(frame, placeholder_text=CONFIG["business"]["default_coupon_name"], width=300)
        self.coupon_id_entry.pack(pady=2)
        # Set default coupon ID
        self.coupon_id_entry.insert(0, str(CONFIG["business"]["default_coupon_id"]))

        self.update_button = ctk.CTkButton(frame, text="Update Stamp Card", command=self.update_stampcard)
        self.update_button.pack(pady=20)

        # -- Output Log --
        log_label = ctk.CTkLabel(frame, text="📋 Activity Log", font=("Arial", 12, "bold"))
        log_label.pack(pady=(10, 5))
        
        self.output_box = ctk.CTkTextbox(frame, height=200, width=540, wrap="word", state="disabled")
        self.output_box.pack(pady=(0, 10), fill="x", expand=False)
        self.output_box.configure(fg_color="#0D1117", text_color="#E6EDF3", font=("Consolas", 11))
        
        # -- Info Section (at bottom) --
        info_frame = ctk.CTkFrame(frame, fg_color="#404040", corner_radius=10)
        info_frame.pack(pady=(15, 15), padx=20, fill="x")
        
        info_title = ctk.CTkLabel(info_frame, text="ℹ️ How it Works", font=("Arial", 14, "bold"), text_color="#FFFFFF")
        info_title.pack(pady=(10, 5))
        
        info_text = ctk.CTkLabel(info_frame, 
            text=f"• 1-{self.stamps_per_card-1} Stamps: Updates normally\n• {self.stamps_per_card}/{self.stamps_per_card} Stamps: Auto-assigns reward coupon\n• Card resets to 0/{self.stamps_per_card} after reward is given", 
            font=("Arial", 11), justify="left", text_color="#CCCCCC")
        info_text.pack(pady=(0, 10))

    def log(self, message):
        self.output_box.configure(state="normal")  # Enable to insert
        self.output_box.insert("end", message + "\n")
        self.output_box.see("end")
        self.output_box.configure(state="disabled")  # Disable again
    
    def update_stamp_display(self, data):
        """Update the visual stamp card display"""
        num_stamps = data["no_of_stamps"]
        cards_filled = data["no_of_cards_filled"]
        rewards_earned = data["no_of_rewards_earned"]
        
        # Update stamp grid (dynamic based on config)
        for i, label in enumerate(self.stamp_labels):
            if i < num_stamps:
                label.configure(text=CONFIG["ui"]["stamp_emoji"], text_color="#000000")  # Filled stamp in black
            else:
                label.configure(text=CONFIG["ui"]["empty_slot_emoji"], text_color="#666666")  # Empty slot in gray
        
        # Update info labels
        self.stamps_info.configure(text=f"Stamps: {num_stamps}/{self.stamps_per_card}")
        self.cards_info.configure(text=f"Cards Completed: {cards_filled} | Rewards Earned: {rewards_earned}")
        
        # Update status (dynamic based on stamps_per_card)
        if num_stamps == self.stamps_per_card:
            self.status_info.configure(text="🎉 CARD COMPLETE! Ready for reward!", text_color="#00FF00")
        elif num_stamps == self.stamps_per_card - 1:
            self.status_info.configure(text="⚡ One more stamp needed!", text_color="#FFA500")
        elif num_stamps > 0:
            self.status_info.configure(text=f"🔥 {self.stamps_per_card-num_stamps} stamps to go!", text_color="#87CEEB")
        else:
            self.status_info.configure(text="📍 Start collecting stamps!", text_color="#CCCCCC")

    def handle_login(self):
        self.output_box.delete("1.0", "end")
        try:
            u = self.username_entry.get().strip()
            p = self.password_entry.get().strip()
            self.log("🔐 Logging in...")
            self.token = login(u, p)
            self.log("✅ Logged in.")
        except Exception as e:
            self.log(f"❌ Login failed: {e}")

    def fetch_stampcard(self):
        self.output_box.delete("1.0", "end")
        
        # Show loading state
        original_text = self.fetch_button.cget("text")
        self.fetch_button.configure(text="⏳ Fetching...", state="disabled")
        self.update()  # Force GUI refresh
        
        try:
            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()
            mid = int(self.member_id_entry.get().strip())
            
            if not username or not password:
                self.log("❌ Error: Username and password are required")
                return
            
            self.log("🔐 Logging in...")
            try:
                token = login(username, password)
                self.log("✅ Login successful")
            except Exception as login_error:
                self.log(f"❌ Login failed: {login_error}")
                return
            
            self.log("📡 Fetching stamp card...")
            data = get_stampcard(token, mid)

            # populate stamp field only (other fields are now read-only in the visual display)
            self.stamps_entry.delete(0, "end")
            self.stamps_entry.insert(0, str(data["no_of_stamps"]))
            
            # Update visual stamp display
            self.update_stamp_display(data)
            
            # Force GUI update
            self.update()

            self.log("✅ Stamp card data loaded.")
        except Exception as e:
            self.log(f"❌ Error fetching stamp card: {e}")
        finally:
            # Restore button state
            self.fetch_button.configure(text=original_text, state="normal")

    def update_stampcard(self):
        # Show loading state
        original_text = self.update_button.cget("text")
        self.update_button.configure(text="⏳ Updating...", state="disabled")
        self.update()  # Force GUI refresh
        
        try:
            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()
            mid = int(self.member_id_entry.get().strip())
            stamps = int(self.stamps_entry.get().strip())
            coupon_id_str = self.coupon_id_entry.get().strip()

            self.log("🔐 Logging in...")
            try:
                token = login(username, password)
                self.log("✅ Login successful")
            except Exception as login_error:
                self.log(f"❌ Login failed: {login_error}")
                return

            # Get current data to preserve cards_filled and rewards_earned
            current_data = get_stampcard(token, mid)
            current_cards = current_data["no_of_cards_filled"]
            current_rewards = current_data["no_of_rewards_earned"]

            # Check if stamps are being set to max (card completion)
            if stamps == self.stamps_per_card:
                if not coupon_id_str:
                    self.log(f"❌ Error: Coupon ID required when completing a stamp card ({self.stamps_per_card}/{self.stamps_per_card} stamps)")
                    return
                
                coupon_id = int(coupon_id_str)
                
                self.log("🎉 Card completed! Generating coupon and resetting stamps...")
                
                # Assign coupon to member with duplicate setting from config
                allow_duplicates = CONFIG["business"].get("allow_duplicate_coupons", False)
                self.log(f"🎫 Assigning coupon {coupon_id} to member {mid} (duplicates: {allow_duplicates})...")
                coupon_result = assign_coupon(token, coupon_id, [mid], allow_duplicates)
                self.log("✅ Coupon assigned successfully!")
                
                # Reset stamps to 0 and increment counters
                final_stamps = 0
                final_cards = current_cards + 1
                final_rewards = current_rewards + 1
                
                self.log(f"🔄 Resetting stamps to 0/{self.stamps_per_card} (Card #{final_cards} completed)")
            else:
                # Normal stamp update (1, 2, or 3 stamps)
                final_stamps = stamps
                final_cards = current_cards
                final_rewards = current_rewards
                self.log(f"🛠️ Updating stamps to {stamps}/{self.stamps_per_card}...")

            # Update the stamp card
            upd = update_stampcard(token, mid, final_stamps, final_cards, final_rewards)
            self.log("✅ Stamp card updated successfully!")
            
            # Refresh the display with updated data
            data = get_stampcard(token, mid)
            self.update_stamp_display(data)
            
            # Update the stamps entry field to show the actual final value
            self.stamps_entry.delete(0, "end")
            self.stamps_entry.insert(0, str(final_stamps))
            
        except Exception as e:
            self.log(f"❌ Error updating stamp card: {e}")
        finally:
            # Restore button state
            self.update_button.configure(text=original_text, state="normal")

# --- Main ---
if __name__ == "__main__":
    app = StampCardApp()
    app.mainloop()
