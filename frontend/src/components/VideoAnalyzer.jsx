import { useState } from 'react'
import confetti from 'canvas-confetti' 
import api from '../services/api'

// Ejemplos de videos populares
const EXAMPLE_VIDEOS = [
  { title: 'Gangnam Style', url: 'https://www.youtube.com/watch?v=9bZkp7q19f0' },
  { title: 'Baby Shark', url: 'https://www.youtube.com/watch?v=XqZsoesa55w' },
  { title: 'Despacito', url: 'https://www.youtube.com/watch?v=kJQP7kiw5Fk' },
]

function VideoAnalyzer() {
  const [url, setUrl] = useState('')
  const [maxComments, setMaxComments] = useState(50)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleAnalyze = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await api.analyzeVideo(url, maxComments)
      setResult(response)
      
      // Confetti si NO hay comentarios tóxicos
      if (response.toxic_count === 0) {
        confetti({
          particleCount: 150,
          spread: 90,
          origin: { y: 0.6 },
          startVelocity: 45,
          decay: 0.91,
          scalar: 1.2,
          ticks: 200,
          colors: ['#10b981', '#34d399', '#6ee7b7', '#a7f3d0']
        });
      }
      
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al analizar el video')
    } finally {
      setLoading(false)
    }
  }

  const loadExample = (exampleUrl) => {
    setUrl(exampleUrl)
    setError(null)
    setResult(null)
  }

  return (
    <div className="bg-gray-800 rounded-xl shadow-2xl p-8 backdrop-blur-sm bg-opacity-90">
      {/* Ejemplos Rápidos */}
      <div className="mb-6">
        <p className="text-sm text-gray-400 mb-2">⚡ Prueba con estos videos:</p>
        <div className="flex flex-wrap gap-2">
          {EXAMPLE_VIDEOS.map((video) => (
            <button
              key={video.url}
              onClick={() => loadExample(video.url)}
              className="px-4 py-2 bg-gray-700 hover:bg-purple-600 text-gray-300 hover:text-white rounded-lg text-sm transition-colors"
            >
              {video.title}
            </button>
          ))}
        </div>
      </div>

      <form onSubmit={handleAnalyze} className="space-y-6">
        <div>
          <label htmlFor="url" className="block text-sm font-medium text-gray-300 mb-2">
            URL del Video de YouTube
          </label>
          <input
            type="text"
            id="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://www.youtube.com/watch?v=..."
            required
            className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
          />
        </div>

        <div>
          <label htmlFor="maxComments" className="block text-sm font-medium text-gray-300 mb-2">
            Máximo de comentarios: <span className="text-purple-400 font-bold">{maxComments}</span>
          </label>
          <input
            type="range"
            id="maxComments"
            min="10"
            max="200"
            value={maxComments}
            onChange={(e) => setMaxComments(Number(e.target.value))}
            className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-600"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>10</span>
            <span>200</span>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:from-gray-600 disabled:to-gray-600 text-white font-bold py-4 px-6 rounded-lg transition-all transform hover:scale-105 disabled:scale-100 shadow-lg"
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analizando comentarios...
            </span>
          ) : (
            '🔍 Analizar Video'
          )}
        </button>
      </form>

      {error && (
        <div className="mt-6 bg-red-900 border border-red-700 text-red-200 px-4 py-3 rounded-lg animate-pulse">
          ❌ {error}
        </div>
      )}

      {result && (
        <div className="mt-8 space-y-6 animate-fadeIn">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-white mb-2">📊 Resultados del Análisis</h2>
            <h3 className="text-lg text-gray-300">{result.video_title}</h3>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-gradient-to-br from-gray-700 to-gray-800 rounded-lg p-4 text-center transform hover:scale-105 transition-transform">
              <div className="text-3xl font-bold text-white">{result.total_comments_analyzed}</div>
              <div className="text-sm text-gray-400 mt-1">Comentarios</div>
            </div>
            <div className="bg-gradient-to-br from-red-900 to-red-800 rounded-lg p-4 text-center transform hover:scale-105 transition-transform">
              <div className="text-3xl font-bold text-red-200">{result.toxic_count}</div>
              <div className="text-sm text-red-300 mt-1">Tóxicos</div>
            </div>
            <div className="bg-gradient-to-br from-green-900 to-green-800 rounded-lg p-4 text-center transform hover:scale-105 transition-transform">
              <div className="text-3xl font-bold text-green-200">{result.normal_count}</div>
              <div className="text-sm text-green-300 mt-1">Normales</div>
            </div>
            <div className="bg-gradient-to-br from-yellow-900 to-yellow-800 rounded-lg p-4 text-center transform hover:scale-105 transition-transform">
              <div className="text-3xl font-bold text-yellow-200">{result.toxicity_percentage.toFixed(1)}%</div>
              <div className="text-sm text-yellow-300 mt-1">Toxicidad</div>
            </div>
          </div>

          {/* Barra de progreso de toxicidad */}
          <div className="bg-gray-700 rounded-full h-6 overflow-hidden">
            <div 
              className={`h-full flex items-center justify-center text-xs font-bold text-white transition-all duration-1000 ${
                result.toxicity_percentage > 50 ? 'bg-red-600' : 
                result.toxicity_percentage > 25 ? 'bg-yellow-600' : 'bg-green-600'
              }`}
              style={{ width: `${result.toxicity_percentage}%` }}
            >
              {result.toxicity_percentage > 10 && `${result.toxicity_percentage.toFixed(1)}%`}
            </div>
          </div>

          {result.top_toxic_comments.length > 0 && (
            <div>
              <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                ⚠️ Top Comentarios Tóxicos
                <span className="text-sm font-normal text-gray-400">
                  (ordenados por confianza)
                </span>
              </h3>
              <div className="space-y-4">
                {result.top_toxic_comments.map((comment, index) => {
                  const isHighConfidence = comment.confidence > 0.80;
                  
                  return (
                    <div 
                      key={comment.comment_id} 
                      className={`bg-gray-700 rounded-lg p-4 hover:bg-gray-600 transition-colors border-l-4 ${
                        isHighConfidence 
                          ? 'border-toxic-high animate-shake border-red-600' 
                          : 'border-red-500'
                      }`}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <span className="bg-red-600 text-white px-3 py-1 rounded-full text-sm font-bold">
                            #{index + 1}
                          </span>
                          <span className="text-gray-300 font-medium">{comment.author}</span>
                        </div>
                        <span className="text-red-400 text-sm font-semibold bg-red-900 bg-opacity-50 px-3 py-1 rounded-full">
                          {(comment.confidence * 100).toFixed(1)}% confianza
                        </span>
                      </div>
                      <p className="text-white mb-3 leading-relaxed">{comment.text}</p>
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-gray-400">
                          📅 {new Date(comment.published_at).toLocaleDateString('es-ES')}
                        </span>
                        <span className="bg-red-800 text-red-200 px-3 py-1 rounded-full text-xs font-semibold">
                          🚫 Hate Speech
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default VideoAnalyzer