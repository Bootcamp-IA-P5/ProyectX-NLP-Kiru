import { useState } from 'react'
import api from '../services/api'

// Ejemplos de texto para probar
const EXAMPLE_TEXTS = [
  "This video is amazing, thanks for sharing!",
  "You're absolutely stupid and worthless",
  "I love this content, keep it up!",
]

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

  const loadExample = (exampleText) => {
    setText(exampleText)
    setError(null)
    setResult(null)
  }

  return (
    <div className="bg-gray-800 rounded-xl shadow-2xl p-8 backdrop-blur-sm bg-opacity-90">
      {/* Ejemplos Rápidos */}
      <div className="mb-6">
        <p className="text-sm text-gray-400 mb-2">⚡ Prueba con estos ejemplos:</p>
        <div className="space-y-2">
          {EXAMPLE_TEXTS.map((example, index) => (
            <button
              key={index}
              onClick={() => loadExample(example)}
              className="w-full text-left px-4 py-2 bg-gray-700 hover:bg-purple-600 text-gray-300 hover:text-white rounded-lg text-sm transition-colors"
            >
              {example}
            </button>
          ))}
        </div>
      </div>

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
            className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none transition-all"
          />
          <div className="text-right text-xs text-gray-500 mt-1">
            {text.length} caracteres
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
              Analizando...
            </span>
          ) : (
            '🔍 Analizar Texto'
          )}
        </button>
      </form>

      {error && (
        <div className="mt-6 bg-red-900 border border-red-700 text-red-200 px-4 py-3 rounded-lg animate-pulse">
          ❌ {error}
        </div>
      )}

      {result && (
        <div className={`mt-8 rounded-xl p-6 border-2 animate-fadeIn ${
          result.prediction === 'hate_speech' 
            ? 'bg-gradient-to-br from-red-900 to-red-800 border-red-600' 
            : 'bg-gradient-to-br from-green-900 to-green-800 border-green-600'
        }`}>
          <div className="text-center mb-6">
            <div className="text-6xl mb-4">
              {result.prediction === 'hate_speech' ? '🚫' : '✅'}
            </div>
            <h3 className={`text-3xl font-bold mb-2 ${
              result.prediction === 'hate_speech' ? 'text-red-200' : 'text-green-200'
            }`}>
              {result.prediction === 'hate_speech' ? 'Hate Speech Detectado' : 'Texto Normal'}
            </h3>
          </div>

          <div className="space-y-4">
            <div className="bg-black bg-opacity-30 rounded-lg p-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-300 font-medium">Predicción:</span>
                <span className={`font-bold ${
                  result.prediction === 'hate_speech' ? 'text-red-300' : 'text-green-300'
                }`}>
                  {result.prediction === 'hate_speech' ? 'Hate Speech' : 'Normal'}
                </span>
              </div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-300 font-medium">Confianza:</span>
                <span className="text-white font-bold text-xl">
                  {(result.confidence * 100).toFixed(2)}%
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-300 font-medium">Modelo:</span>
                <span className="text-white font-semibold">
                  {result.model && result.model.includes('distilbert') ? '🤖 DistilBERT' : '📊 Logistic Regression'}
                </span>
              </div>
            </div>

            {/* Barra de confianza */}
            <div>
              <div className="text-sm text-gray-300 mb-2 flex justify-between">
                <span>Nivel de Confianza</span>
                <span className="font-bold">{(result.confidence * 100).toFixed(1)}%</span>
              </div>
              <div className="bg-gray-700 rounded-full h-4 overflow-hidden">
                <div 
                  className={`h-full transition-all duration-1000 ${
                    result.prediction === 'hate_speech' ? 'bg-red-500' : 'bg-green-500'
                  }`}
                  style={{ width: `${result.confidence * 100}%` }}
                />
              </div>
            </div>

            {/* Indicador de certeza */}
            <div className="text-center pt-4 border-t border-gray-600">
              {result.confidence > 0.9 ? (
                <span className="text-yellow-300 font-semibold">🔥 Alta certeza en la predicción</span>
              ) : result.confidence > 0.7 ? (
                <span className="text-blue-300 font-semibold">✓ Confianza moderada</span>
              ) : (
                <span className="text-gray-400 font-semibold">⚠️ Predicción con baja confianza</span>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default TextPredictor