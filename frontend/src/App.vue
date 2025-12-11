<script setup lang="ts">
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'

const router = useRouter()
const sleighX = ref(0)
const sleighY = ref(0)
const isPlaying = ref(false)
const audioPlayer = ref<HTMLAudioElement | null>(null)
const username = ref<string | null>(null)
const showProfileDropdown = ref(false)

const isLoggedIn = computed(() => !!username.value)

function handleMouseMove(event: MouseEvent) {
  sleighX.value = event.clientX
  sleighY.value = event.clientY
}

function toggleMusic() {
  if (audioPlayer.value) {
    if (isPlaying.value) {
      audioPlayer.value.pause()
    } else {
      audioPlayer.value.play()
    }
    isPlaying.value = !isPlaying.value
  }
}

function logout() {
  localStorage.removeItem('bearerToken')
  localStorage.removeItem('username')
  username.value = null
  showProfileDropdown.value = false
  router.push('/login')
}

function toggleProfileDropdown() {
  showProfileDropdown.value = !showProfileDropdown.value
}

function checkAuth() {
  username.value = localStorage.getItem('username')
  console.log('Auth check - username:', username.value, 'token exists:', !!localStorage.getItem('bearerToken'))
  
  // If we have a token but no username, it means user logged in before the update
  // We should clear everything to force a fresh login
  if (localStorage.getItem('bearerToken') && !username.value) {
    console.log('Found token without username - clearing for fresh login')
    localStorage.removeItem('bearerToken')
  }
}

// Watch for route changes to update auth immediately
watch(() => router.currentRoute.value.path, () => {
  checkAuth()
})

onMounted(() => {
  window.addEventListener('mousemove', handleMouseMove)
  checkAuth()
  // Check auth on storage changes (e.g., login in another tab)
  window.addEventListener('storage', checkAuth)
  
  // Also check when route changes (in case user logs in)
  router.afterEach(() => {
    checkAuth()
  })
})

onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove)
  window.removeEventListener('storage', checkAuth)
})
</script>

<template>
  <div id="app">
    <header>
      <div class="mascot-background" />
      <div class="header-content">
        <div class="brand">
          <div class="mascot-logo">
            <img src="/mascot/mascot-action.png" alt="Team Blue Mascot" class="mascot-icon">
          </div>
          <div class="brand-text">
            <h1>Team Blue</h1>
            <span class="subtitle">Asset Management</span>
          </div>
        </div>
        <nav>
          <RouterLink to="/">
            🏠 Home
          </RouterLink>
          <RouterLink to="/mascot-theme">
            🎖️ Our Hero
          </RouterLink>
          <RouterLink v-if="!isLoggedIn" to="/login">
            🔐 Login
          </RouterLink>
          <RouterLink to="/assets">
            🎁 Assets
          </RouterLink>
          <RouterLink to="/add-asset">
            ➕ Add Asset
          </RouterLink>
          <RouterLink to="/employees">
            👥 Employees
          </RouterLink>
          <RouterLink to="/about">
            🎄 About Us
          </RouterLink>
        </nav>
      </div>
    </header>

    <!-- Profile Dropdown Button (Fixed Position) -->
    <div v-if="isLoggedIn" class="profile-container">
      <button class="profile-btn" @click="toggleProfileDropdown">
        <span class="profile-icon">👤</span>
      </button>
      <div v-if="showProfileDropdown" class="profile-dropdown">
        <div class="profile-header">
          <span class="profile-username">{{ username }}</span>
        </div>
        <button class="dropdown-logout-btn" @click="logout">
          🚪 Logout
        </button>
      </div>
    </div>

    <main>
      <div class="mascot-watermark" />
      <div class="snowflakes" aria-hidden="true">
        <div class="snowflake">
          ❅
        </div>
        <div class="snowflake">
          ❆
        </div>
        <div class="snowflake">
          ❅
        </div>
        <div class="snowflake">
          ❆
        </div>
        <div class="snowflake">
          ❅
        </div>
        <div class="snowflake">
          ❆
        </div>
      </div>
      
      <!-- Sleigh Cursor Follower -->
      <div 
        class="sleigh-cursor" 
        :style="{ left: (sleighX - 40) + 'px', top: (sleighY + 40) + 'px' }"
        aria-hidden="true"
      >
        <img src="/mascot/SwabRidingSleigh.png" alt="Santa Swab on Sleigh">
      </div>
      
      <!-- Music Player -->
      <audio ref="audioPlayer" loop>
        <source src="/Music/Buble.mp3" type="audio/mpeg">
      </audio>
      
      <button class="music-toggle" :class="{ playing: isPlaying }" @click="toggleMusic">
        <span v-if="isPlaying">🎵</span>
        <span v-else>🔇</span>
      </button>
      
      <RouterView />
    </main>
    
    <footer class="app-footer">
      <div class="footer-mascot">
        <img src="/mascot/SantaSwab.png" alt="Santa Swab">
      </div>
      <p>🎄 Team Blue Asset Management System - Ho Ho Ho! Merry Christmas! 🎅</p>
    </footer>
  </div>
