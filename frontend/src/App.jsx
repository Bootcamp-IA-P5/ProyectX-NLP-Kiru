import { useState } from 'react'
import VideoAnalyzer from './components/VideoAnalyzer'
import TextPredictor from './components/TextPredictor'

function App() {
  const [activeTab, setActiveTab] = useState('video')

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header con Badge del Modelo */}
        <header className="text-center mb-12">
          <div className="mb-4">
            <span className="inline-block bg-gradient-to-r from-purple-600 to-pink-600 text-white px-4 py-2 rounded-full text-sm font-semibold mb-4 animate-pulse">
              🤖 Powered by DistilBERT - 88% Accuracy
            </span>
          </div>
          <h1 className="text-5xl font-bold text-white mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
            🛡️ YouTube Hate Speech Detector
          </h1>
          <p className="text-xl text-gray-300">
            Detección automática de mensajes de odio usando IA
          </p>
          
          {/* Métricas del Modelo */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8 max-w-3xl mx-auto">
            <div className="bg-gray-800 bg-opacity-50 rounded-lg p-4 backdrop-blur-sm">
              <div className="text-3xl font-bold text-blue-400">88%</div>
              <div className="text-sm text-gray-400">Accuracy</div>
            </div>
            <div className="bg-gray-800 bg-opacity-50 rounded-lg p-4 backdrop-blur-sm">
              <div className="text-3xl font-bold text-green-400">87.4%</div>
              <div className="text-sm text-gray-400">F1-Score</div>
            </div>
            <div className="bg-gray-800 bg-opacity-50 rounded-lg p-4 backdrop-blur-sm">
              <div className="text-3xl font-bold text-purple-400">66M</div>
              <div className="text-sm text-gray-400">Parámetros</div>
            </div>
            <div className="bg-gray-800 bg-opacity-50 rounded-lg p-4 backdrop-blur-sm">
              <div className="text-3xl font-bold text-yellow-400">&lt;3%</div>
              <div className="text-sm text-gray-400">Overfitting</div>
            </div>
          </div>
        </header>

        <nav className="flex justify-center gap-4 mb-8">
          <button 
            className={`px-8 py-3 rounded-lg font-semibold transition-all transform hover:scale-105 ${
              activeTab === 'video' 
                ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/50' 
                : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
            }`}
            onClick={() => setActiveTab('video')}
          >
            📹 Analizar Video
          </button>
          <button 
            className={`px-8 py-3 rounded-lg font-semibold transition-all transform hover:scale-105 ${
              activeTab === 'text' 
                ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/50' 
                : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
            }`}
            onClick={() => setActiveTab('text')}
          >
            💬 Analizar Texto
          </button>
        </nav>

        <main className="max-w-6xl mx-auto">
          {activeTab === 'video' ? <VideoAnalyzer /> : <TextPredictor />}
        </main>

        {/* Footer */}
        <footer className="text-center mt-16 border-t border-gray-700 pt-8">
          <div className="flex justify-center gap-6 mb-4">
            <a 
              href="https://github.com/Bootcamp-IA-P5/ProyectX-NLP-Kiru" 
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-400 hover:text-white transition-colors flex items-center gap-2"
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
              className="text-gray-400 hover:text-white transition-colors"
            >
              📚 API Docs
            </a>
          </div>
          <p className="text-gray-400 text-sm">
            Proyecto Bootcamp IA - Factoría F5 | Powered by DistilBERT & FastAPI
          </p>
        </footer>
      </div>
    </div>
  )
}

export default App