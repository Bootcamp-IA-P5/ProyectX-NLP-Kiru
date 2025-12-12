import { useState } from 'react'
import api from '../services/api'

// Ejemplos de texto para probar
const EXAMPLE_TEXTS = [
  "This video is amazing, thanks for sharing!",
  "You're absolutely stupid and worthless",
  "I love this content, keep it up!",
  "Get out of here you idiot",
]

function ModelComparison() {
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleCompare = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await api.compareModels(text)
      setResult(response)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al comparar modelos')
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
      <div className="mb-6">
        <h2 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 mb-2">
          🔬 Comparación de Modelos
        </h2>
        <p className="text-gray-400">
          Compara las predicciones de Logistic Regression vs DistilBERT
        </p>
      </div>

      {/* Ejemplos Rápidos */}
      <div className="mb-6">
        <p className="text-sm text-gray-400 mb-2">⚡ Prueba con estos ejemplos:</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {EXAMPLE_TEXTS.map((example, index) => (
            <button
              key={index}
              onClick={() => loadExample(example)}
              className="text-left px-4 py-2 bg-gray-700 hover:bg-purple-600 text-gray-300 hover:text-white rounded-lg text-sm transition-colors"
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      <form onSubmit={handleCompare} className="space-y-6">
        <div>
          <label htmlFor="text" className="block text-sm font-medium text-gray-300 mb-2">
            Texto a Analizar
          </label>
          <textarea
            id="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Escribe un comentario para comparar las predicciones..."
            rows="4"
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
              Comparando...
            </span>
          ) : (
            '⚖️ Comparar Modelos'
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
          {/* Texto analizado */}
          <div className="bg-gray-700 rounded-lg p-4">
            <p className="text-gray-400 text-sm mb-1">Texto analizado:</p>
            <p className="text-white">{result.text}</p>
          </div>

          {/* Comparación lado a lado */}
          <div className="grid md:grid-cols-2 gap-6">
            {/* Logistic Regression */}
            <div className={`rounded-xl p-6 border-2 ${
              result.logistic_regression.prediction === 'hate_speech'
                ? 'bg-gradient-to-br from-red-900 to-red-800 border-red-600'
                : 'bg-gradient-to-br from-green-900 to-green-800 border-green-600'
            }`}>
              <div className="text-center mb-4">
                <h3 className="text-xl font-bold text-white mb-2">📊 Logistic Regression</h3>
                <div className="text-5xl mb-2">
                  {result.logistic_regression.prediction === 'hate_speech' ? '🚫' : '✅'}
                </div>
                <p className={`text-lg font-semibold ${
                  result.logistic_regression.prediction === 'hate_speech' ? 'text-red-200' : 'text-green-200'
                }`}>
                  {result.logistic_regression.prediction === 'hate_speech' ? 'Hate Speech' : 'Normal'}
                </p>
              </div>
              
              <div className="space-y-3">
                <div className="bg-black bg-opacity-30 rounded-lg p-3">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">Confianza:</span>
                    <span className="text-white font-bold text-lg">
                      {(result.logistic_regression.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="mt-2 bg-gray-700 rounded-full h-2 overflow-hidden">
                    <div 
                      className={`h-full transition-all duration-1000 ${
                        result.logistic_regression.prediction === 'hate_speech' ? 'bg-red-500' : 'bg-green-500'
                      }`}
                      style={{ width: `${result.logistic_regression.confidence * 100}%` }}
                    />
                  </div>
                </div>
                <div className="bg-black bg-opacity-30 rounded-lg p-3">
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-gray-300">Threshold:</span>
                    <span className="text-white">{result.logistic_regression.threshold}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* DistilBERT */}
            <div className={`rounded-xl p-6 border-2 ${
              result.distilbert.prediction === 'hate_speech'
                ? 'bg-gradient-to-br from-red-900 to-red-800 border-red-600'
                : 'bg-gradient-to-br from-green-900 to-green-800 border-green-600'
            }`}>
              <div className="text-center mb-4">
                <h3 className="text-xl font-bold text-white mb-2">🤖 DistilBERT</h3>
                <div className="text-5xl mb-2">
                  {result.distilbert.prediction === 'hate_speech' ? '🚫' : '✅'}
                </div>
                <p className={`text-lg font-semibold ${
                  result.distilbert.prediction === 'hate_speech' ? 'text-red-200' : 'text-green-200'
                }`}>
                  {result.distilbert.prediction === 'hate_speech' ? 'Hate Speech' : 'Normal'}
                </p>
              </div>
              
              <div className="space-y-3">
                <div className="bg-black bg-opacity-30 rounded-lg p-3">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">Confianza:</span>
                    <span className="text-white font-bold text-lg">
                      {(result.distilbert.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="mt-2 bg-gray-700 rounded-full h-2 overflow-hidden">
                    <div 
                      className={`h-full transition-all duration-1000 ${
                        result.distilbert.prediction === 'hate_speech' ? 'bg-red-500' : 'bg-green-500'
                      }`}
                      style={{ width: `${result.distilbert.confidence * 100}%` }}
                    />
                  </div>
                </div>
                {result.distilbert.probabilities && (
                  <div className="bg-black bg-opacity-30 rounded-lg p-3">
                    <p className="text-gray-300 text-sm mb-2">Probabilidades:</p>
                    <div className="space-y-1 text-xs">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Hate Speech:</span>
                        <span className="text-white">{(result.distilbert.probabilities.hate_speech * 100).toFixed(2)}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Normal:</span>
                        <span className="text-white">{(result.distilbert.probabilities.normal * 100).toFixed(2)}%</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Análisis de Comparación */}
          <div className="bg-gradient-to-r from-blue-900 to-purple-900 rounded-xl p-6 border-2 border-blue-600">
            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              📊 Análisis de Comparación
            </h3>
            
            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-black bg-opacity-30 rounded-lg p-4">
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-3xl">
                    {result.comparison.agreement ? '✅' : '⚠️'}
                  </span>
                  <div>
                    <p className="text-gray-300 text-sm">Concordancia</p>
                    <p className="text-white font-bold">
                      {result.comparison.agreement ? 'Ambos coinciden' : 'Predicciones diferentes'}
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-black bg-opacity-30 rounded-lg p-4">
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-3xl">📏</span>
                  <div>
                    <p className="text-gray-300 text-sm">Diferencia de Confianza</p>
                    <p className="text-white font-bold">
                      {(result.comparison.confidence_diff * 100).toFixed(2)}%
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-black bg-opacity-30 rounded-lg p-4">
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-3xl">
                    {result.comparison.both_confident ? '💪' : '🤔'}
                  </span>
                  <div>
                    <p className="text-gray-300 text-sm">Nivel de Certeza</p>
                    <p className="text-white font-bold">
                      {result.comparison.both_confident ? 'Ambos muy seguros (>70%)' : 'Confianza variable'}
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-black bg-opacity-30 rounded-lg p-4">
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-3xl">⭐</span>
                  <div>
                    <p className="text-gray-300 text-sm">Modelo Recomendado</p>
                    <p className="text-white font-bold">
                      {result.comparison.recommended_model === 'distilbert' ? '🤖 DistilBERT' : '📊 Logistic Regression'}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Gráfico de comparación de confianza */}
            <div className="mt-6">
              <p className="text-gray-300 text-sm mb-3">Comparación de Confianza:</p>
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-400">📊 Logistic Regression</span>
                    <span className="text-white font-bold">
                      {(result.logistic_regression.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="bg-gray-700 rounded-full h-3 overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-blue-500 to-blue-400 transition-all duration-1000"
                      style={{ width: `${result.logistic_regression.confidence * 100}%` }}
                    />
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-400">🤖 DistilBERT</span>
                    <span className="text-white font-bold">
                      {(result.distilbert.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="bg-gray-700 rounded-full h-3 overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-purple-500 to-pink-400 transition-all duration-1000"
                      style={{ width: `${result.distilbert.confidence * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ModelComparison