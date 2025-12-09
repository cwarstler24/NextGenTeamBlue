<template>
  <div class="mascot-showcase">
    <div class="hero-section animate-in">
      <div class="hero-content">
        <h1>🎖️ Meet Our Hero</h1>
        <p>Protecting assets with style and courage!</p>
      </div>
    </div>

    <div class="mascot-gallery">
      <div class="card mascot-card animate-in" style="animation-delay: 0.1s">
        <div class="mascot-image-container">
          <img src="/mascot/mascot-hero.png" alt="Helicopter Rescue Hero" />
        </div>
        <h3>🚁 Rescue Operations</h3>
        <p>Always ready to save the day and secure your assets!</p>
        <span class="badge">Hero Mode</span>
      </div>

      <div class="card mascot-card animate-in" style="animation-delay: 0.2s">
        <div class="mascot-image-container">
          <img src="/mascot/mascot-action.png" alt="Action Hero" />
        </div>
        <h3>💥 Action Ready</h3>
        <p>Armed with the best asset management tools!</p>
        <span class="badge action">Combat Ready</span>
      </div>

      <div class="card mascot-card animate-in" style="animation-delay: 0.3s">
        <div class="mascot-image-container">
          <img src="/mascot/mascot-portrait.png" alt="Team Leader" />
        </div>
        <h3>😎 Team Leader</h3>
        <p>Leading Team Blue to victory in asset management!</p>
        <span class="badge">Commander</span>
      </div>
    </div>

    <div class="theme-preview animate-in" style="animation-delay: 0.4s">
      <h2>🎨 Theme Colors</h2>
      <div class="color-palette">
        <div class="color-swatch teal">
          <div class="swatch"></div>
          <span>Mascot Teal</span>
        </div>
        <div class="color-swatch orange">
          <div class="swatch"></div>
          <span>Action Orange</span>
        </div>
        <div class="color-swatch sky">
          <div class="swatch"></div>
          <span>Sky Blue</span>
        </div>
        <div class="color-swatch danger">
          <div class="swatch"></div>
          <span>Danger Red</span>
        </div>
      </div>
    </div>

    <div class="button-showcase animate-in" style="animation-delay: 0.5s">
      <h2>🎯 Action Buttons</h2>
      <div class="button-grid">
        <button>Standard Button</button>
        <button class="action-button">Action Button</button>
        <button disabled>Disabled Button</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Mascot showcase component
</script>

<style scoped>
.mascot-showcase {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-content h1 {
  font-size: 2.5rem;
  margin: 0 0 1rem 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.hero-content p {
  font-size: 1.25rem;
  margin: 0;
  opacity: 0.95;
}

.mascot-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.mascot-card {
  text-align: center;
  padding: 2rem;
}

.mascot-image-container {
  width: 200px;
  height: 200px;
  margin: 0 auto 1.5rem;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid #fb923c;
  box-shadow: 0 8px 16px rgba(251, 146, 60, 0.3);
  transition: all 0.3s ease;
}

.mascot-image-container:hover {
  transform: scale(1.1) rotate(5deg);
  border-color: #14b8a6;
  box-shadow: 0 12px 24px rgba(20, 184, 166, 0.4);
}

.mascot-image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mascot-card h3 {
  color: #0f766e;
  margin: 1rem 0 0.5rem 0;
  font-size: 1.25rem;
}

.mascot-card p {
  color: #6b7280;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.theme-preview {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.theme-preview h2 {
  color: #0f766e;
  margin: 0 0 1.5rem 0;
  text-align: center;
}

.color-palette {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
}

.color-swatch {
  text-align: center;
}

.swatch {
  width: 80px;
  height: 80px;
  margin: 0 auto 0.5rem;
  border-radius: 50%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.swatch:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.color-swatch.teal .swatch {
  background: linear-gradient(135deg, #14b8a6 0%, #0f766e 100%);
}

.color-swatch.orange .swatch {
  background: linear-gradient(135deg, #fb923c 0%, #ea580c 100%);
}

.color-swatch.sky .swatch {
  background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
}

.color-swatch.danger .swatch {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
}

.color-swatch span {
  font-size: 0.875rem;
  color: #4b5563;
  font-weight: 600;
}

.button-showcase {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.button-showcase h2 {
  color: #0f766e;
  margin: 0 0 1.5rem 0;
  text-align: center;
}

.button-grid {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2rem;
  }

  .mascot-gallery {
    grid-template-columns: 1fr;
  }

  .mascot-image-container {
    width: 150px;
    height: 150px;
  }

  .button-grid {
    flex-direction: column;
  }
}
</style>