</template>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: relative;
}

header {
  background: linear-gradient(135deg, #c41e3a 0%, #165b33 50%, #c41e3a 100%);
  color: white;
  box-shadow: 0 4px 20px rgba(196, 30, 58, 0.4);
  padding: 1.5rem 2rem;
  position: relative;
  overflow: hidden;
  border-bottom: 4px solid #ffd700;
}

.mascot-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 20% 50%, rgba(255, 215, 0, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255, 255, 255, 0.05) 10px, rgba(255, 255, 255, 0.05) 20px);
  pointer-events: none;
  animation: snowfall 20s linear infinite;
}

@keyframes snowfall {
  0% { background-position: 0 0; }
  100% { background-position: 0 100px; }
}

.header-content {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  position: relative;
  z-index: 1;
}

.brand {
  display: flex;
  align-items: center;
  gap: 1rem;
  animation: slideInLeft 0.6s ease-out;
}

.mascot-logo {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid #ffd700;
  box-shadow: 0 0 25px rgba(255, 215, 0, 0.6), 0 0 15px rgba(196, 30, 58, 0.4);
  transition: all 0.3s ease;
  background: white;
  animation: christmasGlow 2s ease-in-out infinite;
}

@keyframes christmasGlow {
  0%, 100% {
    box-shadow: 0 0 25px rgba(255, 215, 0, 0.6), 0 0 15px rgba(196, 30, 58, 0.4);
  }
  50% {
    box-shadow: 0 0 35px rgba(255, 215, 0, 0.8), 0 0 25px rgba(22, 91, 51, 0.6);
  }
}

.mascot-logo:hover {
  transform: rotate(360deg) scale(1.1);
  border-color: #c41e3a;
  box-shadow: 0 0 40px rgba(255, 215, 0, 0.9), 0 0 30px rgba(196, 30, 58, 0.7);
}

.mascot-icon {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand h1 {
  font-size: 1.75rem;
  font-weight: 800;
  margin: 0;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  letter-spacing: 0.5px;
}

.subtitle {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1px;
}

nav {
  display: flex;
  gap: 0.5rem;
  animation: slideInRight 0.6s ease-out;
}

nav a {
  color: rgba(255, 255, 255, 0.95);
  padding: 0.625rem 1.25rem;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  border: 2px solid transparent;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

nav a:hover {
  background-color: rgba(255, 215, 0, 0.25);
  border-color: #ffd700;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(196, 30, 58, 0.3);
}

nav a.router-link-exact-active {
  background: linear-gradient(135deg, #c41e3a 0%, #165b33 100%);
  border-color: #ffd700;
  color: white;
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.5);
}

.profile-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 10000;
}

.profile-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #c41e3a 0%, #165b33 100%);
  border: 3px solid #ffd700;
  color: white;
  font-size: 1.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(196, 30, 58, 0.4), 0 0 20px rgba(255, 215, 0, 0.3);
  animation: christmasGlow 2s ease-in-out infinite;
}

.profile-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(196, 30, 58, 0.5), 0 0 30px rgba(255, 215, 0, 0.5);
}

.profile-icon {
  line-height: 1;
}

.profile-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  min-width: 200px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  border: 3px solid #ffd700;
  overflow: hidden;
  animation: dropdownSlide 0.3s ease-out;
}

