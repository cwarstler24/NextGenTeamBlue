<template>
  <div class="mascot-showcase">
    <div class="hero-section animate-in">
      <div class="hero-content">
        <h1>😎 Meet Swab!</h1>
        <p>Delivering asset management joy this holiday season! 🎄</p>
      </div>
    </div>

    <div class="mascot-gallery">
      <div class="card mascot-card animate-in" style="animation-delay: 0.1s; cursor: pointer;" @click="showHeroVideo = true">
        <div class="mascot-image-container">
          <img src="/mascot/mascot-hero.png" alt="Helicopter Rescue Hero" />
        </div>
        <h3>🚁 Rescue Operations</h3>
        <p>Always ready to save the day and secure your assets!</p>
        <span class="badge">Hero Mode</span>
        <p class="click-hint">👆 Click to watch the rescue!</p>
      </div>

      <div class="card mascot-card animate-in" style="animation-delay: 0.2s; cursor: pointer;" @click="showVideo = true">
        <div class="mascot-image-container">
          <img src="/mascot/mascot-action.png" alt="Action Hero" />
        </div>
        <h3>💥 Action Ready</h3>
        <p>Armed with the best asset management tools!</p>
        <span class="badge action">Combat Ready</span>
        <p class="click-hint">👆 Click to watch the action!</p>
      </div>

      <div class="card mascot-card animate-in" style="animation-delay: 0.3s; cursor: pointer;" @click="showSantaVideo = true">
        <div class="mascot-image-container">
          <img src="/mascot/SantaSwab.png" alt="Santa's Helper" />
        </div>
        <h3>🎁 Santa's Helper</h3>
        <p>Making sure all kids get their presents!</p>
        <span class="badge">Jolly</span>
        <p class="click-hint">👆 Click to see the magic!</p>
      </div>
    </div>

    <div class="theme-preview animate-in" style="animation-delay: 0.4s">
      <h2>🎄 Christmas Theme Colors</h2>
      <div class="color-palette">
        <div class="color-swatch red">
          <div class="swatch"></div>
          <span>Christmas Red</span>
        </div>
        <div class="color-swatch green">
          <div class="swatch"></div>
          <span>Christmas Green</span>
        </div>
        <div class="color-swatch gold">
          <div class="swatch"></div>
          <span>Festive Gold</span>
        </div>
        <div class="color-swatch snow">
          <div class="swatch"></div>
          <span>Snow White</span>
        </div>
      </div>
    </div>

    <div class="button-showcase animate-in" style="animation-delay: 0.5s">
      <h2>🎁 Holiday Buttons</h2>
      <div class="button-grid">
        <button>Standard Button</button>
        <button class="action-button">Action Button</button>
        <button disabled>Disabled Button</button>
      </div>
    </div>

    <!-- Video Modal - Action Hero -->
    <div v-if="showVideo" class="video-modal" @click="showVideo = false">
      <div class="video-container" @click.stop>
        <button class="close-button" @click="showVideo = false">✕</button>
        <h2>🎬 Swab The Leader</h2>
        <video controls autoplay>
          <source src="/mascot/SwabTheLeader.mp4" type="video/mp4">
          Your browser does not support the video tag.
        </video>
      </div>
    </div>

    <!-- Video Modal - Helicopter Hero -->
    <div v-if="showHeroVideo" class="video-modal" @click="showHeroVideo = false">
      <div class="video-container" @click.stop>
        <button class="close-button" @click="showHeroVideo = false">✕</button>
        <h2>🚁 Swab The Savior</h2>
        <video controls autoplay>
          <source src="/mascot/SwabTheSavior.mp4" type="video/mp4">
          Your browser does not support the video tag.
        </video>
      </div>
    </div>

    <!-- Video Modal - Santa's Helper -->
    <div v-if="showSantaVideo" class="video-modal" @click="showSantaVideo = false">
      <div class="video-container" @click.stop>
        <button class="close-button" @click="showSantaVideo = false">✕</button>
        <h2>🎅 Swab The Giver</h2>
        <video controls autoplay>
          <source src="/mascot/SwabTheGiver.mp4" type="video/mp4">
          Your browser does not support the video tag.
        </video>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const showVideo = ref(false)
const showHeroVideo = ref(false)
const showSantaVideo = ref(false)
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
  border: 5px solid #ffd700;
  box-shadow: 0 8px 16px rgba(196, 30, 58, 0.3), 0 0 20px rgba(255, 215, 0, 0.4);
  transition: all 0.3s ease;
  background: white;
}

.mascot-image-container:hover {
  transform: scale(1.1) rotate(5deg);
  border-color: #c41e3a;
  box-shadow: 0 12px 24px rgba(255, 215, 0, 0.6), 0 0 30px rgba(22, 91, 51, 0.5);
}

.mascot-image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mascot-card h3 {
  color: #c41e3a;
  margin: 1rem 0 0.5rem 0;
  font-size: 1.25rem;
  text-shadow: 1px 1px 2px rgba(255, 215, 0, 0.3);
}

.mascot-card p {
  color: #4b5563;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.theme-preview {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 2px solid #ffd700;
}

.theme-preview h2 {
  color: #c41e3a;
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

.color-swatch.red .swatch {
  background: linear-gradient(135deg, #c41e3a 0%, #8b0000 100%);
  box-shadow: 0 4px 8px rgba(196, 30, 58, 0.3);
}

.color-swatch.green .swatch {
  background: linear-gradient(135deg, #165b33 0%, #0f5132 100%);
  box-shadow: 0 4px 8px rgba(22, 91, 51, 0.3);
}

.color-swatch.gold .swatch {
  background: linear-gradient(135deg, #ffd700 0%, #d4af37 100%);
  box-shadow: 0 4px 8px rgba(255, 215, 0, 0.4);
}

.color-swatch.snow .swatch {
  background: linear-gradient(135deg, #ffffff 0%, #e8f4f8 100%);
  border: 2px solid #ddd;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
  border: 2px solid #ffd700;
}

.button-showcase h2 {
  color: #165b33;
  margin: 0 0 1.5rem 0;
  text-align: center;
}

.button-grid {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.click-hint {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #ffd700;
  font-weight: 600;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

/* Video Modal */
.video-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.video-container {
  position: relative;
  background: linear-gradient(135deg, #c41e3a 0%, #165b33 100%);
  padding: 2rem;
  border-radius: 12px;
  max-width: 90vw;
  max-height: 90vh;
  box-shadow: 0 10px 40px rgba(255, 215, 0, 0.3);
  border: 3px solid #ffd700;
}

.video-container h2 {
  color: white;
  text-align: center;
  margin: 0 0 1rem 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.video-container video {
  max-width: 800px;
  max-height: 80vh;
  border-radius: 8px;
  display: block;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.close-button {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: #c41e3a;
  color: white;
  border: 2px solid #ffd700;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  padding: 0;
  line-height: 1;
}

.close-button:hover {
  background: #ffd700;
  color: #1a1a1a;
  transform: rotate(90deg);
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
