import { useState } from 'react'
import api from '../services/api'

function TextPredictor() {
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handlePredict = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await api.predictText(text)
      setResult(response)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al analizar el texto')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-gray-800 rounded-xl shadow-2xl p-8">
      <form onSubmit={handlePredict} className="space-y-6">
        <div>
          <label htmlFor="text" className="block text-sm font-medium text-gray-300 mb-2">
            Texto a Analizar
          </label>
          <textarea
            id="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Escribe o pega un comentario para analizar..."
            rows="6"
            required
            className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white font-bold py-3 px-6 rounded-lg transition-colors"
        >
          {loading ? '⏳ Analizando...' : '🔍 Analizar Texto'}
        </button>
      </form>

      {error && (
        <div className="mt-6 bg-red-900 border border-red-700 text-red-200 px-4 py-3 rounded-lg">
          ❌ {error}
        </div>
      )}

      {result && (
        <div className={`mt-8 rounded-xl p-6 ${
          result.prediction === 'hate_speech' 
            ? 'bg-red-900 border-2 border-red-600' 
            : 'bg-green-900 border-2 border-green-600'
        }`}>
          <h3 className={`text-2xl font-bold mb-4 ${
            result.prediction === 'hate_speech' ? 'text-red-200' : 'text-green-200'
          }`}>
            {result.prediction === 'hate_speech' ? '🚫 Hate Speech Detectado' : '✅ Texto Normal'}
          </h3>

          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-300 font-medium">Predicción:</span>
              <span className="text-white font-semibold">{result.prediction}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-300 font-medium">Confianza:</span>
              <span className="text-white font-semibold">{(result.confidence * 100).toFixed(2)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-300 font-medium">Modelo:</span>
              <span className="text-white font-semibold">{result.model}</span>
            </div>
          </div>

          <div className="mt-4 bg-gray-700 rounded-full h-4 overflow-hidden">
            <div 
              className={`h-full transition-all ${
                result.prediction === 'hate_speech' ? 'bg-red-500' : 'bg-green-500'
              }`}
              style={{ width: `${result.confidence * 100}%` }}
            />
          </div>
        </div>
      )}
    </div>
  )
}

export default TextPredictor