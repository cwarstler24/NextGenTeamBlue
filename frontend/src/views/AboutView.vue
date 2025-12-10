<template>
  <div class="about-view">
    <div class="hero-section animate-in">
      <div class="hero-content">
        <h1>🎄 About Team Blue</h1>
        <p>Meet the team behind the magic! ✨</p>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner" />
      <p>Loading team info...</p>
    </div>

    <div v-else-if="error" class="error">
      <h3>❌ Error Loading Content</h3>
      <p>{{ error }}</p>
    </div>

    <div v-else class="content-wrapper animate-in">
      <!-- Mission Statement -->
      <section v-if="missionStatement" class="card mission-card">
        <div class="card-icon">
          🎯
        </div>
        <h2>Our Mission</h2>
        <p class="mission-text">
          {{ missionStatement }}
        </p>
      </section>

      <!-- Development Team -->
      <section v-if="teamMembers.length" class="team-section">
        <h2 class="section-title">
          🎅 Development Team
        </h2>
        <div class="team-grid">
          <div v-for="member in teamMembers" :key="member.title" class="card team-card">
            <div class="member-emoji">
              {{ member.emoji }}
            </div>
            <h3>{{ member.name }}</h3>
            <p class="member-title">
              {{ member.title }}
            </p>
          </div>
        </div>
      </section>

      <!-- Copyright -->
      <section v-if="copyright" class="card copyright-card">
        <div class="card-icon">
          ⚖️
        </div>
        <h2>Copyright & License</h2>
        <div class="copyright-content">
          <pre>{{ copyright }}</pre>
        </div>
      </section>

      <!-- Festive Footer -->
      <div class="festive-footer">
        <p>🎁 Built with ❤️ by Team Blue 🎄</p>
        <p class="year">
          {{ new Date().getFullYear() }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const loading = ref(true)
const error = ref('')
const missionStatement = ref('')
const teamMembers = ref<Array<{ name: string; title: string; emoji: string }>>([])
const copyright = ref('')

const teamEmojiMap: Record<string, string> = {
  'cameron': '🎖️',
  'travis': '🚀',
  'ethan': '🔒',
  'clayton': '🧙',
  'oluwasegun': '🧪',
  'nate': '🗡️'
}

async function fetchAboutUs() {
  try {
    loading.value = true
    error.value = ''
    
    // Fetch the aboutUs.txt file from the backend or public directory
    const response = await fetch('/Documentation/aboutUs.txt')
    
    if (!response.ok) {
      throw new Error('Failed to load about us information')
    }
    
    const text = await response.text()
    parseContent(text)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Unknown error occurred'
    console.error('Error fetching about us:', e)
  } finally {
    loading.value = false
  }
}

function parseContent(text: string) {
  // Extract mission statement
  const missionMatch = text.match(/Mission Statement:\s*"([^"]+)"/s)
  if (missionMatch) {
    missionStatement.value = missionMatch[1]!.trim().replace(/\s+/g, ' ')
  } else {
    // Fallback: try to extract without quotes
    const altMatch = text.match(/Mission Statement:\s*\n(.+?)(?=\n\n|Development Team:)/s)
    if (altMatch) {
      missionStatement.value = altMatch[1]!.trim().replace(/\s+/g, ' ').replace(/^"|"$/g, '')
    }
  }

  // Extract team members
  const teamSection = text.match(/Development Team:(.*?)(?=Copyright Statement:|$)/s)
  if (teamSection) {
    const teamText = teamSection[1]
    const memberLines = teamText!.split('\n').filter(line => line.includes(':'))
    
    teamMembers.value = memberLines.map(line => {
      const [title, name] = line.split(':').map(s => s.trim())
      const firstName = name?.split(' ')[0]?.toLowerCase() || ''
      const emoji = teamEmojiMap[firstName] || '👤'
      
      return {
        name: name || '',
        title: title || '',
        emoji
      }
    }).filter(member => member.name)
  }

  // Extract copyright
  const copyrightMatch = text.match(/Copyright Statement:(.*)/s)
  if (copyrightMatch) {
    copyright.value = copyrightMatch[1]!.trim()
  }
}

onMounted(() => {
  fetchAboutUs()
})
</script>

<style scoped>
.about-view {
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

.loading {
  text-align: center;
  padding: 4rem 2rem;
  color: #165b33;
}

.spinner {
  width: 50px;
  height: 50px;
  margin: 0 auto 1rem;
  border: 4px solid #ffd700;
  border-top-color: #c41e3a;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.content-wrapper {
  animation-delay: 0.2s;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 2px solid #ffd700;
  position: relative;
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #c41e3a 0%, #ffd700 25%, #165b33 50%, #ffd700 75%, #c41e3a 100%);
  background-size: 200% 100%;
  animation: christmasShimmer 3s linear infinite;
}

.card-icon {
  font-size: 3rem;
  text-align: center;
  margin-bottom: 1rem;
}

.mission-card h2 {
  color: #c41e3a;
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 2rem;
  text-shadow: 1px 1px 2px rgba(255, 215, 0, 0.3);
}

.mission-text {
  font-size: 1.125rem;
  line-height: 1.8;
  color: #4b5563;
  text-align: center;
  max-width: 900px;
  margin: 0 auto;
  font-style: italic;
}

.team-section {
  margin-bottom: 2rem;
}

.section-title {
  color: #165b33;
  text-align: center;
  font-size: 2rem;
  margin-bottom: 2rem;
  text-shadow: 1px 1px 2px rgba(255, 215, 0, 0.3);
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.team-card {
  text-align: center;
  padding: 2rem;
  transition: all 0.3s ease;
}

.team-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(196, 30, 58, 0.2), 0 0 20px rgba(255, 215, 0, 0.3);
}

.member-emoji {
  font-size: 4rem;
  margin-bottom: 1rem;
  animation: float 3s ease-in-out infinite;
}

.team-card:nth-child(1) .member-emoji { animation-delay: 0s; }
.team-card:nth-child(2) .member-emoji { animation-delay: 0.5s; }
.team-card:nth-child(3) .member-emoji { animation-delay: 1s; }
.team-card:nth-child(4) .member-emoji { animation-delay: 1.5s; }
.team-card:nth-child(5) .member-emoji { animation-delay: 2s; }

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.team-card h3 {
  color: #c41e3a;
  font-size: 1.25rem;
  margin: 0 0 0.5rem 0;
  font-weight: 700;
}

.member-title {
  color: #165b33;
  font-size: 0.95rem;
  line-height: 1.5;
  font-weight: 600;
  margin: 0;
}

.copyright-card {
  background: #f9fafb;
}

.copyright-card h2 {
  color: #165b33;
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.75rem;
}

.copyright-content {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  overflow-x: auto;
}

.copyright-content pre {
  margin: 0;
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
  line-height: 1.6;
  color: #4b5563;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.festive-footer {
  text-align: center;
  padding: 3rem 1rem;
  margin-top: 2rem;
}

.festive-footer p {
  font-size: 1.25rem;
  color: #c41e3a;
  font-weight: 700;
  margin: 0.5rem 0;
  text-shadow: 1px 1px 2px rgba(255, 215, 0, 0.3);
}

.festive-footer .year {
  color: #165b33;
  font-size: 1rem;
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2rem;
  }

  .team-grid {
    grid-template-columns: 1fr;
  }

  .card {
    padding: 1.5rem;
  }

  .mission-text {
    font-size: 1rem;
  }
}
</style>
