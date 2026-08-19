import tkinter as tk
from tkinter import messagebox
import requests
import webbrowser
from PIL import Image, ImageTk
from io import BytesIO
import threading


class GitHubProfileFinder:
    def __init__(self, root):
        self.root = root

        self.root.title("💗 GitHub Profile Finder")
        self.root.geometry("850x720")
        self.root.resizable(False, False)
        self.root.configure(bg="#fff5f8")

        self.avatar_image = None

        self.create_ui()

    # =========================================================
    # UI
    # =========================================================

    def create_ui(self):

        # Header
        header = tk.Frame(
            self.root,
            bg="#fff5f8"
        )
        header.pack(fill="x", pady=(25, 5))

        tk.Label(
            header,
            text="🔎 GitHub Profile Finder",
            font=("Segoe UI", 28, "bold"),
            fg="#e83e72",
            bg="#fff5f8"
        ).pack()

        tk.Label(
            header,
            text="✨ Discover GitHub profiles instantly ✨",
            font=("Segoe UI", 11),
            fg="#777777",
            bg="#fff5f8"
        ).pack(pady=5)

        # Search Card
        search_card = tk.Frame(
            self.root,
            bg="white",
            highlightbackground="#f3bfd0",
            highlightthickness=1
        )
        search_card.pack(
            fill="x",
            padx=35,
            pady=18
        )

        tk.Label(
            search_card,
            text="Enter GitHub Username",
            font=("Segoe UI", 11, "bold"),
            fg="#555555",
            bg="white"
        ).pack(
            pady=(18, 8)
        )

        search_row = tk.Frame(
            search_card,
            bg="white"
        )
        search_row.pack(pady=(0, 18))

        self.username_entry = tk.Entry(
            search_row,
            width=35,
            font=("Segoe UI", 12),
            justify="center",
            bg="#fff9fb",
            fg="#333333",
            relief="flat",
            highlightbackground="#efb8cb",
            highlightthickness=1
        )
        self.username_entry.pack(
            side="left",
            padx=8,
            ipady=8
        )

        self.search_button = tk.Button(
            search_row,
            text="🔍 Search",
            command=self.start_search,
            font=("Segoe UI", 11, "bold"),
            bg="#f55382",
            fg="white",
            activebackground="#dc3d6c",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=8
        )
        self.search_button.pack(side="left")

        self.username_entry.bind(
            "<Return>",
            lambda event: self.start_search()
        )

        # Profile Card
        self.profile_card = tk.Frame(
            self.root,
            bg="white",
            highlightbackground="#f3bfd0",
            highlightthickness=1
        )
        self.profile_card.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=5
        )

        # Avatar
        self.avatar_label = tk.Label(
            self.profile_card,
            text="👤",
            font=("Segoe UI Emoji", 65),
            bg="white"
        )
        self.avatar_label.pack(pady=(20, 5))

        # Name
        self.name_label = tk.Label(
            self.profile_card,
            text="Search for a GitHub user",
            font=("Segoe UI", 20, "bold"),
            fg="#d93667",
            bg="white"
        )
        self.name_label.pack()

        # Username
        self.username_label = tk.Label(
            self.profile_card,
            text="@username",
            font=("Segoe UI", 11),
            fg="#888888",
            bg="white"
        )
        self.username_label.pack(pady=3)

        # Bio
        self.bio_label = tk.Label(
            self.profile_card,
            text="Enter a username above to view their profile.",
            font=("Segoe UI", 10),
            fg="#666666",
            bg="white",
            wraplength=650,
            justify="center"
        )
        self.bio_label.pack(pady=8)

        # Stats
        stats_frame = tk.Frame(
            self.profile_card,
            bg="#fff5f8"
        )
        stats_frame.pack(
            fill="x",
            padx=60,
            pady=15
        )

        self.repo_label = self.create_stat(
            stats_frame,
            "📦",
            "Repositories"
        )

        self.followers_label = self.create_stat(
            stats_frame,
            "👥",
            "Followers"
        )

        self.following_label = self.create_stat(
            stats_frame,
            "💗",
            "Following"
        )

        # Details
        details_frame = tk.Frame(
            self.profile_card,
            bg="white"
        )
        details_frame.pack(
            pady=8
        )

        self.location_label = tk.Label(
            details_frame,
            text="📍 Location: —",
            font=("Segoe UI", 10),
            fg="#666666",
            bg="white"
        )
        self.location_label.pack(pady=3)

        self.website_label = tk.Label(
            details_frame,
            text="🌐 Website: —",
            font=("Segoe UI", 10),
            fg="#666666",
            bg="white"
        )
        self.website_label.pack(pady=3)

        self.joined_label = tk.Label(
            details_frame,
            text="📅 Joined: —",
            font=("Segoe UI", 10),
            fg="#666666",
            bg="white"
        )
        self.joined_label.pack(pady=3)

        # Profile Button
        self.profile_button = tk.Button(
            self.profile_card,
            text="🌐 Open GitHub Profile",
            command=self.open_profile,
            state="disabled",
            font=("Segoe UI", 10, "bold"),
            bg="#e7d4ff",
            fg="#7041a5",
            activebackground="#d8bdf8",
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=8
        )
        self.profile_button.pack(pady=12)

        # Status
        self.status_label = tk.Label(
            self.root,
            text="🌸 Ready to search",
            font=("Segoe UI", 9),
            fg="#d45b7b",
            bg="#fff5f8"
        )
        self.status_label.pack(pady=8)

        # Store profile URL
        self.profile_url = None

    # =========================================================
    # STAT CARD
    # =========================================================

    def create_stat(self, parent, icon, title):

        frame = tk.Frame(
            parent,
            bg="#fff5f8"
        )
        frame.pack(
            side="left",
            expand=True,
            fill="x",
            padx=8,
            pady=10
        )

        value = tk.Label(
            frame,
            text="—",
            font=("Segoe UI", 18, "bold"),
            fg="#e83e72",
            bg="#fff5f8"
        )
        value.pack()

        tk.Label(
            frame,
            text=f"{icon} {title}",
            font=("Segoe UI", 9),
            fg="#777777",
            bg="#fff5f8"
        ).pack()

        return value

    # =========================================================
    # SEARCH
    # =========================================================

    def start_search(self):

        username = self.username_entry.get().strip()

        if not username:
            messagebox.showwarning(
                "Oops! 🌸",
                "Please enter a GitHub username."
            )
            return

        self.search_button.config(
            state="disabled"
        )

        self.status_label.config(
            text="🔎 Searching GitHub..."
        )

        thread = threading.Thread(
            target=self.search_user,
            args=(username,),
            daemon=True
        )

        thread.start()

    def search_user(self, username):

        try:

            url = f"https://api.github.com/users/{username}"

            response = requests.get(
                url,
                timeout=10,
                headers={
                    "Accept": "application/vnd.github+json"
                }
            )

            if response.status_code == 404:
                self.root.after(
                    0,
                    lambda: self.show_error(
                        "User not found 😢\n"
                        "Please check the username."
                    )
                )
                return

            response.raise_for_status()

            data = response.json()

            self.root.after(
                0,
                lambda: self.display_profile(data)
            )

        except requests.exceptions.Timeout:

            self.root.after(
                0,
                lambda: self.show_error(
                    "Request timed out ⏳\n"
                    "Please try again."
                )
            )

        except requests.exceptions.ConnectionError:

            self.root.after(
                0,
                lambda: self.show_error(
                    "No internet connection 🌐\n"
                    "Please check your connection."
                )
            )

        except requests.exceptions.RequestException:

            self.root.after(
                0,
                lambda: self.show_error(
                    "Something went wrong.\n"
                    "Please try again later."
                )
            )

    # =========================================================
    # DISPLAY PROFILE
    # =========================================================

    def display_profile(self, data):

        self.search_button.config(
            state="normal"
        )

        self.status_label.config(
            text="💗 Profile found successfully!"
        )

        # Name
        name = data.get("name") or "No name available"

        self.name_label.config(
            text=name
        )

        # Username
        login = data.get(
            "login",
            "unknown"
        )

        self.username_label.config(
            text=f"@{login}"
        )

        # Bio
        bio = data.get("bio")

        if not bio:
            bio = "No bio available."

        self.bio_label.config(
            text=bio
        )

        # Stats
        self.repo_label.config(
            text=str(
                data.get(
                    "public_repos",
                    0
                )
            )
        )

        self.followers_label.config(
            text=str(
                data.get(
                    "followers",
                    0
                )
            )
        )

        self.following_label.config(
            text=str(
                data.get(
                    "following",
                    0
                )
            )
        )

        # Location
        location = data.get("location")

        self.location_label.config(
            text=f"📍 Location: {location or 'Not available'}"
        )

        # Website
        website = data.get("blog")

        if website:
            website_text = website
        else:
            website_text = "Not available"

        self.website_label.config(
            text=f"🌐 Website: {website_text}"
        )

        # Joined date
        created = data.get("created_at")

        if created:
            try:
                date = datetime.strptime(
                    created,
                    "%Y-%m-%dT%H:%M:%SZ"
                ).strftime("%d %B %Y")

            except ValueError:
                date = created

        else:
            date = "Unknown"

        self.joined_label.config(
            text=f"📅 Joined: {date}"
        )

        # Profile URL
        self.profile_url = data.get(
            "html_url"
        )

        self.profile_button.config(
            state="normal"
        )

        # Avatar
        avatar_url = data.get(
            "avatar_url"
        )

        if avatar_url:
            self.load_avatar(avatar_url)

    # =========================================================
    # AVATAR
    # =========================================================

    def load_avatar(self, avatar_url):

        try:

            response = requests.get(
                avatar_url,
                timeout=10
            )

            response.raise_for_status()

            image = Image.open(
                BytesIO(response.content)
            )

            image = image.resize(
                (130, 130)
            )

            self.avatar_image = ImageTk.PhotoImage(
                image
            )

            self.avatar_label.config(
                image=self.avatar_image,
                text=""
            )

        except Exception:
            self.avatar_label.config(
                image="",
                text="👤"
            )

    # =========================================================
    # ERROR
    # =========================================================

    def show_error(self, message):

        self.search_button.config(
            state="normal"
        )

        self.status_label.config(
            text="❌ Search failed"
        )

        messagebox.showerror(
            "GitHub Profile Finder",
            message
        )

    # =========================================================
    # OPEN PROFILE
    # =========================================================

    def open_profile(self):

        if self.profile_url:
            webbrowser.open(
                self.profile_url
            )


# =============================================================
# IMPORTS
# =============================================================

from datetime import datetime


# =============================================================
# START APP
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = GitHubProfileFinder(
        root
    )

    root.mainloop()