@keyframes dropdownSlide {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.profile-header {
  padding: 1rem;
  background: linear-gradient(135deg, #c41e3a 0%, #165b33 100%);
  border-bottom: 2px solid #ffd700;
}

.profile-username {
  color: white;
  font-weight: 700;
  font-size: 1rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.profile-username::before {
  content: '👤';
  font-size: 1.2rem;
}

.dropdown-logout-btn {
  width: 100%;
  background: white;
  color: #c41e3a;
  border: none;
  padding: 0.875rem 1rem;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.dropdown-logout-btn:hover {
  background: linear-gradient(135deg, #c41e3a 0%, #8b0000 100%);
  color: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

main {
  flex: 1;
  padding: 2rem;
  max-width: 1280px;
  margin: 0 auto;
  width: 100%;
  position: relative;
  animation: fadeIn 0.8s ease-out;
}

.mascot-watermark {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 120px;
  height: 120px;
  background-image: url('/mascot/SantaSwab.png');
  background-size: cover;
  background-position: center;
  opacity: 0.12;
  pointer-events: none;
  border-radius: 50%;
  z-index: 0;
  animation: float 6s ease-in-out infinite;
  filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.3));
}

.mascot-watermark::before {
  content: '❄️';
  position: absolute;
  top: -20px;
  right: -20px;
  font-size: 2rem;
  animation: snowflakeSpin 4s linear infinite;
}

@keyframes snowflakeSpin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Sleigh Cursor Follower */
.sleigh-cursor {
  position: fixed;
  width: 80px;
  height: 80px;
  pointer-events: none;
  z-index: 9999;
  transform: translate(-50%, -50%);
  transition: left 0.15s ease-out, top 0.15s ease-out;
}

.sleigh-cursor img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.3));
  animation: sleighBounce 0.5s ease-in-out infinite;
}

@keyframes sleighBounce {
  0%, 100% {
    transform: translateY(0) rotate(-5deg);
  }
  50% {
    transform: translateY(-3px) rotate(-5deg);
  }
}

/* Music Toggle Button */
.music-toggle {
  position: fixed;
  bottom: 30px;
  left: 30px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #c41e3a 0%, #165b33 100%);
  border: 3px solid #ffd700;
  color: white;
  font-size: 1.75rem;
  cursor: pointer;
  z-index: 9998;
  box-shadow: 0 4px 12px rgba(196, 30, 58, 0.4), 0 0 20px rgba(255, 215, 0, 0.3);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.music-toggle:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(196, 30, 58, 0.5), 0 0 30px rgba(255, 215, 0, 0.5);
}

.music-toggle.playing {
  animation: musicPulse 1s ease-in-out infinite;
}

@keyframes musicPulse {
  0%, 100% {
    box-shadow: 0 4px 12px rgba(196, 30, 58, 0.4), 0 0 20px rgba(255, 215, 0, 0.3);
  }
  50% {
    box-shadow: 0 6px 16px rgba(196, 30, 58, 0.6), 0 0 30px rgba(255, 215, 0, 0.6);
  }
}

.app-footer {
  background: linear-gradient(to top, #165b33 0%, #c41e3a 100%);
  color: white;
  padding: 2rem;
  text-align: center;
  border-top: 4px solid #ffd700;
  position: relative;
  overflow: hidden;
}

.app-footer::before {
  content: '🎄 ❄️ 🎁 ⭐ 🔔 ❄️ 🎄';
  position: absolute;
  top: 0.5rem;
  left: 50%;
  transform: translateX(-50%);
  font-size: 1.2rem;
  opacity: 0.6;
}

.footer-mascot {
  width: 80px;
  height: 80px;
  margin: 0 auto 1rem;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid #ffd700;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
  animation: christmasGlow 2s ease-in-out infinite;
}

.footer-mascot img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.app-footer p {
  margin: 0;
  font-weight: 500;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(5deg);
  }
}

/* Christmas snowflakes ❄️ */
.snowflakes {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
  overflow: hidden;
}

.snowflake {
  position: absolute;
  top: -10%;
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.5rem;
  animation: snowfall-anim 10s linear infinite;
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
}

.snowflake:nth-child(1) {
  left: 10%;
  animation-duration: 12s;
  animation-delay: 0s;
  font-size: 1.2rem;
}

.snowflake:nth-child(2) {
  left: 30%;
  animation-duration: 10s;
  animation-delay: 2s;
  font-size: 1.8rem;
}

.snowflake:nth-child(3) {
  left: 50%;
  animation-duration: 14s;
  animation-delay: 1s;
  font-size: 1.5rem;
}

.snowflake:nth-child(4) {
  left: 70%;
  animation-duration: 11s;
  animation-delay: 3s;
  font-size: 1.3rem;
}

.snowflake:nth-child(5) {
  left: 85%;
  animation-duration: 13s;
  animation-delay: 0.5s;
  font-size: 1.6rem;
}

.snowflake:nth-child(6) {
  left: 20%;
  animation-duration: 15s;
  animation-delay: 2.5s;
  font-size: 1.4rem;
}

@keyframes snowfall-anim {
  0% {
    transform: translateY(0) rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: translateY(100vh) rotate(360deg);
    opacity: 0.5;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }

  nav {
    width: 100%;
    flex-wrap: wrap;
  }

  .brand h1 {
    font-size: 1.5rem;
  }

  .mascot-logo {
    width: 50px;
    height: 50px;
  }

  .mascot-watermark {
    width: 80px;
    height: 80px;
  }

  .profile-btn {
    width: 50px;
    height: 50px;
    font-size: 1.4rem;
  }

  .profile-container {
    top: 15px;
    right: 15px;
  }

  .profile-dropdown {
    right: 0;
    min-width: 180px;
  }
}
</style>
