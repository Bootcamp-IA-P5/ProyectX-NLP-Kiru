import { useState } from 'react'
import api from '../services/api'

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
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al analizar el video')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-gray-800 rounded-xl shadow-2xl p-8">
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
            className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
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
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white font-bold py-3 px-6 rounded-lg transition-colors"
        >
          {loading ? '⏳ Analizando...' : '🔍 Analizar Video'}
        </button>
      </form>

      {error && (
        <div className="mt-6 bg-red-900 border border-red-700 text-red-200 px-4 py-3 rounded-lg">
          ❌ {error}
        </div>
      )}

      {result && (
        <div className="mt-8 space-y-6">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-white mb-2">📊 Resultados del Análisis</h2>
            <h3 className="text-lg text-gray-300">{result.video_title}</h3>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-gray-700 rounded-lg p-4 text-center">
              <div className="text-3xl font-bold text-white">{result.total_comments_analyzed}</div>
              <div className="text-sm text-gray-400 mt-1">Comentarios</div>
            </div>
            <div className="bg-red-900 rounded-lg p-4 text-center">
              <div className="text-3xl font-bold text-red-200">{result.toxic_count}</div>
              <div className="text-sm text-red-300 mt-1">Tóxicos</div>
            </div>
            <div className="bg-green-900 rounded-lg p-4 text-center">
              <div className="text-3xl font-bold text-green-200">{result.normal_count}</div>
              <div className="text-sm text-green-300 mt-1">Normales</div>
            </div>
            <div className="bg-yellow-900 rounded-lg p-4 text-center">
              <div className="text-3xl font-bold text-yellow-200">{result.toxicity_percentage.toFixed(1)}%</div>
              <div className="text-sm text-yellow-300 mt-1">Toxicidad</div>
            </div>
          </div>

          {result.top_toxic_comments.length > 0 && (
            <div>
              <h3 className="text-xl font-bold text-white mb-4">⚠️ Top Comentarios Tóxicos</h3>
              <div className="space-y-4">
                {result.top_toxic_comments.map((comment, index) => (
                  <div key={comment.comment_id} className="bg-gray-700 rounded-lg p-4 border-l-4 border-red-500">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span className="bg-red-600 text-white px-2 py-1 rounded text-sm font-bold">
                          #{index + 1}
                        </span>
                        <span className="text-gray-300 font-medium">{comment.author}</span>
                      </div>
                      <span className="text-red-400 text-sm font-semibold">
                        {(comment.confidence * 100).toFixed(1)}% confianza
                      </span>
                    </div>
                    <p className="text-white mb-3">{comment.text}</p>
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-gray-400">
                        {new Date(comment.published_at).toLocaleDateString('es-ES')}
                      </span>
                      <span className="bg-red-800 text-red-200 px-3 py-1 rounded-full text-xs font-semibold">
                        🚫 Hate Speech
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default VideoAnalyzer