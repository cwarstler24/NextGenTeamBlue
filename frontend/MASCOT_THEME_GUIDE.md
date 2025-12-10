# Team Blue Mascot Theme Setup Guide

## 🎖️ Overview
Your frontend now features a complete mascot-themed design inspired by your action hero spoon character!

## 📸 Image Setup

**IMPORTANT**: Save your 3 mascot images to the following location with these exact names:

```
frontend/public/mascot/
├── mascot-hero.png      (Helicopter rescue scene - first image)
├── mascot-action.png    (Jungle/explosions scene - second image)
└── mascot-portrait.png  (Alternative pose - third image)
```

Without these images, you'll see broken image links. Simply save the 3 images you provided with these names.

## 🎨 Theme Features

### Color Palette
- **Mascot Teal**: `#14b8a6` - Primary brand color inspired by the mascot's color
- **Action Orange**: `#fb923c` - Explosive action accents from the backgrounds
- **Sky Blue**: `#0ea5e9` - Sky and water tones
- **Danger Red**: `#dc2626` - Red bandana accent
- **Military Olive**: `#4a5525` - Tactical gear inspiration

### Design Elements

1. **Animated Header**
   - Rotating mascot logo on hover
   - Gradient background with teal → sky blue
   - Orange border accents
   - Smooth slide-in animations

2. **Hero Sections**
   - Gradient backgrounds matching mascot themes
   - Floating animations
   - Action-packed color schemes

3. **Buttons**
   - Gradient fills with ripple effects
   - Hover transforms to action orange
   - Pulse animations for action buttons
   - Upper-case military-style text

4. **Cards**
   - Gradient top borders (teal → orange → blue)
   - Hover elevation effects
   - Clean, modern design

5. **Tables**
   - Gradient headers
   - Smooth hover transitions
   - Polished professional look

6. **Footer**
   - Circular mascot portrait
   - Teal gradient background
   - Orange accent border

### New Features

#### Mascot Showcase Page
Visit `/mascot-theme` to see:
- All three mascot images in action
- Color palette showcase
- Button style demos
- Interactive hover effects

#### Watermark
- Subtle floating mascot watermark in bottom-right corner
- Gentle floating animation

## 🚀 Running the Application

```bash
cd frontend
npm install
npm run dev
```

Then navigate to:
- Main app: `http://localhost:5173/`
- Mascot theme page: `http://localhost:5173/mascot-theme`

## 🎯 Usage Tips

### Custom Button Styles
```html
<!-- Standard themed button -->
<button>Standard Button</button>

<!-- Action emphasis button -->
<button class="action-button">Action Button</button>
```

### Using Cards
```html
<div class="card">
  <!-- Your content -->
</div>
```

### Hero Sections
```html
<div class="hero-section">
  <h1>Your Title</h1>
  <p>Your content</p>
</div>
```

### Badges
```html
<span class="badge">Status</span>
<span class="badge action">Action</span>
```

## 🎨 Customization

All theme colors are defined in `frontend/src/assets/base.css`:

```css
--vt-c-primary: #14b8a6;        /* Mascot teal */
--vt-c-action-orange: #fb923c;   /* Action orange */
--vt-c-sky: #0ea5e9;            /* Sky blue */
--vt-c-danger: #dc2626;         /* Danger red */
--vt-c-military: #4a5525;       /* Military olive */
```

## 📱 Responsive Design

The theme is fully responsive and includes:
- Mobile-optimized navigation
- Flexible grid layouts
- Touch-friendly button sizes
- Adaptive mascot sizes

## ✨ Animation Classes

Add these classes to any element:
- `.animate-in` - Slide up fade-in animation
- Add `animation-delay` style for staggered effects

Example:
```html
<div class="card animate-in" style="animation-delay: 0.2s">
  <!-- Content -->
</div>
```

## 🎖️ Enjoy Your New Theme!

Your application now has a unique, action-packed identity centered around your awesome mascot. The teal, orange, and blue color scheme creates a dynamic, energetic feel perfect for an asset management system with personality!
