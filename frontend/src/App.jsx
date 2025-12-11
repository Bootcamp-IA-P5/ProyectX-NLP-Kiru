import { useState } from 'react'
import { ThemeProvider, useTheme } from './context/ThemeContext'
import VideoAnalyzer from './components/VideoAnalyzer'
import TextPredictor from './components/TextPredictor'
import ModelComparison from './components/ModelComparison'
import ModelMetrics from './pages/ModelMetrics'

function AppContent() {
  const [activeTab, setActiveTab] = useState('video')
  const { isDark, toggleTheme } = useTheme()

  return (
    <div className={`min-h-screen ${isDark ? 'bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900' : 'bg-gradient-to-br from-gray-100 via-purple-100 to-gray-100'}`}>
      <div className="container mx-auto px-4 py-8">
        {/* Header con Badge del Modelo */}
        <header className="text-center mb-12">
          <div className="flex justify-between items-center mb-4">
            <div className="flex-1"></div>
            <div className="flex-1 flex justify-center">
              <span className={`inline-block bg-gradient-to-r from-purple-600 to-pink-600 text-white px-4 py-2 rounded-full text-sm font-semibold animate-pulse`}>
                🤖 Powered by DistilBERT - 88% Accuracy
              </span>
            </div>
            {/* Toggle de Tema */}
            <div className="flex-1 flex justify-end">
              <button
                onClick={toggleTheme}
                className={`p-3 rounded-lg transition-all transform hover:scale-110 ${
                  isDark 
                    ? 'bg-gray-800 text-yellow-400 hover:bg-gray-700' 
                    : 'bg-white text-gray-800 hover:bg-gray-100 shadow-lg'
                }`}
                title={isDark ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'}
              >
                {isDark ? (
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                ) : (
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                  </svg>
                )}
              </button>
            </div>
          </div>
          
          <h1 className={`text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r ${
            isDark ? 'from-blue-400 to-purple-400' : 'from-blue-600 to-purple-600'
          }`}>
            🛡️ YouTube Hate Speech Detector
          </h1>
          <p className={`text-xl ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
            Detección automática de mensajes de odio usando IA
          </p>
          
          {/* Métricas del Modelo */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8 max-w-3xl mx-auto">
            <div className={`rounded-lg p-4 backdrop-blur-sm ${
              isDark ? 'bg-gray-800 bg-opacity-50' : 'bg-white bg-opacity-70 shadow-lg'
            }`}>
              <div className="text-3xl font-bold text-blue-400">88%</div>
              <div className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Accuracy</div>
            </div>
            <div className={`rounded-lg p-4 backdrop-blur-sm ${
              isDark ? 'bg-gray-800 bg-opacity-50' : 'bg-white bg-opacity-70 shadow-lg'
            }`}>
              <div className="text-3xl font-bold text-green-400">88%</div>
              <div className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>F1-Score</div>
            </div>
            <div className={`rounded-lg p-4 backdrop-blur-sm ${
              isDark ? 'bg-gray-800 bg-opacity-50' : 'bg-white bg-opacity-70 shadow-lg'
            }`}>
              <div className="text-3xl font-bold text-purple-400">66M</div>
              <div className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Parámetros</div>
            </div>
            <div className={`rounded-lg p-4 backdrop-blur-sm ${
              isDark ? 'bg-gray-800 bg-opacity-50' : 'bg-white bg-opacity-70 shadow-lg'
            }`}>
              <div className="text-3xl font-bold text-yellow-400">3.3%</div>
              <div className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Overfitting</div>
            </div>
          </div>
        </header>

        {/* Navegación con nuevas opciones */}
        <nav className="flex flex-wrap justify-center gap-4 mb-8">
          <button 
            className={`px-6 py-3 rounded-lg font-semibold transition-all transform hover:scale-105 ${
              activeTab === 'video' 
                ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/50' 
                : isDark
                  ? 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                  : 'bg-white text-gray-700 hover:bg-gray-100 shadow'
            }`}
            onClick={() => setActiveTab('video')}
          >
            📹 Analizar Video
          </button>
          <button 
            className={`px-6 py-3 rounded-lg font-semibold transition-all transform hover:scale-105 ${
              activeTab === 'text' 
                ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/50' 
                : isDark
                  ? 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                  : 'bg-white text-gray-700 hover:bg-gray-100 shadow'
            }`}
            onClick={() => setActiveTab('text')}
          >
            💬 Analizar Texto
          </button>
          <button 
            className={`px-6 py-3 rounded-lg font-semibold transition-all transform hover:scale-105 ${
              activeTab === 'compare' 
                ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/50' 
                : isDark
                  ? 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                  : 'bg-white text-gray-700 hover:bg-gray-100 shadow'
            }`}
            onClick={() => setActiveTab('compare')}
          >
            ⚖️ Comparar Modelos
          </button>
          <button 
            className={`px-6 py-3 rounded-lg font-semibold transition-all transform hover:scale-105 ${
              activeTab === 'metrics' 
                ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/50' 
                : isDark
                  ? 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                  : 'bg-white text-gray-700 hover:bg-gray-100 shadow'
            }`}
            onClick={() => setActiveTab('metrics')}
          >
            📊 Métricas
          </button>
        </nav>

        {/* Contenido Principal */}
        <main className="max-w-6xl mx-auto">
          {activeTab === 'video' && <VideoAnalyzer />}
          {activeTab === 'text' && <TextPredictor />}
          {activeTab === 'compare' && <ModelComparison />}
          {activeTab === 'metrics' && <ModelMetrics />}
        </main>

        {/* Footer */}
        <footer className={`text-center mt-16 pt-8 ${
          isDark ? 'border-gray-700' : 'border-gray-300'
        } border-t`}>
          <div className="flex justify-center gap-6 mb-4">
            <a 
              href="https://github.com/Bootcamp-IA-P5/ProyectX-NLP-Kiru" 
              target="_blank"
              rel="noopener noreferrer"
              className={`${
                isDark ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'
              } transition-colors flex items-center gap-2`}
            >
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              GitHub
            </a>
            <a 
              href="https://youtube-hate-speech-detector.onrender.com/docs" 
              target="_blank"
              rel="noopener noreferrer"
              className={`${
                isDark ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'
              } transition-colors`}
            >
              📚 API Docs
            </a>
          </div>
          <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
            Proyecto Bootcamp IA - Factoría F5 | Powered by DistilBERT & FastAPI
          </p>
        </footer>
      </div>
    </div>
  )
}

// App principal con ThemeProvider
function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  )
}

export default App