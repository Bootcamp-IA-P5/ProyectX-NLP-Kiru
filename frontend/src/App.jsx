import { useState } from 'react'
import VideoAnalyzer from './components/VideoAnalyzer'
import TextPredictor from './components/TextPredictor'

function App() {
  const [activeTab, setActiveTab] = useState('video')

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            🛡️ YouTube Hate Speech Detector
          </h1>
          <p className="text-xl text-gray-300">
            Detección automática de mensajes de odio usando IA
          </p>
        </header>

        <nav className="flex justify-center gap-4 mb-8">
          <button 
            className={`px-8 py-3 rounded-lg font-semibold transition-all ${
              activeTab === 'video' 
                ? 'bg-purple-600 text-white shadow-lg scale-105' 
                : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
            }`}
            onClick={() => setActiveTab('video')}
          >
            📹 Analizar Video
          </button>
          <button 
            className={`px-8 py-3 rounded-lg font-semibold transition-all ${
              activeTab === 'text' 
                ? 'bg-purple-600 text-white shadow-lg scale-105' 
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

        <footer className="text-center mt-16 text-gray-400">
          <p>Proyecto Bootcamp IA - Factoría F5 | Powered by DistilBERT</p>
        </footer>
      </div>
    </div>
  )
}

export default App